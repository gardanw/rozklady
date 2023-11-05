from datetime import time
from typing import Union

from pydantic import BaseModel


class RunStopBase(BaseModel):
    arrival_time: time
    depart_time: time


class RunStopCreate(RunStopBase):
    stop: Union[int, str]
    town: Union[int, str] = None


class RunStop(RunStopBase):
    id: int
    run_id: int
    stop_id: int


class RunStopInDB(RunStop):
    pass
