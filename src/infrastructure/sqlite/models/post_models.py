from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime as dati
from ..database import Base


class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=dati.utcnow)
    text = Column(Text, nullable=False)
    title = Column(String, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    pub_date = Column(DateTime, nullable=False)
    image = Column(String, default="", nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    author = relationship("UserModel", back_populates="posts")
    location = relationship("LocationModel", back_populates="posts")
    category = relationship("CategoryModel", back_populates="posts")
    comments = relationship(
        "CommentModel", back_populates="post", cascade="all, delete-orphan"
    )