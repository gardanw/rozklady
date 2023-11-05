from pydantic import BaseModel

from app.schemas.run_stop import RunStopInDB, RunStopCreate


class RunBase(BaseModel):
    descript: str


class RunCreate(RunBase):
    run_stops: list[RunStopCreate] = None


class Run(RunBase):
    id: int
    busline_id: int


class RunInDB(Run):
    run_stops: list[RunStopInDB] = []
