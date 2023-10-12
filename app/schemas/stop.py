from pydantic import BaseModel


class StopBase(BaseModel):
    stop_name: str


class StopCreate(StopBase):
    pass


class Stop(StopBase):
    id: int
    town_id: int


class StopInDB(Stop):
    pass
