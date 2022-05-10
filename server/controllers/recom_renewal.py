import os
from typing import List
from fastapi import APIRouter
from jsf import JSF

from models.recom_renewal import (
    ResultByIdInput, ResultByIdOutput,
    ResultByGnoInput, ResultByGnoOutput,
    EnvInput,
    GetUsersOutput,
    MonitorModelByBzOutput,
    MonitorResultByBzOutput
)
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
    m_id = body.m_id
    tbl_name = "mlresult_staging.mf_gi_sim" if body.env == "staging" else "mlresult.mf_gi_sim"
    query = f"""
WITH RAW_TABLE AS (
  WITH USER_HISTORY(m_id, gno, actvt_code, dt, is_include) AS (
    WITH PARAM(m_id) AS (
      SELECT '{m_id}' AS m_id -- [INPUT] Change ID to Test!!!
    )

    -- Extract user-interacted gno
    SELECT DISTINCT
      t.m_id
      , t.gno
      , min(t.actvt_code) OVER (PARTITION BY t.gno) AS actvt_code
      , max(t.dt) OVER (PARTITION BY t.gno) AS dt
      , IF(sim.gno IS NOT NULL, 'O', 'X') AS is_include
    FROM (
      SELECT t.m_id, gno, actvt_code, log_dt AS dt
      FROM job_db30_gg.log_gg_actvt t
      JOIN param p ON t.m_id = p.m_id

      UNION ALL

      SELECT t.m_id, gno, 5 AS actvt_code, hist_dt AS dt
      FROM job_db30_etc.agi_click_login_hist t
      JOIN param p ON t.m_id = p.m_id
    ) t
    LEFT JOIN {tbl_name} sim ON t.gno = sim.gno
    ORDER BY is_include ASC, dt DESC, actvt_code ASC -- SORT: LATEST TRAINED INTERACTION
    LIMIT 10
  )

  -- Concat input gno & output gno
  SELECT
    'UserHistory' AS kind
    , uh.m_id
    , uh.gno
    , (
      CASE uh.actvt_code
        WHEN 1 THEN '온라인 지원'
        WHEN 2 THEN '이메일 지원'
        WHEN 3 THEN '스크랩'
        WHEN 4 THEN '홈페이지 지원'
        WHEN 5 THEN '클릭'
      END
    ) AS actvt_code
    , uh.dt
    , uh.is_include
    , NULL AS score
  FROM USER_HISTORY uh

  UNION ALL

  (SELECT
    'Recommend' AS kind
    , NULL AS m_id
    , recom_gno AS gno
    , NULL AS actvt_code
    , NULL AS dt
    , NULL AS is_include
    , avg(sim.score + (1 - sim.score) * (
        CASE uh.actvt_code
          WHEN 1 THEN 0.6
          WHEN 2 THEN 0.5
          WHEN 3 THEN 0.4
          WHEN 4 THEN 0.3
          WHEN 5 THEN 0.2
        END
    )) AS score
  FROM {tbl_name} sim
  JOIN USER_HISTORY uh ON sim.gno = uh.gno
  WHERE sim.score > 0.90
  GROUP BY recom_gno
  ORDER BY score DESC
  LIMIT 200)
)

-- Join profiles
SELECT
  t.kind
  , t.m_id
  , t.gno
  , t.actvt_code
  , t.is_include
  , t.dt
  , t.score
  , agi.gi_title AS TITLE
  , bzt._1 AS BZT_1
  , bzt._2 AS BZT_2
  , localty._1 AS LOCAL_1
  , localty._2 AS LOCAL_2
  , IF(pay.is_paid IS NOT NULL, 'O', 'X') AS IS_PAID
  , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(t.gno as VARCHAR)) AS URL
FROM RAW_TABLE t

-- TITLE
LEFT JOIN (SELECT gno, gi_title FROM JOB_DB30_GI.AGI WHERE year IN (2021, 2022)) agi ON t.Gno = agi.Gno

-- BizJobType
LEFT JOIN (
  SELECT
    t.gno,
    array_join(array_distinct(array_agg(bztc.BizJobType_Bctgr_Name)), ' / ') AS _1,
    array_join(array_distinct(array_agg(bzt.BizJobType_Name)), ' / ') AS _2
  FROM RAW_TABLE t
  LEFT JOIN JOB_DB30_GI.AGI_BizJobtype agi_bzt ON (t.Gno = agi_bzt.Gno)
  LEFT JOIN JOB_DB30_GI.Code_BizJobtype bzt ON (agi_bzt.BizJobtype_Code = bzt.BizJobtype_Code)
  LEFT JOIN JOB_DB30_GI.Code_BizJobtype_Bctgr bztc ON bzt.BizJobtype_Bctgr_Code = bztc.BizJobtype_Bctgr_Code
  GROUP BY t.gno
) bzt ON t.gno = bzt.gno

-- Localty
LEFT JOIN (
  SELECT
    t.gno,
    array_join(array_distinct(array_agg(localty_outer.local_name)), ' / ') AS _1,
    array_join(array_distinct(array_agg(localty_inner.local_name)), ' / ') AS _2
  FROM RAW_TABLE t
  LEFT JOIN JOB_DB30_GI.AGI_Work_Local agi_local ON t.Gno = agi_local.Gno
  LEFT JOIN JOB_DB30_GI.Code_Local localty_inner ON agi_local.Local_Code = localty_inner.Local_Code
  LEFT JOIN JOB_DB30_GI.Code_Local localty_outer ON localty_inner.local_ctgr_code = localty_outer.Local_Code
  GROUP BY t.gno
) localty ON t.gno = localty.gno

-- IS_PAID
LEFT JOIN (
  SELECT DISTINCT gno, 1 AS is_paid
  FROM JOB_DB30_GI.AGI_Opt
) pay ON t.gno = pay.gno

ORDER BY t.kind DESC, t.dt DESC, t.score DESC -- ORDERING
    """
    query = query_result_by_id.func(body)
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
    query = query_monitor_result_by_bz.string
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(MonitorResultByBzOutput.schema()).generate(3)
    return data

