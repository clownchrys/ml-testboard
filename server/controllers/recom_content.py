import os
from typing import List
from fastapi import APIRouter
from jsf import JSF

from models.recom_content import (
    GetUsersOutput,
    ResultByIdInput, ResultByIdOutput,
)
from queries.recom_content import (
    query_get_active_users,
    query_get_passive_users,
    query_result_of_interview_review,
    query_result_of_job_interview,
    query_result_of_job_news,
    query_result_of_job_talk,
    query_result_of_passletter,
)
from connections import PrestoExecutor

router = APIRouter()
tag = os.path.basename(__file__)


@router.post("/result_of_interview_review", tags=[tag], response_model=List[ResultByIdOutput], description="면접후기 추천")
async def handler_result_of_interview_review(body: ResultByIdInput):
    query = query_result_of_interview_review.func(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = JSF(ResultByIdOutput.schema()).generate(3)
    return data


@router.post("/result_of_job_news", tags=[tag], response_model=List[ResultByIdOutput], description="취업뉴스 추천")
async def handler_result_of_job_news(body: ResultByIdInput):
    query = query_result_of_job_news.func(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = JSF(ResultByIdOutput.schema()).generate(3)
    return data


@router.post("/result_of_job_talk", tags=[tag], response_model=List[ResultByIdOutput], description="취업톡톡 추천")
async def handler_result_of_job_talk(body: ResultByIdInput):
    query = query_result_of_job_talk.func(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = JSF(ResultByIdOutput.schema()).generate(3)
    return data


@router.post("/result_of_passletter", tags=[tag], response_model=List[ResultByIdOutput], description="합격자소서 추천")
async def handler_result_of_passletter(body: ResultByIdInput):
    query = query_result_of_passletter.func(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = JSF(ResultByIdOutput.schema()).generate(3)
    return data


@router.post("/result_of_job_interview", tags=[tag], response_model=List[ResultByIdOutput], description="직무인터뷰 추천")
async def handler_result_of_job_interview(body: ResultByIdInput):
    query = query_result_of_job_interview.func(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = JSF(ResultByIdOutput.schema()).generate(3)
    return data


@router.post("/get_active_users", tags=[tag], response_model=List[GetUsersOutput], description="Active 유저 추출")
async def handler_get_active_users():
    query = query_get_active_users.string
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = JSF(GetUsersOutput.schema()).generate(3)
    return data


@router.post("/get_passive_users", tags=[tag], response_model=List[GetUsersOutput], description="Passive 유저 추출")
async def handler_get_passive_users():
    query = query_get_passive_users.string
    data = PrestoExecutor.execute(query, include_rowid=True)
    #data = JSF(GetUsersOutput.schema()).generate(3)
    return data


#@router.post("/monitor_model_by_bz", tags=[tag], response_model=List[MonitorModelByBzOutput], description="직무 산업별 모델 출력 조회")
#async def handler_monitor_model_by_bz():
#    query = query_monitor_model_by_bz.string
#    data = PrestoExecutor.execute(query, include_rowid=True)
#    # data = JSF(MonitorModelByBzOutput.schema()).generate(3)
#    return data
#
#
#@router.post("/monitor_result_by_bz", tags=[tag], response_model=List[MonitorResultByBzOutput], description="직무 산업별 추천 결과 조회")
#async def handler_monitor_result_by_bz():
#    query = query_monitor_result_by_bz.string
#    data = PrestoExecutor.execute(query, include_rowid=True)
#    # data = JSF(MonitorResultByBzOutput.schema()).generate(3)
#    return data
