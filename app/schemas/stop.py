from pydantic import BaseModel

from app.schemas.run_stop import RunStop


class StopBase(BaseModel):
    stop_name: str


class StopCreate(StopBase):
    pass


class Stop(StopBase):
    id: int
    town_id: int


class StopInDB(Stop):
    run_stops: list[RunStop] = []
