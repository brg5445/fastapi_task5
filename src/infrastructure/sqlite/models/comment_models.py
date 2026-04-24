from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from datetime import datetime as dati

from sqlalchemy.orm import relationship
from ..database import Base


class CommentModel(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=dati.utcnow)
    text = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post = relationship("PostModel", back_populates="comments")
    author = relationship("UserModel", back_populates="comments")