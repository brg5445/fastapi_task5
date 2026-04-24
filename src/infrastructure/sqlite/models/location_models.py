from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime as dati
from ..database import Base


class LocationModel(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=dati.utcnow)
    is_published = Column(Boolean, default=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    posts = relationship("PostModel", back_populates="location", cascade="all, delete-orphan")