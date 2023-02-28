from models import BaseModel


class ShowProfileInput(BaseModel):
    dbType: str
    profileType: str
    keyColName: str
    keyColValue: str
