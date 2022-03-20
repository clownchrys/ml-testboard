import os
from typing import List
from fastapi import APIRouter

from models.recom_renewal import (
    ResultByIdInput, ResultByIdOutput,
    ResultByGnoInput, ResultByGnoOutput
)
from dummies.recom_renewal import (
    result_by_id, result_by_gno
)
from connections import PrestoExecutor

router = APIRouter()
tag = os.path.basename(__file__)


@router.post("/result_by_id", tags=[tag], response_model=List[ResultByIdOutput], description="유저별 검증")
async def get_result_by_id(body: ResultByIdInput):
    query = f"""
WITH RAW_TABLE AS (

  WITH USER_HISTORY(m_id, gno, actvt_code, dt, is_include) AS (

    WITH PARAM(m_id) AS (

      SELECT '{body.m_id}' AS m_id -- [INPUT] Change ID to Test!!!

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

    LEFT JOIN mlresult.mf_gi_sim sim ON t.gno = sim.gno

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

    -- , sum(sim.score + (1 - sim.score) * (

    --     CASE uh.actvt_code

    --       WHEN 1 THEN 0.6

    --       WHEN 2 THEN 0.5

    --       WHEN 3 THEN 0.4

    --       WHEN 4 THEN 0.3

    --       WHEN 5 THEN 0.2

    --     END

    -- )) AS score

    , avg(sim.score + (1 - sim.score) * (

        CASE uh.actvt_code

          WHEN 1 THEN 0.6

          WHEN 2 THEN 0.5

          WHEN 3 THEN 0.4

          WHEN 4 THEN 0.3

          WHEN 5 THEN 0.2

        END

    )) AS score

  FROM mlresult.mf_gi_sim sim

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
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = result_by_id
    return data


@router.post("/result_by_gno", tags=[tag], response_model=List[ResultByGnoOutput], description="공고별 검증")
async def get_result_by_gno(body: List[ResultByGnoInput]):
    elems = ",".join([ f"ARRAY[{model.gno}, {model.actvt_code}]" for model in body ])

    query = f"""
WITH RAW_TABLE AS (

  WITH USER_HISTORY(gno, actvt_code, is_include, rownum) AS (

  

    -- UserHistory

    -- (gno, actvt_code) combinations TO TEST

    WITH INPUT_GNO AS (

      SELECT ARRAY[
        { elems }
      ] AS inputs
    )

    SELECT DISTINCT

        t.info[1] AS gno

      , t.info[2] AS actvt_code

      , IF(EXISTS (SELECT 1 FROM mlresult.mf_gi_sim sim WHERE gno = t.info[1]), 'O', 'X') AS is_include

      , row_number() OVER () AS rownum

    FROM INPUT_GNO

    CROSS JOIN UNNEST(inputs) AS t (info)

  )

  

  -- Union USER_HISTORY & RECOMMEND

  SELECT

    'UserHistory' AS kind

    , gno

    , (

      CASE actvt_code

        WHEN 1 THEN '온라인 지원'

        WHEN 2 THEN '이메일 지원'

        WHEN 3 THEN '스크랩'

        WHEN 4 THEN '홈페이지 지원'

        WHEN 5 THEN '클릭'

      END

    ) AS actvt_code

    , is_include

    , NULL AS score

    , rownum

  FROM USER_HISTORY

  

  UNION ALL

  

  (SELECT

    'Recommend' AS kind

    , recom_gno AS gno

    , NULL AS actvt_code

    , NULL AS is_include

    , sum(sim.score + (1 - sim.score) * (

        CASE uh.actvt_code

          WHEN 1 THEN 0.6

          WHEN 2 THEN 0.5

          WHEN 3 THEN 0.4

          WHEN 4 THEN 0.3

          WHEN 5 THEN 0.2

        END

    )) AS score

    , NULL AS rownum

  FROM mlresult.mf_gi_sim sim

  JOIN USER_HISTORY uh ON sim.gno = uh.gno

  WHERE sim.score > 0.90

  GROUP BY recom_gno

  ORDER BY score DESC

  LIMIT 200)

)



-- Join profiles

SELECT

    t.kind

  , t.gno

  , t.actvt_code

  , t.is_include

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



ORDER BY t.kind DESC, t.score DESC, t.rownum -- ORDERING
    """
    # print(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = result_by_gno
    return data
