from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Stop(Base):
    __tablename__ = "stops"
    id = Column(Integer, primary_key=True, index=True)
    stop_name = Column(String, index=True)
    town_id = Column(Integer, ForeignKey("towns.id"))

    town = relationship("Town", back_populates="stops")
    run_stops = relationship("RunStop", back_populates="stop")
