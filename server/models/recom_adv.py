from typing import Optional, Union, List

from models import BaseModel, BaseModelWithRowid


class ResultByUserStoryInput(BaseModel):
    m_id: str
    story_number: int

class ResultByGuestStoryInput(BaseModel):
    story_number: int


class ResultByStoryUserOutput(BaseModelWithRowid):
    m_id: Optional[str]
    story_title: str
    gno: int
    gi_title: Optional[str]
    abn_bizjobtype_name: Optional[str]
    job_bizjobtype_name: Optional[str]
    jk_jobtitle_name: Optional[str]
    recom_score: Optional[float]
    url: Optional[str]


class ResultByStoryGuestOutput(BaseModelWithRowid):
    story_title: str
    gno: int
    gi_title: Optional[str]
    #AGI_BizJobType_Name: Optional[str]
    recom_score: Optional[float]
    url: Optional[str]


class ResultUserProfile(BaseModelWithRowid):
    m_id: str
    abn_bizjobtype_name: Optional[str]
    job_bizjobtype_name: Optional[str]
    jk_jobtitle_name: Optional[str]

