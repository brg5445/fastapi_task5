from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime as dati

from ..database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    bio_info = Column(Text, default="")
    hashed_password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    date_joined = Column(DateTime(timezone=True), default=dati.utcnow)
    posts = relationship("PostModel", back_populates="author", foreign_keys="PostModel.author_id", cascade="all, delete-orphan")
    comments = relationship("CommentModel", back_populates="author", cascade="all, delete-orphan")