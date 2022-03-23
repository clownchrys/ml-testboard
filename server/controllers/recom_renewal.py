import os
from typing import List
from fastapi import APIRouter
from jsf import JSF

from models.recom_renewal import (
    ResultByIdInput, ResultByIdOutput,
    ResultByGnoInput, ResultByGnoOutput,
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
    query = query_result_by_id.func(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(ResultByIdOutput.schema()).generate(3)
    return data


@router.post("/result_by_gno", tags=[tag], response_model=List[ResultByGnoOutput], description="공고별 검증")
async def handler_result_by_gno(body: List[ResultByGnoInput]):
    query = query_result_by_gno.func(body)
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(ResultByGnoOutput.schema()).generate(3)
    return data


@router.post("/get_users", tags=[tag], response_model=List[GetUsersOutput], description="추천 가능한 유저 목록 조회")
async def handler_get_users():
    query = query_get_users.string
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(GetUsersOutput.schema()).generate(3)
    return data


@router.post("/monitor_model_by_bz", tags=[tag], response_model=List[MonitorModelByBzOutput], description="직무 산업별 모델 출력 조회")
async def handler_monitor_model_by_bz():
    query = query_monitor_model_by_bz.string
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(MonitorModelByBzOutput.schema()).generate(3)
    return data


@router.post("/monitor_result_by_bz", tags=[tag], response_model=List[MonitorResultByBzOutput], description="직무 산업별 추천 결과 조회")
async def handler_monitor_result_by_bz():
    query = query_monitor_result_by_bz.string
    data = PrestoExecutor.execute(query, include_rowid=True)
    # data = JSF(MonitorResultByBzOutput.schema()).generate(3)
    return data
