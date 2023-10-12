from datetime import time

from pydantic import BaseModel


class RunStopBase(BaseModel):
    arrival_time: time
    depart_time: time
    stop_id: int


class RunStopCreate(RunStopBase):
    pass


class RunStop(RunStopBase):
    id: int
    run_id: int


class RunStopInDB(RunStop):
    pass
