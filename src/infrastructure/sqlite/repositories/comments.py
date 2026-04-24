from typing import List

from sqlalchemy.orm import Session, joinedload

from ..models.comment_models import CommentModel
from ..models.post_models import PostModel
from ..models.user_models import UserModel
from ....schemas.comments import CommentCreate, CommentUpdate

from src.core.exceptions.database_exceptions import (UserNotFoundException,
                                                     PostNotFoundException,
                                                     CommentNotFoundException)

class CommentRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session, post_id: int | None, skip: int, limit: int) -> List[CommentModel]:
        post = (DataBase.query(PostModel)
                .filter(PostModel.id == post_id)
                .first())
        if not post:
            raise PostNotFoundException()
        query = DataBase.query(CommentModel)
        if post_id is not None:
            query = query.filter(CommentModel.post_id == post_id)
        return query.order_by(CommentModel.created_at).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, comment_id: int) -> CommentModel:
        comment = DataBase.query(CommentModel).filter(
            CommentModel.id == comment_id
        ).first()
        if not comment:
            raise CommentNotFoundException()
        return comment

    def create(self, DataBase: Session, payload: CommentCreate) -> CommentModel:
        post = DataBase.query(PostModel).filter(
            PostModel.id == payload.post_id
        ).first()
        if not post:
            raise PostNotFoundException()
        author = DataBase.query(UserModel).filter(
            UserModel.nickname == payload.author_nickname
        ).first()
        if not author:
            raise UserNotFoundException()

        dict_ = (payload.model_dump(exclude={'author_nickname'})
                 | {'author_id':author.id})

        comment = CommentModel(**dict_)
        DataBase.add(comment)
        DataBase.commit()
        DataBase.refresh(comment)
        return comment

    def update(self, DataBase: Session, comment_id: int, payload: CommentUpdate) -> CommentModel:
        comment = DataBase.query(CommentModel).filter(
            CommentModel.id == comment_id
        ).first()
        if not comment:
            raise CommentNotFoundException()
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(comment, field, value)
        DataBase.commit()
        DataBase.refresh(comment)
        return comment

    def destroy(self, DataBase: Session, comment_id: int):
        comment = DataBase.query(CommentModel).filter(
            CommentModel.id == comment_id
        ).first()
        if not comment:
            raise CommentNotFoundException()
        DataBase.delete(comment)
        DataBase.commit()