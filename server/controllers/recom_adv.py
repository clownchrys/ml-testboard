import os
from typing import List
from fastapi import APIRouter
from jsf import JSF

from models.recom_adv import (
    ResultByUserStoryInput, ResultByStoryUserOutput,
    ResultByGuestStoryInput, ResultByStoryGuestOutput,
    ResultUserProfile,
)
from connections import PrestoExecutor

router = APIRouter()
tag = os.path.basename(__file__)


@router.post("/result_by_user_story", tags=[tag], response_model=List[ResultByStoryUserOutput], description="유저별 검증")
async def handler_result_by_user_story(body: ResultByUserStoryInput):
    # make query
    # 공고형
    if body.story_number in (45, 61, 62, 46, 47, 89, 54, 55, 56, 57):
        query = f"""
        SELECT DISTINCT
            T.m_id
            , (SELECT story_title FROM user_story_staging.story_table_df WHERE story_number = {body.story_number}) AS story_title
            , T.gno
            , AGI.gi_title
            , ARRAY_JOIN(T.abn_bizjobtype_name, ' / ') AS abn_bizjobtype_name
            , ARRAY_JOIN(T.job_bizjobtype_name, ' / ') AS job_bizjobtype_name
            , ARRAY_JOIN(T.jk_jobtitle_name, ' / ') AS jk_jobtitle_name
            , T.recom_score
            , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(T.gno AS VARCHAR)) AS url
        FROM (
            SELECT *
            FROM user_story_staging.qe_user_profile A
            INNER JOIN user_story_staging.story_{body.story_number} B ON B.jk_jobtitle_code = A.jk_jobtitle_code
            WHERE m_id = {body.m_id!r}
            ) T
            
        LEFT JOIN (SELECT gno, gi_title FROM job_db30_gi.AGI WHERE year in (2021,2022)) AGI ON T.gno = AGI.gno
        ORDER BY T.recom_score DESC 
        LIMIT 100
        """

    # 통계형
    elif body.story_number in (79, 80, 81):
        query = f"""
        SELECT DISTINCT
            (SELECT story_title FROM user_story_staging.story_table_df WHERE story_number = {body.story_number}) AS story_title
            , T.gno
            , AGI.gi_title
            , T.recom_score
            , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(T.gno AS VARCHAR)) AS url
        FROM user_story_staging.story_{body.story_number} T
        LEFT JOIN (SELECT gno, gi_title FROM job_db30_gi.AGI WHERE year in (2021,2022)) AGI ON AGI.gno = T.gno
        ORDER BY T.recom_score DESC
        LIMIT 100
        """

    # 행동기반
#    elif body.story_number in (79, 80, 81):
#        query = f"""
#        SELECT
#            (SELECT story_title FROM user_story_staging.story_table_df WHERE story_number = {body.story_number}) AS story_title
#            , T.gno
#            , AGI.gi_title
#            , T.recom_score
#            , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(T.gno AS VARCHAR)) AS url
#        FROM user_story_staging.story_{body.story_number} T
#        LEFT JOIN (SELECT gno, gi_title FROM job_db30_gi.AGI WHERE year in (2021,2022)) AGI ON AGI.gno = T.gno
#        ORDER BY T.recom_score DESC
#        LIMIT 100
#        """

    else:
        return JSF(ResultByStoryUserOutput.schema()).generate(3)

    data = PrestoExecutor.execute(query, include_rowid=True)
    return data


@router.post("/result_user_profile", tags=[tag], response_model=List[ResultUserProfile], description="유저별 스토리 및 속성 조회")
async def handler_result_user_profile():
    query = """
        SELECT DISTINCT
          A.m_id
          , story_number
          , ARRAY_JOIN(C.abn_bizjobtype_name, ' / ') AS abn_bizjobtype_name
          , ARRAY_JOIN(C.job_bizjobtype_name, ' / ') AS job_bizjobtype_name
          , ARRAY_JOIN(C.jk_jobtitle_name, ' / ') AS jk_jobtitle_name
        FROM user_story_staging.user_profile A
        LEFT JOIN user_story_staging.qe_user_profile C ON A.m_id = C.m_id
        LIMIT 10000
        """

    # data = JSF(ResultUserProfile.schema()).generate(3)
    data = PrestoExecutor.execute(query, include_rowid=True)
    return data


@router.post("/result_user_profile", tags=[tag], response_model=List[ResultUserProfile], description="유저별 스토리 및 속성 조회")
async def handler_result_user_profile():
    query = """
        SELECT DISTINCT
          A.m_id
          , story_number
          , C.abn_bizjobtype_name
          , C.job_bizjobtype_name
          , C.jk_jobtitle_name
        FROM user_story_staging.user_profile A
        LEFT JOIN JOB_DB30_GI.Code_BizJobType B ON A.jk_jobtitle_code = B.BizJobType_Code
        LEFT JOIN user_story_staging.qe_user_profile C ON A.m_id = C.m_id
        LIMIT 10000
        """

    # data = JSF(ResultUserProfile.schema()).generate(3)
    data = PrestoExecutor.execute(query, include_rowid=True)
    return data


@router.post("/result_by_guest_story", tags=[tag], response_model=List[ResultByStoryGuestOutput], description="비로그인 유저별 검증")
async def handler_result_by_guest_story(body: ResultByGuestStoryInput):
    # make query
    # 공고형
    if body.story_number in (45, 61, 62, 46, 47, 89, 54, 55, 56, 57):
        query = f"""
        SELECT DISTINCT
            (SELECT story_title FROM user_story_staging.story_table_df WHERE story_number = {body.story_number}) AS story_title
            , T.gno
            , AGI.gi_title
            --, B.BizJobType_Name AS AGI_BizJobType_Name
            , T.recom_score
            , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(T.gno AS VARCHAR)) AS url
        FROM user_story_staging.story_{body.story_number} T
        LEFT JOIN (SELECT gno, gi_title FROM job_db30_gi.AGI WHERE year in (2021,2022)) AGI ON AGI.gno = T.gno
        --LEFT JOIN JOB_DB30_GI.Code_BizJobType B ON T.jk_jobtitle_code = B.BizJobType_Code
        ORDER BY T.recom_score DESC
        LIMIT 100
        """

    # 통계형
    elif body.story_number in (79, 80, 81):
        query = f"""
        SELECT DISTINCT
            (SELECT story_title FROM user_story_staging.story_table_df WHERE story_number = {body.story_number}) AS story_title
            , T.gno
            , AGI.gi_title
            , T.recom_score
            , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(T.gno AS VARCHAR)) AS url
        FROM user_story_staging.story_{body.story_number} T
        LEFT JOIN (SELECT gno, gi_title FROM job_db30_gi.AGI WHERE year in (2021,2022)) AGI ON AGI.gno = T.gno
        ORDER BY T.recom_score DESC
        LIMIT 100
        """

    else:
        return JSF(ResultByStoryGuestOutput.schema()).generate(3)

    data = PrestoExecutor.execute(query, include_rowid=True)
    return data

