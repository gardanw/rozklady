from sqlalchemy.orm import Session
from datetime import time


import app.models
import app.schemas


def save_in_db(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)


def create_town(db: Session, town: app.schemas.TownCreate) -> app.schemas.Town:
    db_town = app.models.Town(town_name=town.town_name)
    save_in_db(db=db, obj=db_town)
    return db_town


def get_town(db: Session, town_id: int) -> app.schemas.TownInDB:
    return db.query(app.models.Town).filter(app.models.Town.id == town_id).first()


def get_town_by_name(db: Session, name: str) -> app.schemas.TownInDB:
    return db.query(app.models.Town).filter(app.models.Town.town_name == name).first()


def get_towns(db: Session) -> list[app.schemas.TownInDB]:
    return db.query(app.models.Town).order_by(app.models.Town.town_name).all()


def update_town_name(
    db: Session, town: app.schemas.TownInDB, new_name: str
) -> app.schemas.TownInDB:
    town.town_name = new_name
    db.commit()
    return town


def del_town(db: Session, town: app.schemas.TownInDB) -> app.schemas.TownInDB:
    for stop in town.stops:
        del_stop(db, stop=stop)
    db.delete(town)
    db.commit()
    return town


def get_town_stops(db: Session, town_id: int) -> list[app.schemas.StopInDB]:
    return (
        db.query(app.models.Stop)
        .filter(app.models.Stop.town_id == town_id)
        .order_by(app.models.Stop.stop_name)
        .all()
    )


def create_stop(
    db: Session, stop: app.schemas.StopCreate, town_id: int
) -> app.schemas.Stop:
    db_stop = app.models.Stop(**stop.model_dump(), town_id=town_id)
    save_in_db(db=db, obj=db_stop)
    return db_stop


def get_stop(db: Session, stop_id: int) -> app.schemas.StopInDB:
    return db.query(app.models.Stop).filter(app.models.Stop.id == stop_id).first()


def update_stop_name(
    db: Session, stop: app.schemas.StopInDB, new_name: str
) -> app.schemas.StopInDB:
    stop.stop_name = new_name
    db.commit()
    return stop


def del_stop(db: Session, stop: app.schemas.StopInDB) -> app.schemas.StopInDB:
    for run_stop in stop.run_stops:
        del_run_stop(db, run_stop=run_stop)
    db.delete(stop)
    db.commit()
    return stop


def create_busline(
    db: Session, busline: app.schemas.BuslineCreate
) -> app.schemas.Busline:
    db_busline = app.models.Busline(**busline.model_dump())
    save_in_db(db=db, obj=db_busline)
    return db_busline


def get_busline(db: Session, busline_id: int) -> app.schemas.BuslineInDB:
    return (
        db.query(app.models.Busline).filter(app.models.Busline.id == busline_id).first()
    )


def get_busline_by_name_and_direction(
    db: Session, name: str, ret: bool
) -> app.schemas.BuslineInDB:
    return (
        db.query(app.models.Busline)
        .filter(app.models.Busline.busline_name == name)
        .filter(app.models.Busline.busline_return == ret)
        .first()
    )


def get_buslines(db: Session) -> list[app.schemas.BuslineInDB]:
    return db.query(app.models.Busline).order_by(app.models.Busline.busline_name).all()


def update_busline(
    db: Session, busline: app.schemas.BuslineInDB, new_name: str, ret: bool
) -> app.schemas.BuslineInDB:
    busline.busline_name = new_name
    busline.busline_return = ret
    db.commit()
    return busline


def del_busline(
    db: Session, busline: app.schemas.BuslineInDB
) -> app.schemas.BuslineInDB:
    for run in busline.runs:
        del_run(db, run=run)
    db.delete(busline)
    db.commit()
    return busline


def create_run(
    db: Session, run: app.schemas.RunCreate, busline_id: int
) -> app.schemas.Run:
    db_run = app.models.Run(**run.model_dump(), busline_id=busline_id)
    save_in_db(db=db, obj=db_run)
    return db_run


def get_run(db: Session, run_id: int) -> app.schemas.RunInDB:
    db_run = db.query(app.models.Run).filter(app.models.Run.id == run_id).first()
    return db_run


def get_busline_runs(db: Session, busline_id: int) -> list[app.schemas.RunInDB]:
    return (
        db.query(app.models.Run).filter(app.models.Run.busline_id == busline_id).all()
    )


def get_runs(db: Session) -> list[app.schemas.RunInDB]:
    return db.query(app.models.Run).order_by(app.models.busline_id).all()


def update_run_descript(
    db: Session, run: app.schemas.RunInDB, descript: str
) -> app.schemas.RunInDB:
    run.descript = descript
    db.commit()
    return run


def del_run(db: Session, run: app.schemas.RunInDB) -> app.schemas.RunInDB:
    for run_stop in run.run_stops:
        del_run_stop(db, run_stop=run_stop)
    db.delete(run)
    db.commit()
    return run


def create_run_stop(
    db: Session, run_stop: app.schemas.RunStopCreate, run_id: int
) -> app.schemas.RunStop:
    db_run_stop = app.models.RunStop(**run_stop.model_dump(), run_id=run_id)
    save_in_db(db=db, obj=db_run_stop)
    return db_run_stop


def get_run_stop(db: Session, run_stop_id: int) -> app.schemas.RunStopInDB:
    return (
        db.query(app.models.RunStop)
        .filter(app.models.RunStop.id == run_stop_id)
        .first()
    )


def get_run_stops(db: Session) -> list[app.schemas.RunStopInDB]:
    return (
        db.query(app.models.RunStop)
        .order_by(app.models.RunStop.run_id)
        .order_by(app.models.RunStop.depart_time)
        .all()
    )


def get_run_run_stops(db: Session, run_id: int) -> list[app.schemas.RunStopInDB]:
    return (
        db.query(app.models.RunStop)
        .filter(app.models.RunStop.run_id == run_id)
        .order_by(app.models.RunStop.depart_time)
        .all()
    )


def get_stop_run_stops(db: Session, stop_id: int) -> list[app.schemas.RunStopInDB]:
    return (
        db.query(app.models.RunStop)
        .filter(app.models.RunStop.run_id == stop_id)
        .order_by(app.models.RunStop.depart_time)
        .all()
    )


def update_run_stop_times(
    db: Session,
    run_stop: app.schemas.RunStopInDB,
    arrival_time: time,
    depart_time: time,
) -> app.schemas.RunStopInDB:
    run_stop.arrival_time = arrival_time
    run_stop.depart_time = depart_time
    db.commit()
    return run_stop


def del_run_stop(
    db: Session, run_stop: app.schemas.RunStopInDB
) -> app.schemas.RunStopInDB:
    db.delete(run_stop)
    db.commit()
    return run_stop
