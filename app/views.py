from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.schemas
from app import crud
from app.database import get_db
from app.utils import get_town_by_param

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
    return created_stops


@router.get("/towns/{town}/stops/", response_model=list[app.schemas.Stop])
async def read_town_stops(town: Union[int, str], db: Session = Depends(get_db)):
    db_town = get_town_by_param(db=db, town=town)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    stops = db_town.stops
    return stops


@router.get("/stops/{stop_id}", response_model=app.schemas.StopInDB)
async def read_stop(stop_id: int, db: Session = Depends(get_db)):
    db_stop = crud.get_stop(db=db, stop_id=stop_id)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return db_stop


@router.delete("/stops/{stop_id}", response_model=app.schemas.StopInDB)
async def del_stop(stop_id: int, db: Session = Depends(get_db)):
    db_stop = crud.get_stop(db=db, stop_id=stop_id)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return crud.del_stop(db, stop=db_stop)


@router.put("/stops/{stop_id}", response_model=app.schemas.StopInDB)
async def edit_stop_name(
    stop_id: int, stop: app.schemas.StopBase, db: Session = Depends(get_db)
):
    db_stop = crud.get_stop(db=db, stop_id=stop_id)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return crud.update_stop_name(db, stop=db_stop, new_name=stop.stop_name)


@router.post("/buslines/", response_model=app.schemas.Busline)
async def create_busline(
    busline: app.schemas.BuslineCreate, db: Session = Depends(get_db)
):
    busline_db = crud.get_busline_by_name_and_direction(
        db, name=busline.busline_name, ret=busline.busline_return
    )
    if busline_db:
        raise HTTPException(status_code=400, detail="Busline already registered")
    return crud.create_busline(db=db, busline=busline)


@router.get("/buslines/", response_model=list[app.schemas.BuslineInDB])
async def read_buslines(db: Session = Depends(get_db)):
    db_buslines = crud.get_buslines(db=db)
    return db_buslines


@router.get("/buslines/{busline_id}", response_model=app.schemas.BuslineInDB)
async def read_busline(busline_id: int, db: Session = Depends(get_db)):
    db_busline = crud.get_busline(db, busline_id=busline_id)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return db_busline


@router.delete("/buslines/{busline_id}", response_model=app.schemas.BuslineInDB)
async def del_busline(busline_id: int, db: Session = Depends(get_db)):
    db_busline = crud.get_busline(db, busline_id=busline_id)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return crud.del_busline(db, busline=db_busline)


@router.put("/buslines/{busline_id}", response_model=app.schemas.BuslineInDB)
async def edit_busline(
    busline_id: int, busline: app.schemas.BuslineBase, db: Session = Depends(get_db)
):
    db_busline = crud.get_busline(db, busline_id=busline_id)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return crud.update_busline(
        db,
        busline=db_busline,
        new_name=busline.busline_name,
        ret=busline.busline_return,
    )


@router.post("/buslines/{busline_id}/runs/", response_model=app.schemas.Run)
async def create_busline_run(
    busline_id: int, run: app.schemas.RunCreate, db: Session = Depends(get_db)
):
    db_busline = crud.get_busline(db=db, busline_id=busline_id)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return crud.create_run(db=db, run=run, busline_id=busline_id)


@router.get("/buslines/{busline_id}/runs/", response_model=list[app.schemas.RunInDB])
async def read_busline_runs(busline_id: int, db: Session = Depends(get_db)):
    db_busline = crud.get_busline(db=db, busline_id=busline_id)
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


@router.post("/runs/{run_id}/run_stops", response_model=app.schemas.RunStop)
async def create_run_stop(
    run_id: int,
    run_stop: app.schemas.RunStopCreate,
    db: Session = Depends(get_db),
):
    db_run = crud.get_run(db=db, run_id=run_id)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    db_stop = crud.get_stop(db=db, stop_id=run_stop.stop_id)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return crud.create_run_stop(db=db, run_stop=run_stop, run_id=run_id)


@router.get("/runs/{run_id}/run_stops", response_model=list[app.schemas.RunStopInDB])
async def read_run_run_stops(run_id: int, db: Session = Depends(get_db)):
    db_run = crud.get_run(db=db, run_id=run_id)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return db_run.run_stops


@router.get("/stops/{stop_id}/run_stops", response_model=list[app.schemas.RunStopInDB])
async def read_stop_run_stops(stop_id: int, db: Session = Depends(get_db)):
    db_stop = crud.get_stop(db=db, stop_id=stop_id)
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
