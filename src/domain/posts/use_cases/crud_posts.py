from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.post_models import PostModel
from src.infrastructure.sqlite.models.user_models import UserModel
from src.schemas.posts import PostCreate, PostUpdate
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIDException,
    PostDontCreateException,
    PostDontChangeException
)


class MethodsForPost:
    def get(self, db: Session, skip: int = 0, limit: int = 20, published_only: bool = False):
        query = db.query(PostModel)
        if published_only:
            query = query.filter(PostModel.published == True)
        return query.offset(skip).limit(limit).all()

    def get_detail(self, db: Session, post_id: int):
        post = db.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise PostNotFoundByIDException()
        return post

    def create(self, db: Session, payload: PostCreate, author_id: int):
        from src.infrastructure.sqlite.models.category_models import CategoryModel
        from src.infrastructure.sqlite.models.location_models import LocationModel

        category = db.query(CategoryModel).filter(CategoryModel.id == payload.category_id).first()
        location = db.query(LocationModel).filter(LocationModel.id == payload.location_id).first()

        if not category or not location:
            raise PostDontCreateException("Категория или локация не найдены")

        post = PostModel(
            title=payload.title,
            content=payload.content,
            category_id=payload.category_id,
            location_id=payload.location_id,
            author_id=author_id,  # Автоматически устанавливаем автора
            published=payload.published if hasattr(payload, 'published') else False
        )

        try:
            db.add(post)
            db.commit()
            db.refresh(post)
            return post
        except Exception as e:
            db.rollback()
            raise PostDontCreateException(str(e))

    def update(self, db: Session, post_id: int, payload: PostUpdate, current_user: UserModel):
        post = db.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise PostNotFoundByIDException()

        if post.author_id != current_user.id:
            raise PostDontChangeException("Вы не являетесь автором этого поста")

        if payload.title is not None:
            post.title = payload.title
        if payload.content is not None:
            post.content = payload.content
        if payload.category_id is not None:
            # Проверка существования категории
            from src.infrastructure.sqlite.models.category_models import CategoryModel
            category = db.query(CategoryModel).filter(CategoryModel.id == payload.category_id).first()
            if not category:
                raise PostDontChangeException("Категория не найдена")
            post.category_id = payload.category_id
        if payload.location_id is not None:
            from src.infrastructure.sqlite.models.location_models import LocationModel
            location = db.query(LocationModel).filter(LocationModel.id == payload.location_id).first()
            if not location:
                raise PostDontChangeException("Локация не найдена")
            post.location_id = payload.location_id
        if hasattr(payload, 'published') and payload.published is not None:
            post.published = payload.published

        try:
            db.commit()
            db.refresh(post)
            return post
        except Exception as e:
            db.rollback()
            raise PostDontChangeException(str(e))

    def destroy(self, db: Session, post_id: int, current_user: UserModel):
        post = db.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise PostNotFoundByIDException()

        if post.author_id != current_user.id:
            raise PostDontChangeException("Вы не являетесь автором этого поста")

        try:
            db.delete(post)
            db.commit()
        except Exception as e:
            db.rollback()
            raise PostDontChangeException(str(e))