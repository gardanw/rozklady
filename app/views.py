from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.schemas
from app import crud
from app.database import get_db
from app.utils import get_town_by_param, get_stop_by_param, get_busline_by_param

router = APIRouter()


@router.post("/towns/", response_model=list[app.schemas.Town])
async def create_town(
    towns: Union[list[app.schemas.TownCreate], app.schemas.TownCreate],
    db: Session = Depends(get_db),
):
    if not isinstance(towns, list):
        towns = [towns]

    created_towns = []

    for town in towns:
        db_town = crud.get_town_by_name(db=db, name=town.town_name)
        if not db_town:
            created_town = crud.create_town(db=db, town=town)
            created_towns.append(created_town)
    return created_towns


@router.get("/towns/", response_model=list[app.schemas.TownInDB])
async def read_towns(db: Session = Depends(get_db)):
    db_towns = crud.get_towns(db=db)
    return db_towns


@router.get("/towns/{town}", response_model=app.schemas.TownInDB)
async def read_town(town: Union[str, int], db: Session = Depends(get_db)):
    db_town = get_town_by_param(db=db, town=town)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return db_town


@router.delete("/towns/{town}", response_model=app.schemas.TownInDB)
async def del_town(town: Union[int, str], db: Session = Depends(get_db)):
    db_town = get_town_by_param(db=db, town=town)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return crud.del_town(db=db, town=db_town)


@router.put("/towns/{town}", response_model=app.schemas.TownInDB)
async def edit_town_name(
    town: Union[int, str],
    temp_town: app.schemas.TownBase,
    db: Session = Depends(get_db),
):
    db_town = get_town_by_param(db=db, town=town)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return crud.update_town_name(db=db, town=db_town, new_name=temp_town.town_name)


@router.post("/towns/{town}/stops/", response_model=list[app.schemas.Stop])
async def create_town_stop(
    town: Union[int, str],
    stops: Union[list[app.schemas.StopCreate], app.schemas.StopCreate],
    db: Session = Depends(get_db),
):
    db_town = get_town_by_param(db=db, town=town)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")

    town_stops_name = [
        town_stop.stop_name
        for town_stop in crud.get_town_stops(db=db, town_id=db_town.id)
    ]

    if not isinstance(stops, list):
        stops = [stops]

    created_stops = []

    for stop in stops:
        if stop.stop_name not in town_stops_name:
            created_stop = crud.create_stop(db=db, stop=stop, town_id=db_town.id)
            created_stops.append(created_stop)
            town_stops_name.append(stop.stop_name)
    return created_stops


@router.get("/towns/{town}/stops/", response_model=list[app.schemas.Stop])
async def read_town_stops(town: Union[int, str], db: Session = Depends(get_db)):
    db_town = get_town_by_param(db=db, town=town)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    stops = db_town.stops
    return stops


@router.get("/stops/{stop}", response_model=app.schemas.StopInDB)
async def read_stop(
    stop: Union[int, str], town: Union[int, str] = "", db: Session = Depends(get_db)
):
    db_stop = get_stop_by_param(db=db, stop=stop, town=town)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return db_stop


@router.delete("/stops/{stop}", response_model=app.schemas.StopInDB)
async def del_stop(
    stop: Union[int, str], town: Union[int, str] = "", db: Session = Depends(get_db)
):
    db_stop = get_stop_by_param(db=db, stop=stop, town=town)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return crud.del_stop(db, stop=db_stop)


@router.put("/stops/{stop}", response_model=app.schemas.StopInDB)
async def edit_stop_name(
    stop: Union[int, str],
    temp_stop: app.schemas.StopBase,
    town: Union[int, str] = "",
    db: Session = Depends(get_db),
):
    db_stop = get_stop_by_param(db=db, stop=stop, town=town)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return crud.update_stop_name(db, stop=db_stop, new_name=temp_stop.stop_name)


@router.post("/buslines/", response_model=list[app.schemas.Busline])
async def create_busline(
    buslines: Union[list[app.schemas.BuslineCreate], app.schemas.BuslineCreate],
    db: Session = Depends(get_db),
):
    if not isinstance(buslines, list):
        buslines = [buslines]

    created_buslines = []

    for busline in buslines:
        busline_db = crud.get_busline_by_name_and_direction(
            db, name=busline.busline_name, ret=busline.busline_return
        )
        if not busline_db:
            created_busline = crud.create_busline(db=db, busline=busline)
            created_buslines.append(created_busline)
    return created_buslines


@router.get("/buslines/", response_model=list[app.schemas.BuslineInDB])
async def read_buslines(db: Session = Depends(get_db)):
    db_buslines = crud.get_buslines(db=db)
    return db_buslines


@router.get("/buslines/{busline}", response_model=app.schemas.BuslineInDB)
async def read_busline(
    busline: Union[int, str], ret: bool = None, db: Session = Depends(get_db)
):
    db_busline = get_busline_by_param(db=db, busline=busline, ret=ret)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return db_busline


@router.delete("/buslines/{busline}", response_model=app.schemas.BuslineInDB)
async def del_busline(
    busline: Union[int, str], ret: bool = None, db: Session = Depends(get_db)
):
    db_busline = get_busline_by_param(db=db, busline=busline, ret=ret)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return crud.del_busline(db, busline=db_busline)


