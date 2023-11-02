from typing import Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.schemas import TownInDB
from app.settings import settings


def save_in_db(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)


def get_town_by_param(db: Session, town: Union[int, str]):
    db_town = None

    try:
        town = int(town)
    except ValueError as e:
        if settings.DEBUG:
            print(e, f"\ntown type: {type(town)}")

    if isinstance(town, int):
        db_town = crud.get_town(db=db, town_id=town)
    if isinstance(town, str):
        db_town = crud.get_town_by_name(db=db, name=town)
    return db_town


def get_town_stop(db: Session, stop: Union[int, str], town: TownInDB):
    db_stop = None

    try:
        stop = int(stop)
    except ValueError as e:
        if settings.DEBUG:
            print(e, f"\nstop type: {type(stop)}")

    if isinstance(stop, int):
        db_stop = crud.get_stop(db=db, stop_id=stop)
    if isinstance(stop, str):
        db_stop = next(
            (town_stop for town_stop in town.stops if town_stop.stop_name == stop), None
        )
    return db_stop


def get_stop_by_param(db: Session, stop: Union[str, int], town: Union[str, int]):
    if town:
        db_town = get_town_by_param(db=db, town=town)
        if db_town is None:
            raise HTTPException(status_code=404, detail="Town not found")
        db_stop = get_town_stop(db=db, stop=stop, town=db_town)
    else:
        try:
            stop_id = int(stop)
        except ValueError as e:
            if settings.DEBUG:
                print(e)
            raise HTTPException(status_code=400, detail="Town not specified")
        db_stop = crud.get_stop(db=db, stop_id=stop_id)
    return db_stop
