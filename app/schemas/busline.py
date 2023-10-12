from pydantic import BaseModel

from app.schemas.run import Run


class BuslineBase(BaseModel):
    busline_name: str
    busline_return: bool


class BuslineCreate(BuslineBase):
    pass


class Busline(BuslineBase):
    id: int
    runs: list[Run] = []


class BuslineInDB(Busline):
    pass
