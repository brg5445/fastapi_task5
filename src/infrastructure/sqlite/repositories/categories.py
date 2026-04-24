from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.category_models import CategoryModel
from ....schemas.categories import CategoryUpdateAndCreate

from src.core.exceptions.database_exceptions import CategoryNotFoundException, CategiryAlreadyExistsException

class CategoryRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session, skip: int, limit: int) -> List[CategoryModel]:
        return DataBase.query(CategoryModel).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, category_slug: str) -> CategoryModel:
        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == category_slug
        ).first()
        if not category:
            raise CategoryNotFoundException()
        return category

    def create(self, DataBase: Session, payload: CategoryUpdateAndCreate) -> CategoryModel:
        category = CategoryModel(**payload.model_dump())
        try:
            DataBase.add(category)
            DataBase.commit()
        except IntegrityError:
            raise CategiryAlreadyExistsException()
        DataBase.refresh(category)
        return category

    def update(self, DataBase: Session, category_slug: str, payload: CategoryUpdateAndCreate) -> CategoryModel:
        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == category_slug
        ).first()
        if not category:
            raise CategoryNotFoundException()
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        try:
            DataBase.commit()
        except IntegrityError:
            raise CategiryAlreadyExistsException()
        DataBase.refresh(category)
        return category

    def destroy(self, DataBase: Session, category_slug: str):
        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == category_slug
        ).first()
        if not category:
            raise CategoryNotFoundException()
        DataBase.delete(category)
        DataBase.commit()