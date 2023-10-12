from pydantic import BaseModel

from app.schemas.stop import Stop


class TownBase(BaseModel):
    town_name: str


class TownCreate(TownBase):
    pass


class Town(TownBase):
    id: int
    stops: list[Stop] = []


class TownInDB(Town):
    pass
