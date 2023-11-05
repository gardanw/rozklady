from pydantic import BaseModel

from app.schemas.stop import StopInDB, StopCreate


class TownBase(BaseModel):
    town_name: str


class TownCreate(TownBase):
    stops: list[StopCreate] = None


class Town(TownBase):
    id: int


class TownInDB(Town):
    stops: list[StopInDB] = []
