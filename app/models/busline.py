from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.models import Base


class Busline(Base):
    __tablename__ = "buslines"
    id = Column(Integer, primary_key=True, index=True)
    busline_name = Column(String, index=True)
    busline_return = Column(Boolean, index=True)

    runs = relationship("Run", back_populates="busline")
