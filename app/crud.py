from sqlalchemy.orm import Session

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


def update_town_name(db: Session, town: app.schemas.TownInDB, new_name: str) -> app.schemas.TownInDB:
    town.town_name = new_name
    db.commit()
    return town


def del_town(db: Session, town: app.schemas.TownInDB) -> app.schemas.TownInDB:
    db.delete(town)
    db.commit()
    return town


def get_town_stops(db: Session, town_id: int):
    return db.query(app.models.Stop).filter(app.models.Stop.town_id == town_id).all()


def create_stop(db: Session, stop: app.schemas.StopCreate, town_id: int):
    db_stop = app.models.Stop(**stop.model_dump(), town_id=town_id)
    save_in_db(db=db, obj=db_stop)
    return db_stop


def get_buslien(db: Session, busline_id: int):
    return (
        db.query(app.models.Busline).filter(app.models.Busline.id == busline_id).first()
    )


def create_busline(db: Session, busline: app.schemas.BuslineCreate):
    db_busline = app.models.Busline(**busline.model_dump())
    save_in_db(db=db, obj=db_busline)
    return db_busline


def create_run(db: Session, run: app.schemas.RunCreate, busline_id: int):
    db_run = app.models.Run(**run.model_dump(), busline_id=busline_id)
    save_in_db(db=db, obj=db_run)
    return db_run


def create_run_stop(db: Session, run_stop: app.schemas.RunStopCreate, run_id: int):
    db_run_stop = app.models.RunStop(**run_stop.model_dump(), run_id=run_id)
    save_in_db(db=db, obj=db_run_stop)
    return db_run_stop


def get_run(db: Session, run_id: int):
    return db.query(app.models.Run).filter(app.models.Run.id == run_id).first()


def get_stop(db: Session, stop_id: int):
    return db.query(app.models.Stop).filter(app.models.Stop.id == stop_id)
