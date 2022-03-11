from pydantic import BaseModel

from models import BaseModelWithRowid


class TestBody(BaseModel):
    value: str


class TestModel(BaseModelWithRowid):
    id: int
    value: str
