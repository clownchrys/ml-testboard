from pydantic import BaseModel


class BaseModelWithRowid(BaseModel):
    rowid: int
