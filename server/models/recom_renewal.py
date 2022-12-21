from typing import Optional

from models import BaseModel, BaseModelWithRowid


class EnvInput(BaseModel):
    env: Optional[str]


class ResultByIdInput(EnvInput, BaseModel):
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
    score: Optional[float]
    TITLE: Optional[str]
    BZT_1: Optional[str]
    BZT_2: Optional[str]
    LOCAL_1: Optional[str]
    LOCAL_2: Optional[str]
    IS_PAID: Optional[str]
    URL: Optional[str]


class GetUsersOutput(BaseModelWithRowid):
    m_id: str


class MonitorModelByBzOutput(BaseModelWithRowid):
    gno: int
    recom_gno: int
    score: float
    title: Optional[str]
    title_recom: Optional[str]
    BZT_1: Optional[str]
    BZT_2: Optional[str]
    LOCAL_1: Optional[str]
    LOCAL_2: Optional[str]


class MonitorResultByBzOutput(BaseModelWithRowid):
    m_id: str
    bizjobtype_bctgr_name: Optional[str]
    bizjobtype_name: Optional[str]


class ResultModelByGnoInput(BaseModel):
    env: str
    gno: int


class ResultModelByGnoOutput(BaseModelWithRowid):
    gno: int
    gi_title: Optional[str]
    jobname: Optional[str]
    score: float
    link: str
