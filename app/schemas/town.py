from pydantic import BaseModel


class TownBase(BaseModel):
    town_name: str


class TownCreate(TownBase):
    pass


class Town(TownBase):
    id: int


class TownInDB(Town):
    pass
