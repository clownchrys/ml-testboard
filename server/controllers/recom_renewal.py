import os
from typing import List
from fastapi import APIRouter
from jsf import JSF

from models.recom_renewal import *
from queries.recom_renewal import (
    query_result_by_id,
    query_result_by_gno,
    query_get_users,
    query_monitor_model_by_bz,
    query_monitor_result_by_bz
)
from connections import PrestoExecutor

router = APIRouter()
tag = os.path.basename(__file__)


@router.post("/result_by_id", tags=[tag], response_model=List[ResultByIdOutput], description="유저별 검증")
async def handler_result_by_id(body: ResultByIdInput):
	M_ID = body.m_id
	TBL_NAME = "mlresult_staging.mf_gi_sim" if body.env == "staging" else "mlresult.mf_gi_sim"

	LOG_CNT = 10
	RECM_CNT = 100
	THRESHOLD = 0.9
	DISCOUNT_RATE = 0.1

	query = f"""
	WITH
	IN_OUT_TABLE AS (
	  WITH
	  Code_Recm_Weight_Value (Actvt_Code, Weight_Value) AS (
		VALUES (1, 0.6), (2, 0.5), (3, 0.4), (4, 0.3), (5, 0.2)
	  ),
	  User_Actvt_Log AS (
		-- Calculate Weight
		SELECT
		  Gno
		  , B.Weight_Value * POWER(1.0 / (1 + {DISCOUNT_RATE}), DATE_DIFF('DAY', A.Dt, NOW())) AS Weight -- @DiscountRate
		  -- For QA
		  , A.Actvt_Code
		  , A.Dt
		FROM
		-- Aggregate Actvt_Code & Dt
		(
		  SELECT
			Gno
			, min(Actvt_Code) AS Actvt_Code
			, max(Dt) AS Dt
		  FROM
		  -- Get Raw User Log
		  (
			SELECT
			  Gno
			  , Actvt_Code
			  , Log_Dt AS Dt
			FROM JOB_DB30_GG.Log_GG_Actvt
			WHERE M_ID = {M_ID!r} AND DATE_DIFF('MONTH', Log_Dt, NOW()) <= 3 -- @M_ID / 3개월 내의 인터렉션만 반영
			
			UNION ALL
			
			SELECT
			  Gno
			  , 5 AS Actvt_Code
			  , Hist_Dt AS Dt
			FROM JOB_DB30_ETC.AGI_Click_Login_Hist
			WHERE M_ID = {M_ID!r} AND DATE_DIFF('MONTH', Hist_Dt, NOW()) <= 3 -- @M_ID / 3개월 내의 인터렉션만 반영
		  )
		  GROUP BY Gno  
		) A
		INNER JOIN Code_Recm_Weight_Value B ON A.Actvt_Code = B.Actvt_Code
		WHERE A.Gno IN (SELECT Gno FROM {TBL_NAME})
		ORDER BY Dt DESC -- 시간 우선
		LIMIT {LOG_CNT} -- @LogCnt
	  ) -- END OF INNER WITH
	  
	  SELECT *
	  FROM
	  (
		SELECT
		  T.Gno
		  , 'UserHistory' AS Kind
		  , 'O' AS Is_Include
		  , T.Actvt_Code
		  , T.Dt
		  , null AS Score
		FROM User_Actvt_Log T
		
		UNION ALL
		
		SELECT
		  T.Gno
		  , 'Recommend' AS Kind
		  , null AS Is_Include
		  , null AS Actvt_Code
		  , null AS Dt
		  , T.Score
		FROM
		-- Procedure Output
		(
		  SELECT
			B.Recom_Gno AS Gno
			, SUM(B.Score * A.Weight) AS Score
			--, ROW_NUMBER() OVER (ORDER BY SUM(B.Score * A.Weight)) AS ScoreRank
		  FROM User_Actvt_Log A
		  INNER JOIN {TBL_NAME} B ON A.Gno = B.Gno
		  WHERE
--B.Score > {THRESHOLD} -- @Threshold
			--AND
B.Recom_Gno NOT IN (
			  SELECT Gno
			  FROM JOB_DB30_GG.Log_GG_Actvt
			  WHERE M_ID = {M_ID!r} AND Actvt_Code IN (1, 2, 3, 4) -- @M_ID
			)
		  GROUP BY B.Recom_Gno
		  ORDER BY Score DESC
		  LIMIT {RECM_CNT} -- @Recm_Cnt
		) T
	  )
	) -- END OF OUTER WITH

	SELECT
	  T.Kind
	  , {M_ID!r} AS m_id -- @M_ID
	  , T.Gno
	  , T.Is_Include
	  , CASE T.Actvt_Code
		WHEN 1 THEN '온라인 지원'
		WHEN 2 THEN '이메일 지원'
		WHEN 3 THEN '스크랩'
		WHEN 4 THEN '홈페이지 지원'
		WHEN 5 THEN '클릭'
		END AS actvt_code
	  , T.Dt
	  , T.Score
	  , AGI.GI_Title AS TITLE
	  , BZT._1 AS BZT_1
	  , BZT._2 AS BZT_2
	  , LOC._1 AS LOCAL_1
	  , LOC._2 AS LOCAL_2
	  , CASE OPT.IS_PAID WHEN 1 THEN 'O' ELSE 'X' END AS IS_PAID
	  , CONCAT('https://www.jobkorea.co.kr/recruit/gi_read/', CAST(T.Gno AS VARCHAR)) AS URL
	FROM IN_OUT_TABLE T

	-- ADD PROFILE!!!

	-- 1: TITLE
	LEFT JOIN (SELECT Gno, GI_Title FROM JOB_DB30_GI.AGI WHERE year IN (2021, 2022)) AGI ON T.Gno = AGI.Gno

	-- 2: BizJobType
	LEFT JOIN (
	  SELECT
		T.Gno,
		ARRAY_JOIN(ARRAY_DISTINCT(ARRAY_AGG(bztc.BizJobType_Bctgr_Name)), ' / ') AS _1,
		ARRAY_JOIN(ARRAY_DISTINCT(ARRAY_AGG(bzt.BizJobType_Name)), ' / ') AS _2
	  FROM IN_OUT_TABLE t
	  LEFT JOIN JOB_DB30_GI.AGI_BizJobtype agi_bzt ON (t.Gno = agi_bzt.Gno)
	  LEFT JOIN JOB_DB30_GI.Code_BizJobtype bzt ON (agi_bzt.BizJobtype_Code = bzt.BizJobtype_Code)
	  LEFT JOIN JOB_DB30_GI.Code_BizJobtype_Bctgr bztc ON bzt.BizJobtype_Bctgr_Code = bztc.BizJobtype_Bctgr_Code
	  GROUP BY t.gno
	) BZT ON T.gno = BZT.gno

	-- 3: Local
	LEFT JOIN (
	  SELECT
		t.gno,
		ARRAY_JOIN(ARRAY_DISTINCT(ARRAY_AGG(local_outer.local_name)), ' / ') AS _1,
		ARRAY_JOIN(ARRAY_DISTINCT(ARRAY_AGG(local_inner.local_name)), ' / ') AS _2
	  FROM IN_OUT_TABLE t
	  LEFT JOIN JOB_DB30_GI.AGI_Work_Local agi_local ON t.Gno = agi_local.Gno
	  LEFT JOIN JOB_DB30_GI.Code_Local local_inner ON agi_local.Local_Code = local_inner.Local_Code
	  LEFT JOIN JOB_DB30_GI.Code_Local local_outer ON local_inner.local_ctgr_code = local_outer.Local_Code
	  GROUP BY t.gno
	) LOC ON T.gno = LOC.gno

	-- 4: IS_PAID
	LEFT JOIN (
	  SELECT DISTINCT gno, 1 AS IS_PAID
	  FROM JOB_DB30_GI.AGI_Opt
	) OPT ON T.gno = OPT.gno

	ORDER BY T.Kind DESC, T.Score DESC
    """
	#query = query_result_by_id.func(body)
	data = PrestoExecutor.execute(query, include_rowid=True)
	# data = JSF(ResultByStoryUserOutput.schema()).generate(3)
	return data


