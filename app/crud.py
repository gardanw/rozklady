from sqlalchemy.orm import Session

import app.models
import app.schemas


def get_town(db: Session, town_id: int):
    return db.query(app.models.Town).filter(app.models.Town.id == town_id).first()


def get_town_by_name(db: Session, name: str):
    return db.query(app.models.Town).filter(app.models.Town.town_name == name).first()


def create_town(db: Session, town: app.schemas.TownCreate):
    db_town = app.models.Town(town_name=town.town_name)
    db.add(db_town)
    db.commit()
    db.refresh(db_town)
    return db_town


def get_town_stops(db: Session, town_id: int):
    return db.query(app.models.Stop).filter(app.models.Stop.town_id == town_id).all()


def create_stop(db: Session, stop: app.schemas.StopCreate, town_id: int):
    db_stop = app.models.Stop(**stop.model_dump(), town_id=town_id)
    db.add(db_stop)
    db.commit()
    db.refresh(db_stop)
    return db_stop


def get_buslien(db: Session, busline_id: int):
    return db.query(app.models.Busline).filter(app.models.Busline.id == busline_id).first()

def create_busline(db: Session, busline: app.schemas.BuslineCreate):
    db_busline = app.models.Busline(**busline.model_dump())
    db.add(db_busline)
    db.commit()
    db.refresh(db_busline)
    return db_busline