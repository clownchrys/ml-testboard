from typing import Optional, Union

from models import BaseModel, BaseModelWithRowid


class ResultByUserStoryInput(BaseModel):
    m_id: str
    story_number: int


class ResultByStoryUserOutput(BaseModelWithRowid):
    m_id: str
    story_title: str
    gi_title: Optional[str]
    local_name: Optional[str]
    partname: Optional[str]
    work_sdate: Optional[int]
    score: Optional[float]
    url: str
    am_clickacum_cnt: Optional[int]
    am_applyacum_cnt: Optional[int]


class ResultUserProfile(BaseModelWithRowid):
    m_id: str
    location_count: int
    story_number: str
    location_name: str
    location_code: str