@router.post("/result_by_gno", tags=[tag], response_model=List[ResultByGnoOutput], description="공고별 검증")
async def handler_result_by_gno(body: List[ResultByGnoInput]):
    #tbl_name = "mlresult_staging.mf_gi_sim" if body.env == "staging" else "mlresult.mf_gi_sim"
    query = query_result_by_gno.func(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(ResultByGnoOutput.schema()).generate(3)
    return data


@router.post("/get_users", tags=[tag], response_model=List[GetUsersOutput], description="추천 가능한 유저 목록 조회")
async def handler_get_users(body: EnvInput):
    tbl_name = "mlresult_staging.mf_gi_sim" if body.env == "staging" else "mlresult.mf_gi_sim"
    query = f"""
SELECT DISTINCT m_id                                                                                                                                                                             
FROM (
  SELECT m_id, gno FROM job_db30_gg.log_gg_actvt
  UNION ALL
  SELECT m_id, gno FROM job_db30_etc.agi_click_login_hist
) t
WHERE EXISTS (SELECT 1 FROM {tbl_name} sim WHERE sim.gno = t.gno)
LIMIT 10000
    """
    query = query_get_users.string
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(GetUsersOutput.schema()).generate(3)
    return data


@router.post("/monitor_model_by_bz", tags=[tag], response_model=List[MonitorModelByBzOutput], description="직무 산업별 모델 출력 조회")
async def handler_monitor_model_by_bz(body: EnvInput):
    tbl_name = "mlresult_staging.mf_gi_sim" if body.env == "staging" else "mlresult.mf_gi_sim"
    query = f"""
WITH RAW_TABLE AS
(
  SELECT
 
  t.gno,
  t.recom_gno,
  t.score
  FROM
  (
    SELECT gno, recom_gno, score, rank
    FROM (
        SELECT gno, recom_gno, rank()
               over (PARTITION BY gno ORDER BY score DESC) as rank, score
        FROM {tbl_name} where gno in
              (
                SELECT tt.gno gno
                from
                  (
                  SELECT gno, bizjobtype_code, rank() OVER (PARTITION BY bizjobtype_code ORDER BY rand()) AS rn
                  FROM (SELECT * from job_db30_gi.agi_bizjobtype where gno in (SELECT DISTINCT(gno) gno from {tbl_name}))
                  ) tt
                WHERE tt.rn=1
              )
    ) ranked_table
   
    WHERE ranked_table.rank <= 5
  ) t
  ORDER BY t.gno, t.score DESC
)
 
select
    t.gno
  , t.recom_gno
  , t.score
  , gno_info.gi_title AS title
  , recom_gno_info.gi_title AS title_recom
  , bzt._1 AS BZT_1
  , bzt._2 AS BZT_2
  , localty._1 AS LOCAL_1
  , localty._2 AS LOCAL_2
 
from RAW_TABLE t
 
-- title
LEFT JOIN (SELECT gno, gi_title FROM JOB_DB30_GI.AGI WHERE year IN (2021, 2022)) gno_info ON t.Gno = gno_info.Gno
LEFT JOIN (SELECT gno, gi_title FROM JOB_DB30_GI.AGI WHERE year IN (2021, 2022)) recom_gno_info ON t.recom_gno = recom_gno_info.gno
 
--biz
LEFT JOIN
(
  SELECT
        tb.gno gno,
        array_join(array_distinct(array_agg(bztc.BizJobType_Bctgr_Name)), ' / ') AS _1,
        array_join(array_distinct(array_agg(bzt.BizJobType_Name)), ' / ') AS _2
    FROM (SELECT DISTINCT(gno) gno from {tbl_name}) tb
    LEFT JOIN JOB_DB30_GI.AGI_BizJobtype agi_bzt ON (tb.gno = agi_bzt.Gno)
    LEFT JOIN JOB_DB30_GI.Code_BizJobtype bzt ON (agi_bzt.BizJobtype_Code = bzt.BizJobtype_Code)
    LEFT JOIN JOB_DB30_GI.Code_BizJobtype_Bctgr bztc ON bzt.BizJobtype_Bctgr_Code = bztc.BizJobtype_Bctgr_Code
    GROUP BY tb.gno
) bzt On t.recom_gno = bzt.gno
 
-- Localty
LEFT JOIN (
  SELECT
    tl.gno,
    array_join(array_distinct(array_agg(localty_outer.local_name)), ' / ') AS _1,
    array_join(array_distinct(array_agg(localty_inner.local_name)), ' / ') AS _2
  FROM (SELECT DISTINCT(gno) gno from {tbl_name}) tl
  LEFT JOIN JOB_DB30_GI.AGI_Work_Local agi_local ON tl.Gno = agi_local.Gno
  LEFT JOIN JOB_DB30_GI.Code_Local localty_inner ON agi_local.Local_Code = localty_inner.Local_Code
  LEFT JOIN JOB_DB30_GI.Code_Local localty_outer ON localty_inner.local_ctgr_code = localty_outer.Local_Code
  GROUP BY tl.gno
) localty ON t.recom_gno = localty.gno
 
order by t.gno, t.score desc
"""
    #query = query_monitor_model_by_bz.string
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(MonitorModelByBzOutput.schema()).generate(3)
    return data


@router.post("/monitor_result_by_bz", tags=[tag], response_model=List[MonitorResultByBzOutput], description="직무 산업별 추천 결과 조회")
async def handler_monitor_result_by_bz(body: EnvInput):
    tbl_name = "mlresult_staging.mf_gi_sim" if body.env == "staging" else "mlresult.mf_gi_sim"
    query = f"""
WITH CTE AS (
  SELECT *
  FROM (
    SELECT
        M_Id
      , t.Gno
      , min(t.Actvt_Code) AS Actvt_Code
      , row_number() OVER (PARTITION BY M_Id ORDER BY max(Dt) DESC, min(Actvt_Code) ASC) AS Sort_Order -- SORT: LATEST TRAINED INTERACTIONj
    FROM (
      SELECT M_Id, Gno, Actvt_Code, Log_Dt AS Dt
      FROM JOB_DB30_GG.Log_GG_Actvt
      UNION ALL

      SELECT M_Id, Gno, 5 AS Actvt_Code, Hist_Dt AS Dt
      FROM JOB_DB30_ETC.AGI_Click_Login_Hist t
    ) t
    INNER JOIN {tbl_name} sim ON t.gno = sim.gno
    GROUP BY t.M_Id, t.Gno
  )
  WHERE Sort_Order <= 10
)

SELECT m_id, bizjobtype_bctgr_name, bizjobtype_name
FROM (
  SELECT *
      -- , row_number() OVER (PARTITION BY BizJobtype_Bctgr_Code, BizJobType_Code ORDER BY random()) AS rownum -- random sampling
      , row_number() OVER (PARTITION BY BizJobtype_Bctgr_Code, BizJobType_Code ORDER BY cnt DESC) AS rownum -- max sampling
  FROM (
    SELECT
        A.M_Id
      , B.Gno
      , B.BizJobType_Code, C.BizJobType_Name
      , C.BizJobtype_Bctgr_Code, D.BizJobType_Bctgr_Name
      , count() OVER (PARTITION BY A.M_Id, C.BizJobtype_Bctgr_Code, C.BizJobType_Code) AS cnt
    FROM CTE A
    INNER JOIN JOB_DB30_GI.AGI_BizJobType B ON A.Gno = B.Gno
    INNER JOIN JOB_DB30_GI.Code_BizJobType C ON B.BizJobType_Code = C.BizJobType_Code
    INNER JOIN JOB_DB30_GI.Code_BizJobtype_Bctgr D ON C.BizJobtype_Bctgr_Code = D.BizJobtype_Bctgr_Code -- to display bctgr name
  ) 
)
WHERE rownum <= 1
    """
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(MonitorResultByBzOutput.schema()).generate(3)
    return data


@router.post("/result_model_by_gno", tags=[tag], response_model=List[ResultModelByGnoOutput], description="모델 결과 조회")
async def handler_result_model_by_gno(body: ResultModelByGnoInput):
    db = "mlresult_staging" if body.env else "mlresult"
    table = "mf_gi_sim"
    query = f"""
select a.recom_gno as gno 
, b.gi_title 
, array_join(array_sort(array_distinct(array_agg(cb_sim.bizjobtype_name))), ',') as jobname 
, a.score 
, concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(a.recom_gno as varchar)) as link 
from {db}.{table} a join job_db30_gi.agi b on b.gno = a.recom_gno 
join job_db30_gi.agi_bizjobtype c on b.gno = c.gno 
join job_db30_gi.code_bizjobtype cb_sim on cb_sim.bizjobtype_code = c.bizjobtype_code and cb_sim.bizjobtype_type_code = 2 
where a.gno = {body.gno} 
group by a.recom_gno, b.gi_title, a.score
    """
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(ResultModelByGnoOutput.schema()).generate(3)
    return data
