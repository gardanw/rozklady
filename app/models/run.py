from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Run(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True, index=True)
    busline_id = Column(Integer, ForeignKey("buslines.id"))
    descript = Column(String, index=True)

    busline = relationship("Busline", back_populates="runs")
    run_stops = relationship("RunStop", back_populates="run")
