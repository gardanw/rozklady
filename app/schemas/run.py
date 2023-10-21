from pydantic import BaseModel

from app.schemas.run_stop import RunStop


class RunBase(BaseModel):
    descript: str


class RunCreate(RunBase):
    pass


class Run(RunBase):
    id: int
    busline_id: int


class RunInDB(Run):
    run_stops: list[RunStop] = []
