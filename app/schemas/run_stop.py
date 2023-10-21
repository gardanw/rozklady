from datetime import time

from pydantic import BaseModel


class RunStopBase(BaseModel):
    arrival_time: time
    depart_time: time


class RunStopCreate(RunStopBase):
    stop_id: int


class RunStop(RunStopBase):
    id: int
    run_id: int


class RunStopInDB(RunStop):
    pass
