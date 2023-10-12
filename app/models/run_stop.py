from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship

from app.database import Base


class RunStop(Base):
    __tablename__ = "run_stops"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    stop_id = Column(Integer, ForeignKey("stops.id"))
    arrival_time = Column(Time, index=True)
    depart_time = Column(Time, index=True)

    run = relationship("Run", back_populates="run_stops")
    stop = relationship("Stop", back_populates="run_stops")
