import os
from typing import *

from fastapi import APIRouter
from jsf import JSF

from models.common import (
    ShowProfileInput,
)
from connections import PrestoExecutor

router = APIRouter()
tag = os.path.basename(__file__)


@router.post("/get_profile_data", tags=[tag], description="프로파일 데이터 조회")
async def handler_get_profile_data(body: ShowProfileInput):
    query = f"SELECT * FROM {body.dbType}.{body.profileType} WHERE {body.keyColName} = {body.keyColValue}"
    # print(query)
    # data = [
    #     { **body.__dict__, "string": "aaaaaaaaaaaaaaaaaaaa" * 10 }
    # ]
    data = PrestoExecutor.execute(query, include_rowid=False)
    return data
