from pydantic import BaseModel

from app.schemas.run import RunInDB, RunCreate


class BuslineBase(BaseModel):
    busline_name: str
    busline_return: bool


class BuslineCreate(BuslineBase):
    runs: list[RunCreate] = None


class Busline(BuslineBase):
    id: int


class BuslineInDB(Busline):
    runs: list[RunInDB] = []
