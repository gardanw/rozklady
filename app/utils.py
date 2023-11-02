from typing import Union

from sqlalchemy.orm import Session

from app import crud
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
