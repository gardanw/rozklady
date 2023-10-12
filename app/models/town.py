from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Town(Base):
    __tablename__ = "towns"
    id = Column(Integer, primary_key=True, index=True)
    town_name = Column(String, unique=True, index=True)

    stops = relationship("Stop", back_populates="town")
