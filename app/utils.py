from typing import Union

from sqlalchemy.orm import Session

from app import crud


def save_in_db(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)


def get_town_by_param(db: Session, town: Union[int, str]):
    db_town = None
    if isinstance(town, int):
        db_town = crud.get_town(db=db, town_id=town)
    if isinstance(town, str):
        db_town = crud.get_town_by_name(db=db, name=town)
    return db_town