@router.put("/buslines/{busline}", response_model=app.schemas.BuslineInDB)
async def edit_busline(
    busline: Union[int, str],
    temp_busline: app.schemas.BuslineBase,
    ret: bool = None,
    db: Session = Depends(get_db),
):
    db_busline = get_busline_by_param(db=db, busline=busline, ret=ret)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return crud.update_busline(
        db=db,
        busline=db_busline,
        new_name=temp_busline.busline_name,
        ret=temp_busline.busline_return,
    )


@router.post("/buslines/{busline}/runs/", response_model=list[app.schemas.Run])
async def create_busline_run(
    busline: Union[int, str],
    runs: Union[list[app.schemas.RunCreate], app.schemas.RunCreate],
    ret: bool = None,
    db: Session = Depends(get_db),
):
    db_busline = get_busline_by_param(db=db, busline=busline, ret=ret)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")

    if not isinstance(runs, list):
        runs = [runs]

    created_runs = []

    for run in runs:
        created_run = crud.create_run(db=db, run=run, busline_id=db_busline.id)
        created_runs.append(created_run)

    return created_runs


@router.get("/buslines/{busline}/runs/", response_model=list[app.schemas.RunInDB])
async def read_busline_runs(
    busline: Union[int, str], ret: bool = None, db: Session = Depends(get_db)
):
    db_busline = get_busline_by_param(db=db, busline=busline, ret=ret)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return db_busline.runs


@router.get("/runs/{run_id}", response_model=app.schemas.RunInDB)
async def read_run(run_id: int, db: Session = Depends(get_db)):
    db_run = crud.get_run(db=db, run_id=run_id)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return db_run


@router.delete("/runs/{run_id}/", response_model=app.schemas.RunInDB)
async def del_run(run_id: int, db: Session = Depends(get_db)):
    db_run = crud.get_run(db=db, run_id=run_id)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return crud.del_run(db, run=db_run)


@router.put("/runs/{run_id}", response_model=app.schemas.RunInDB)
async def edit_run_descript(
    run_id: int, run: app.schemas.RunBase, db: Session = Depends(get_db)
):
    db_run = crud.get_run(db=db, run_id=run_id)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return crud.update_run_descript(db, run=db_run, descript=run.descript)


@router.post("/runs/{run_id}/run_stops", response_model=list[app.schemas.RunStop])
async def create_run_stop(
    run_id: int,
    run_stops: Union[list[app.schemas.RunStopCreate], app.schemas.RunStopCreate],
    db: Session = Depends(get_db),
):
    db_run = crud.get_run(db=db, run_id=run_id)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    if not isinstance(run_stops, list):
        run_stops = [run_stops]

    created_run_stops = []

    for run_stop in run_stops:
        created_run_stop = crud.create_run_stop(
            db=db, run_stop=run_stop, run_id=db_run.id
        )
        created_run_stops.append(created_run_stop)
    return created_run_stops


@router.get("/runs/{run_id}/run_stops", response_model=list[app.schemas.RunStopInDB])
async def read_run_run_stops(run_id: int, db: Session = Depends(get_db)):
    db_run = crud.get_run(db=db, run_id=run_id)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return db_run.run_stops


@router.get("/stops/{stop}/run_stops", response_model=list[app.schemas.RunStopInDB])
async def read_stop_run_stops(
    stop: Union[int, str], town: Union[int, str] = "", db: Session = Depends(get_db)
):
    db_stop = get_stop_by_param(db=db, stop=stop, town=town)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return db_stop.run_stops


@router.get("/run_stops/", response_model=list[app.schemas.RunStopInDB])
async def read_run_stops(db: Session = Depends(get_db)):
    return crud.get_run_stops(db)


@router.get("/run_stops/{run_stop_id}", response_model=app.schemas.RunStopInDB)
async def read_run_stop(run_stop_id: int, db: Session = Depends(get_db)):
    db_run_stop = crud.get_run_stop(db, run_stop_id=run_stop_id)
    if db_run_stop is None:
        raise HTTPException(status_code=404, detail="Run Stop not found")
    return db_run_stop


@router.delete("/run_stops/{run_stop_id}", response_model=app.schemas.RunStopInDB)
async def del_run_stop(run_stop_id: int, db: Session = Depends(get_db)):
    db_run_stop = crud.get_run_stop(db, run_stop_id=run_stop_id)
    if db_run_stop is None:
        raise HTTPException(status_code=404, detail="Run Stop not found")
    return crud.del_run_stop(db, run_stop=db_run_stop)


@router.put("/run_stops/{run_stop_id}", response_model=app.schemas.RunStopInDB)
async def edit_run_stop_times(
    run_stop_id: int, run_stop: app.schemas.RunStopBase, db: Session = Depends(get_db)
):
    db_run_stop = crud.get_run_stop(db, run_stop_id=run_stop_id)
    if db_run_stop is None:
        raise HTTPException(status_code=404, detail="Run Stop not found")
    return crud.update_run_stop_times(
        db,
        run_stop=db_run_stop,
        arrival_time=run_stop.arrival_time,
        depart_time=run_stop.depart_time,
    )
