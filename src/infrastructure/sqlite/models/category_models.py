from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime as dati

from ..database import Base

class CategoryModel(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=dati.utcnow)
    title = Column(String, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    posts = relationship("PostModel", back_populates="category", cascade="all, delete-orphan")