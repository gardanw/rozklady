from pydantic import BaseModel

from app.schemas.stop import StopInDB


class TownBase(BaseModel):
    town_name: str


class TownCreate(TownBase):
    pass


class Town(TownBase):
    id: int


class TownInDB(Town):
    stops: list[StopInDB] = []
