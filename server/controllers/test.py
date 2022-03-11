import os
from typing import List
from fastapi import APIRouter, status

from models.test import TestModel, TestBody
from connections import PrestoExecutor

router = APIRouter()
tag = os.path.basename(__file__)


@router.post("/path/{value}", tags=[tag], description="Path variable test")
async def test_path(value: int):
    return value


@router.post("/query", tags=[tag], description="Query variable test")
async def test_query(value: int):
    return value


@router.post("/body", tags=[tag], description="Body variable test")
async def test_body(value: TestBody):
    return value


@router.post("/status_code", tags=[tag], status_code=status.HTTP_307_TEMPORARY_REDIRECT, description="Status code test")
async def test_status_code():
    return "TEST_OK"


@router.post("/result", tags=[tag], response_model=List[TestModel], response_model_exclude_defaults=True)
async def test_result():
    test_data = [
        TestModel(id=1, value="a"),
        TestModel(id=2, value="b"),
        TestModel(id=3, value="c"),
    ]
    return test_data


@router.post("/show_table", tags=[tag])
async def test_show_table():
    query = "SHOW TABLES"
    return PrestoExecutor.execute(query, include_rowid=False)
