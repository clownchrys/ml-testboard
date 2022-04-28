from typing import Optional

from models import BaseModel, BaseModelWithRowid


class ResultByIdInput(BaseModel):
    uid: str


class ResultByIdOutput(BaseModelWithRowid):
    uid: str
    cont_no: int
    tag_type: Optional[int]
    tag_name: Optional[str]
    activity_count: int
    score: Optional[float]
    url: str
    sort_idx: int


class GetUsersOutput(BaseModelWithRowid):
    uid: str
    activity_count: int

