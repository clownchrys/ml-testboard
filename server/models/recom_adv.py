from typing import Optional, Union

from models import BaseModel, BaseModelWithRowid


class ResultByUserStoryInput(BaseModel):
    m_id: str
    story_number: int


class ResultByStoryUserOutput(BaseModelWithRowid):
    m_id: str
    story_title: str
    gi_title: Optional[str]
    bizjobtype_name: Optional[str]
    total_score: Optional[float]
    url: str


class ResultUserProfile(BaseModelWithRowid):
    m_id: str
    story_number: str
    jk_latestjobtitle_code: Optional[str]
    jk_jobtitle_code: Optional[str]
    jk_latestjobtitle_name: Optional[str]
    jk_jobtitle_name: Optional[str]

