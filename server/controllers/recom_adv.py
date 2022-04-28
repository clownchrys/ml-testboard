import os
from typing import List
from fastapi import APIRouter
from jsf import JSF

from models.recom_adv import (
    ResultByUserStoryInput, ResultByStoryUserOutput,
    ResultUserProfile,
)
# from queries.recom_renewal import (
#     query_result_by_id,
#     query_result_by_gno,
#     query_get_users,
#     query_monitor_model_by_bz,
#     query_monitor_result_by_bz
# )
from connections import PrestoExecutor

router = APIRouter()
tag = os.path.basename(__file__)


@router.post("/result_by_user_story", tags=[tag], response_model=List[ResultByStoryUserOutput], description="유저별 검증")
async def handler_result_by_user_story(body: ResultByUserStoryInput):
    # tagging
    tag = ""
    if body.story_number in (89, 54, 55, 56, 57, 83):  # using jk_jobtitle_code
        tag = "jk_jobtitle_code"
    elif body.story_number in (41, 45, 61, 62, 46, 47):  # using jk_latestjobtitle_code
        tag = "jk_latestjobtitle_code"
    elif body.story_number in (79, 80, 81):  # using statistically
        tag = "statistic"

    # make query
    if tag == "jk_jobtitle_code":
        query = f"""
        SELECT
            T.m_id
            , AGI.gi_title
            , CODE.bizjobtype_name
            , T.total_score
            , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(T.gno AS VARCHAR)) AS url
        FROM (
            SELECT A.m_id, B.*
            FROM mlresult.story_recom_user_profile A
            INNER JOIN mlresult.story_{body.story_number} B ON split(A.jk_jobtitle_code, ',')[1] = cast(B.jk_jobtitle_code AS VARCHAR)
            WHERE m_id = {body.m_id!r}
        ) T
        LEFT JOIN (SELECT gno, gi_title FROM job_db30_gi.agi WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
        LEFT JOIN (SELECT bizjobtype_code, bizjobtype_name FROM job_db30_gi.code_bizjobtype) CODE ON T.jk_jobtitle_code = CODE.bizjobtype_code
        ORDER BY T.total_score DESC
        LIMIT 100
        """

    elif tag == "jk_latestjobtitle_code":
        query = f"""
        SELECT
            T.m_id
            , AGI.gi_title
            , CODE.bizjobtype_name
            , T.total_score
            , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(T.gno AS VARCHAR)) AS url
        FROM (
            SELECT A.m_id, B.*
            FROM mlresult.story_recom_user_profile A
            INNER JOIN mlresult.story_{body.story_number} B ON A.jk_latestjobtitle_code = cast(B.jk_jobtitle_code AS VARCHAR)
            WHERE m_id = {body.m_id!r}
        ) T
        LEFT JOIN (SELECT gno, gi_title FROM job_db30_gi.agi WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
        LEFT JOIN (SELECT bizjobtype_code, bizjobtype_name FROM job_db30_gi.code_bizjobtype) CODE ON T.jk_jobtitle_code = CODE.bizjobtype_code
        ORDER BY T.total_score DESC
        LIMIT 100
        """

    elif tag == "statistical":
        query = f"""
        SELECT
            T.m_id
            , AGI.gi_title
            , T.total_score
            , concat('https://www.jobkorea.co.kr/Recruit/GI_Read/', cast(T.gno AS VARCHAR)) AS url
        FROM (
            SELECT {body.m_id!r} AS m_id, *
            FROM mlresult.story_{body.story_number}
        ) T
        LEFT JOIN (SELECT gno, gi_title FROM job_db30_gi.agi WHERE year IN (2021, 2022)) AGI ON T.gno = AGI.gno
        LEFT JOIN (SELECT bizjobtype_code, bizjobtype_name FROM job_db30_gi.code_bizjobtype) CODE ON T.jk_jobtitle_code = CODE.bizjobtype_code
        ORDER BY T.total_score DESC
        LIMIT 100
        """

    else:
        return JSF(ResultByStoryUserOutput.schema()).generate(3)

    data = PrestoExecutor.execute(query, include_rowid=True)
    return data


@router.post("/result_user_profile", tags=[tag], response_model=List[ResultUserProfile], description="유저별 스토리 및 속성 조회")
async def handler_result_user_profile():
    # data = JSF(ResultUserProfile.schema()).generate(3)
    data = PrestoExecutor.execute("SELECT * FROM mlresult.story_recom_user_profile", include_rowid=True)
    return data
