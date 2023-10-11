from sqlalchemy.orm import Session

import app.models, app.schemas


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
