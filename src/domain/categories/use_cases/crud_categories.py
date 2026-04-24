from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.categories import CategoryRepository
from ....schemas.categories import CategoryOut, CategoryUpdateAndCreate

from src.core.exceptions.domain_exceptions import CategoryNotFoundBySlugException, CategoryIsNotUniqueException
from src.core.exceptions.database_exceptions import CategoryNotFoundException, CategiryAlreadyExistsException


class MethodsForCategory:
    def __init__(self):
        self._repo = CategoryRepository()

    def get(self, DataBase: Session, skip: int, limit: int) -> List[CategoryOut]:
        return [CategoryOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit)]

    def get_detail(self, DataBase: Session, category_slug: str) -> CategoryOut:
        try:
            category_model = self._repo.get_detail(DataBase, category_slug)
        except CategoryNotFoundException:
            raise CategoryNotFoundBySlugException(category_slug)
        return CategoryOut.model_validate(category_model)

    def create(self, DataBase: Session, payload: CategoryUpdateAndCreate) -> CategoryOut:
        try:
            category_model = self._repo.create(DataBase, payload)
        except CategiryAlreadyExistsException:
            raise CategoryIsNotUniqueException(payload.slug)
        return CategoryOut.model_validate(category_model)

    def update(self, DataBase: Session, category_slug: str, payload: CategoryUpdateAndCreate) -> CategoryOut:
        try:
            category_model = self._repo.update(DataBase, category_slug, payload)
        except CategoryNotFoundException:
            raise CategoryNotFoundBySlugException(category_slug)
        except CategiryAlreadyExistsException:
            raise CategoryIsNotUniqueException(payload.slug)
        return CategoryOut.model_validate(category_model)
    
    def destroy(self, DataBase: Session, category_slug: str):
        try:
            self._repo.destroy(DataBase, category_slug)
        except CategoryNotFoundException:
            raise CategoryNotFoundBySlugException(category_slug)
