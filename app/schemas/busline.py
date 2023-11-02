from pydantic import BaseModel

from app.schemas.run import RunInDB


class BuslineBase(BaseModel):
    busline_name: str
    busline_return: bool


class BuslineCreate(BuslineBase):
    pass


class Busline(BuslineBase):
    id: int


class BuslineInDB(Busline):
    runs: list[RunInDB] = []
