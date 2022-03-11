from typing import Optional

from models import BaseModel, BaseModelWithRowid


class ResultByIdInput(BaseModel):
    m_id: str


class ResultByIdOutput(BaseModelWithRowid):
    kind: Optional[str]
    m_id: Optional[str]
    gno: Optional[int]
    actvt_code: Optional[str]
    is_include: Optional[str]
    dt: Optional[str]
    score: Optional[float]
    TITLE: Optional[str]
    BZT_1: Optional[str]
    BZT_2: Optional[str]
    LOCAL_1: Optional[str]
    LOCAL_2: Optional[str]
    IS_PAID: Optional[str]
    URL: Optional[str]


class ResultByGnoInput(BaseModel):
    gno: int
    actvt_code: int


class ResultByGnoOutput(BaseModelWithRowid):
    kind: Optional[str]
    gno: Optional[int]
    actvt_code: Optional[str]
    is_include: Optional[str]
    dt: Optional[str]
    score: Optional[int]
    TITLE: Optional[str]
    BZT_1: Optional[str]
    BZT_2: Optional[str]
    LOCAL_1: Optional[str]
    LOCAL_2: Optional[str]
    IS_PAID: Optional[str]
    URL: Optional[str]
