from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
import app.schemas


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/towns/", response_model=app.schemas.Town)
async def create_town(town: app.schemas.TownCreate, db: Session = Depends(get_db)):
    db_town = crud.get_town_by_name(db, name=town.town_name)
    if db_town:
        raise HTTPException(status_code=400, detail="Town already registered")
    return crud.create_town(db=db, town=town)


@router.get("/towns/")
async def add_town_html(request: Request, db: Session = Depends(get_db)):
    db_towns = crud.get_towns(db=db)
    return templates.TemplateResponse(
        "town.html", {"request": request, "towns": db_towns}
    )


@router.get("/towns/{town_id}", response_model=app.schemas.Town)
async def read_town(town_id, db: Session = Depends(get_db)):
    db_town = crud.get_town(db, town_id=town_id)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return db_town


@router.post("/towns/{town_id}/stops/", response_model=app.schemas.Stop)
async def create_stop(
    town_id: int, stop: app.schemas.StopCreate, db: Session = Depends(get_db)
):
    db_town = crud.get_town(db, town_id=town_id)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    db_town_stops = crud.get_town_stops(db=db, town_id=town_id)
    if any(map(lambda x: x.stop_name == stop.stop_name, db_town_stops)):
        raise HTTPException(status_code=400, detail="Stop already in Town")
    return crud.create_stop(db=db, stop=stop, town_id=town_id)


@router.get("/towns/{town_id}/stops/", response_model=list[app.schemas.Stop])
async def read_town_stops(town_id: int, db: Session = Depends(get_db)):
    db_town = crud.get_town(db=db, town_id=town_id)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    stops = crud.get_town_stops(db=db, town_id=town_id)
    return stops


@router.post("/buslines/", response_model=app.schemas.Busline)
async def create_busline(
    busline: app.schemas.BuslineCreate, db: Session = Depends(get_db)
):
    return crud.create_busline(db=db, busline=busline)


@router.post("/buslines/{busline_id}/runs/", response_model=app.schemas.Run)
async def create_run(
    busline_id: int, run: app.schemas.RunCreate, db: Session = Depends(get_db)
):
    db_busline = crud.get_buslien(db=db, busline_id=busline_id)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    return crud.create_run(db=db, run=run, busline_id=busline_id)


@router.post("/buslines/{busline_id}/runs/{run_id}", response_model=app.schemas.RunStop)
async def create_run(
    busline_id: int,
    run_id: int,
    run_stop: app.schemas.RunStopCreate,
    db: Session = Depends(get_db),
):
    db_busline = crud.get_buslien(db=db, busline_id=busline_id)
    if db_busline is None:
        raise HTTPException(status_code=404, detail="Busline not found")
    db_run = crud.get_run(db=db, run_id=run_id)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    db_stop = crud.get_stop(db=db, stop_id=run_stop.stop_id)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return crud.create_run_stop(db=db, run_stop=run_stop, run_id=run_id)
