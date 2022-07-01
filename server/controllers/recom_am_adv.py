import os
from typing import List
from fastapi import APIRouter
from jsf import JSF

from models.recom_am_adv import (
    ResultByUserStoryInput, ResultByStoryUserOutput,
    ResultUserProfile,
)
from connections import PrestoExecutor

router = APIRouter()
tag = os.path.basename(__file__)

db_name = "user_story_am"


@router.post("/result_by_user_story", tags=[tag], response_model=List[ResultByStoryUserOutput], description="유저별 검증")
async def handler_result_by_user_story(body: ResultByUserStoryInput):
    if body.story_number == 18:
        query = f"""
        SELECT
        T.m_id
        , (SELECT story_title FROM {db_name}.story_table WHERE story_no = {body.story_number}) AS story_title
        , AGI.gi_title
        , T.score
        , CNT.am_clickacum_cnt
        , CNT.am_applyacum_cnt
        , concat('https://www.albamon.com/recruit/view/gi?AL_GI_No=', cast(T.gno AS VARCHAR)) AS url
        FROM (select {body.m_id!r} as m_id ,gno, score from {db_name}.story_{body.story_number} where location_code='9999'
              ) as T
          LEFT JOIN (SELECT al_gi_no as gno, subject as gi_title FROM mongi.mon_guin_db WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
          LEFT JOIN (SELECT al_gi_no as gno, am_clickacum_cnt, am_applyacum_cnt FROM mldata.profile_am_recruit) CNT ON T.gno = CNT.gno
        ORDER BY T.score DESC        
        """
    elif body.story_number == 32:
        query = f"""    
        with USERFILTER as (
            SELECT A.m_id, t.location_code
            FROM {db_name}.user_profile as A
              cross join UNNEST(split(location_code, ',')) as t(location_code)
            where m_id={body.m_id!r}
        ),
        
        LOCATION as (
          --gu code
        select m_id, location_code
        from (
          select m_id, location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.gu_code=B.location_code
          
          union all
          --convert from si_code to gu_codes
          select m_id, gu_code as location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.si_code=B.location_code
        
          union all
          --convert from gu_code to si_code
          select m_id, si_code as location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.gu_code=B.location_code
          )
        group by m_id,location_code
        )
        
        SELECT
        T.m_id
        , concat(substr(cast(T.work_sdate as VARCHAR),3,2), '월 ', substr(cast(T.work_sdate as VARCHAR),5,2),'일 하루 ', PART_CODE.partname, '알바 가능하세요?') as story_title
        , AGI.gi_title
        , CODE.local_name
        , PART_CODE.partname
        , T.work_sdate
        , T.score
        , CNT.am_clickacum_cnt
        , CNT.am_applyacum_cnt
        , concat('https://www.albamon.com/recruit/view/gi?AL_GI_No=', cast(T.gno AS VARCHAR)) AS url
        FROM (  select A.m_id,B.gno, B.location_code, B.part_code, B.work_sdate , sum(score) as score
                from LOCATION as A
                inner join {db_name}.story_{body.story_number} as B
                on A.location_code=B.location_code
                group by (m_id,gno,B.part_code, B.work_sdate, B.location_code)
                ORDER BY score DESC LIMIT 200
              ) as T
          LEFT JOIN (SELECT al_gi_no as gno, subject as gi_title FROM mongi.mon_guin_db WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
          LEFT JOIN (select local_code, local_name from job_db30_gi.code_local) CODE ON T.location_code = CODE.local_code
          LEFT JOIN (select partcode, partname from mongi.mon_part_code) as PART_CODE on T.part_code=PART_CODE.partcode
          LEFT JOIN (SELECT al_gi_no as gno, am_clickacum_cnt, am_applyacum_cnt FROM mldata.profile_am_recruit) CNT ON T.gno = CNT.gno
        ORDER BY T.part_code, T.work_sdate, T.score DESC
        """

    elif body.story_number == 33:
        query = f"""
        with USERFILTER as (
            SELECT A.m_id, t.location_code
            FROM {db_name}.user_profile as A
              cross join UNNEST(split(location_code, ',')) as t(location_code)
            where m_id={body.m_id!r}
        ),
        
        LOCATION as (
          --gu code
        select m_id, location_code
        from (
          select m_id, location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.gu_code=B.location_code
          
          union all
          --convert from si_code to gu_codes
          select m_id, gu_code as location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.si_code=B.location_code
        
          union all
          --convert from gu_code to si_code
          select m_id, si_code as location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.gu_code=B.location_code
          )
        group by m_id,location_code
        )
        
        
        SELECT
        T.m_id
        , concat('다음주에 근무할 단기 ' , PART_CODE.partname , ' 공고') as story_title
        , AGI.gi_title
        , CODE.local_name
        , PART_CODE.partname
        , T.score
        , CNT.am_clickacum_cnt
        , CNT.am_applyacum_cnt
        , concat('https://www.albamon.com/recruit/view/gi?AL_GI_No=', cast(T.gno AS VARCHAR)) AS url
        FROM (  select A.m_id,B.gno, B.location_code, B.part_code, sum(score) as score
                from LOCATION as A
                inner join {db_name}.story_{body.story_number} as B
                on A.location_code=B.location_code
                group by (m_id,gno,B.part_code, B.location_code)
                ORDER BY score DESC LIMIT 200
              ) as T
          LEFT JOIN (SELECT al_gi_no as gno, subject as gi_title FROM mongi.mon_guin_db WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
          LEFT JOIN (select local_code, local_name from job_db30_gi.code_local) CODE ON T.location_code = CODE.local_code
          LEFT JOIN (select partcode, partname from mongi.mon_part_code) as PART_CODE on T.part_code=PART_CODE.partcode
          LEFT JOIN (SELECT al_gi_no as gno, am_clickacum_cnt, am_applyacum_cnt FROM mldata.profile_am_recruit) CNT ON T.gno = CNT.gno
        ORDER BY T.part_code, T.score DESC
        """

    elif body.story_number == 97:
        query = f"""
        WITH
        CODE_ACTIVITY_WEIGHT(actvt_code, actvt_weight) AS (
          VALUES (1, 0.6), (2, 0.5), (3, 0.4), (4, 0.3), (5, 0.2)
        ),
        USER_HISTORY(al_gi_no, weight) AS (
          SELECT A.al_gi_no, B.actvt_weight AS weight
          FROM monetc.gg_actvt A
          INNER JOIN CODE_ACTIVITY_WEIGHT B ON A.actvt_code = B.actvt_code
          WHERE al_gi_no IN (SELECT al_gi_no FROM mlresult.mf_gi_sim_am)
            AND m_id = {body.m_id!r}
            AND A.actvt_code IN (1, 2)
          ORDER BY actvt_dt DESC
          LIMIT 10 
        )

        SELECT
          {body.m_id!r} AS m_id
          , '최근 지원한 공고와 유사한 공고' AS story_title
          , AGI.gi_title
          , CNT.am_clickacum_cnt
          , CNT.am_applyacum_cnt
          , T.score
          , concat('https://www.albamon.com/recruit/view/gi?AL_GI_No=', cast(T.gno AS VARCHAR)) AS url
        FROM (
          -- outputs
          SELECT
            al_gi_no_similar AS gno
            , CAST(101 - ROW_NUMBER() OVER (ORDER BY sum(score * weight) DESC) AS DOUBLE) / 100 AS score
          FROM mlresult.mf_gi_sim_am A
          INNER JOIN USER_HISTORY B ON A.al_gi_no = B.al_gi_no
          GROUP BY al_gi_no_similar
          ORDER BY score DESC
          LIMIT 100
        ) T
        LEFT JOIN (SELECT al_gi_no as gno, subject as gi_title FROM mongi.mon_guin_db WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
        LEFT JOIN (SELECT al_gi_no as gno, am_clickacum_cnt, am_applyacum_cnt FROM mldata.profile_am_recruit) CNT ON T.gno = CNT.gno
        ORDER BY T.score DESC
        """

    elif body.story_number == 98:
        query = f"""
        WITH
        CODE_ACTIVITY_WEIGHT(actvt_code, actvt_weight) AS (
          VALUES (1, 0.6), (2, 0.5), (3, 0.4), (4, 0.3), (5, 0.2)
        ),
        USER_HISTORY(al_gi_no, weight) AS (
          SELECT A.al_gi_no, B.actvt_weight AS weight
          FROM monetc.gg_actvt A
          INNER JOIN CODE_ACTIVITY_WEIGHT B ON A.actvt_code = B.actvt_code
          WHERE al_gi_no IN (SELECT al_gi_no FROM mlresult.mf_gi_sim_am)
            AND m_id = {body.m_id!r}
            AND A.actvt_code = 3
          ORDER BY actvt_dt DESC
          LIMIT 10 
        )

        SELECT
          {body.m_id!r} AS m_id
          , '최근 스크랩한 공고와 유사한 공고' AS story_title
          , AGI.gi_title
          , CNT.am_clickacum_cnt
          , CNT.am_applyacum_cnt
          , T.score
          , concat('https://www.albamon.com/recruit/view/gi?AL_GI_No=', cast(T.gno AS VARCHAR)) AS url
        FROM (
          -- outputs
          SELECT
            al_gi_no_similar AS gno
            , CAST(101 - ROW_NUMBER() OVER (ORDER BY sum(score * weight) DESC) AS DOUBLE) / 100 AS score
          FROM mlresult.mf_gi_sim_am A
          INNER JOIN USER_HISTORY B ON A.al_gi_no = B.al_gi_no
          GROUP BY al_gi_no_similar
          ORDER BY score DESC
          LIMIT 100
        ) T
        LEFT JOIN (SELECT al_gi_no as gno, subject as gi_title FROM mongi.mon_guin_db WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
        LEFT JOIN (SELECT al_gi_no as gno, am_clickacum_cnt, am_applyacum_cnt FROM mldata.profile_am_recruit) CNT ON T.gno = CNT.gno
        ORDER BY T.score DESC
        """

    else:
        query = f"""
        with USERFILTER as (
            SELECT A.m_id, t.location_code
            FROM {db_name}.user_profile as A
              cross join UNNEST(split(location_code, ',')) as t(location_code)
            where m_id={body.m_id!r}
        ),
        
        LOCATION as (
          --gu code
        select m_id, location_code
        from (
          select m_id, location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.gu_code=B.location_code
          
          union all
          --convert from si_code to gu_codes
          select m_id, gu_code as location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.si_code=B.location_code
        
          union all
          --convert from gu_code to si_code
          select m_id, si_code as location_code
          from USERFILTER as B
          inner join mongi.AL_Area_Code as C
          on C.gu_code=B.location_code
          )
        group by m_id,location_code
        )
        
        SELECT
        T.m_id
        , (SELECT story_title FROM {db_name}.story_table WHERE story_no = {body.story_number}) AS story_title
        , AGI.gi_title
        , CODE.local_name
        , T.score
        , CNT.am_clickacum_cnt
        , CNT.am_applyacum_cnt
        , concat('https://www.albamon.com/recruit/view/gi?AL_GI_No=', cast(T.gno AS VARCHAR)) AS url
        FROM (  select A.m_id,B.gno, B.location_code, sum(score) as score
                from LOCATION as A
                inner join {db_name}.story_{body.story_number} as B
                on A.location_code=B.location_code
                group by (m_id,gno,B.location_code)
                ORDER BY score DESC LIMIT 200
              ) as T
          LEFT JOIN (SELECT al_gi_no as gno, subject as gi_title FROM mongi.mon_guin_db WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
          LEFT JOIN (select local_code, local_name from job_db30_gi.code_local) CODE ON T.location_code = CODE.local_code
          LEFT JOIN (SELECT al_gi_no as gno, am_clickacum_cnt, am_applyacum_cnt FROM mldata.profile_am_recruit) CNT ON T.gno = CNT.gno
        ORDER BY T.score DESC        

        """

    # data = JSF(ResultByStoryUserOutput.schema()).generate(3)
    data = PrestoExecutor.execute(query, include_rowid=True)
    return data


@router.post("/result_user_profile", tags=[tag], response_model=List[ResultUserProfile], description="유저별 스토리 및 속성 조회")
async def handler_result_user_profile():
    query = f"""
        select A.m_id,cardinality(array_agg(CODE.local_name)) as location_count ,
               array_join(array_distinct(array_agg(cast(A.story_number as VARCHAR))),',') as story_number,
               array_join( array_agg(CODE.local_name),',') as location_name ,
               array_join(array_agg(CODE.local_code),',') as location_code
        from {db_name}.user_profile as A
        cross join unnest(split(A.location_code,',')) as t(location_code)
        LEFT JOIN (select local_code, local_name from job_db30_gi.code_local) CODE ON t.location_code = CODE.local_code
        group by m_id
        order by location_count desc
        LIMIT 10000
        """
    # data = JSF(ResultUserProfile.schema()).generate(3)
    data = PrestoExecutor.execute(query, include_rowid=True)
    return data

