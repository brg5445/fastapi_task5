from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.comment_models import CommentModel
from src.infrastructure.sqlite.models.post_models import PostModel
from src.infrastructure.sqlite.models.user_models import UserModel
from src.schemas.comments import CommentCreate, CommentUpdate
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIDException,
    CommentDontCreateException,
    PostNotFoundByIDException
)


class MethodsForComment:
    def get(self, db: Session, post_id: int = None, skip: int = 0, limit: int = 50):
        query = db.query(CommentModel)
        if post_id is not None:
            post = db.query(PostModel).filter(PostModel.id == post_id).first()
            if not post:
                raise PostNotFoundByIDException()
            query = query.filter(CommentModel.post_id == post_id)
        return query.offset(skip).limit(limit).all()

    def get_detail(self, db: Session, comment_id: int):
        comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
        if not comment:
            raise CommentNotFoundByIDException()
        return comment

    def create(self, db: Session, payload: CommentCreate, author_id: int):
        post = db.query(PostModel).filter(PostModel.id == payload.post_id).first()
        if not post:
            raise CommentDontCreateException("Пост не найден")

        comment = CommentModel(
            content=payload.content,
            post_id=payload.post_id,
            author_id=author_id
        )

        try:
            db.add(comment)
            db.commit()
            db.refresh(comment)
            return comment
        except Exception as e:
            db.rollback()
            raise CommentDontCreateException(str(e))

    def update(self, db: Session, comment_id: int, payload: CommentUpdate, current_user: UserModel):
        comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
        if not comment:
            raise CommentNotFoundByIDException()

        if comment.author_id != current_user.id:
            raise CommentDontCreateException("Вы не являетесь автором этого комментария")

        # Обновление полей
        if payload.content is not None:
            comment.content = payload.content

        try:
            db.commit()
            db.refresh(comment)
            return comment
        except Exception as e:
            db.rollback()
            raise CommentDontCreateException(str(e))

    def destroy(self, db: Session, comment_id: int, current_user: UserModel):
        comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
        if not comment:
            raise CommentNotFoundByIDException()

        if comment.author_id != current_user.id:
            raise CommentDontCreateException("Вы не являетесь автором этого комментария")

        try:
            db.delete(comment)
            db.commit()
        except Exception as e:
            db.rollback()
            raise CommentDontCreateException(str(e))