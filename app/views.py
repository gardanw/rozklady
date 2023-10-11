from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
import app.schemas


router = APIRouter()


@router.post("/towns/", response_model=app.schemas.Town)
async def create_town(town: app.schemas.TownCreate, db: Session = Depends(get_db)):
    db_town = crud.get_town_by_name(db, name=town.town_name)
    if db_town:
        raise HTTPException(status_code=400, detail="Town already registered")
    return crud.create_town(db=db, town=town)


@router.get("/towns/{town_id}", response_model=app.schemas.Town)
async def read_town(town_id, db: Session = Depends(get_db)):
    db_town = crud.get_town(db, town_id=town_id)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return db_town