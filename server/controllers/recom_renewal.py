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
    SELECT *
    FROM some_table
    WHERE m_id = { body.m_id }
    """
    # data = PrestoExecutor.execute(query, include_rowid=True)
    data = result_by_id
    return data


@router.post("/result_by_gno", tags=[tag], response_model=List[ResultByGnoOutput], description="공고별 검증")
async def get_result_by_gno(body: List[ResultByGnoInput]):
    query = f"""
    SELECT *
    FROM some_table
    WHERE 
    """
    # print(body)
    # data = PrestoExecutor.execute(query, include_rowid=True)
    data = result_by_gno
    return data
