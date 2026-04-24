from typing import List

from sqlalchemy.orm import Session, joinedload

from ..models.category_models import CategoryModel
from ..models.location_models import LocationModel
from ..models.post_models import PostModel
from ..models.user_models import UserModel
from ....schemas.posts import PostCreate, PostUpdate

from src.core.exceptions.database_exceptions import (UserNotFoundException,
                                                     CategoryNotFoundException,
                                                     LocationNotFoundException, 
                                                     PostNotFoundException)

class PostRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session,
            skip: int,
            limit: int,
            published_only: bool) -> List[PostModel]:
        query = DataBase.query(PostModel)
        if published_only:
            query = query.filter(PostModel.is_published.is_(True))
        return query.order_by(PostModel.pub_date.desc()).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, post_id: int) -> PostModel:
        post = (
            DataBase.query(PostModel)
            .options(
                joinedload(PostModel.author),
                joinedload(PostModel.category),
                joinedload(PostModel.location),
                joinedload(PostModel.comments),
            )
            .filter(PostModel.id == post_id)
            .first()
        )
        if not post:
            raise PostNotFoundException()
        return post

    def create(self, DataBase: Session, payload: PostCreate) -> PostModel:
        author = DataBase.query(UserModel).filter(
            UserModel.nickname == payload.author_nickname
        ).first()
        if not author:
            raise UserNotFoundException()

        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == payload.category_slug
        ).first()
        if not category:
            raise CategoryNotFoundException()

        location = DataBase.query(LocationModel).filter(
            LocationModel.name == payload.location_name
        ).first()
        if not location:
            raise LocationNotFoundException()

        dict_ = (payload.model_dump(
                    exclude={'location_name',
                             'author_nickname',
                             'category_slug'}
                    ) |
                 {'location_id':location.id,
                  'category_id':category.id,
                  'author_id':author.id})
        post = PostModel(**dict_)
        DataBase.add(post)
        DataBase.commit()
        DataBase.refresh(post)
        return post

    def update(self, DataBase: Session, post_id: int, payload: PostUpdate) -> PostModel:
        post = DataBase.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise PostNotFoundException()
        
        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == payload.category_slug
        ).first()
        if not category:
            raise CategoryNotFoundException()

        location = DataBase.query(LocationModel).filter(
            LocationModel.name == payload.location_name
        ).first()
        if not location:
            raise LocationNotFoundException()

        dict_ = (payload.model_dump(
                    exclude={'location_name',
                             'author_nickname',
                             'category_slug'}
                    ) |
                 {'location_id':location.id,
                  'category_id':category.id})

        for field, value in dict_.items():
            setattr(post, field, value)
        DataBase.commit()
        DataBase.refresh(post)
        return post

    def destroy(self, DataBase: Session, post_id: int):
        post = DataBase.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise PostNotFoundException()
        DataBase.delete(post)
        DataBase.commit()