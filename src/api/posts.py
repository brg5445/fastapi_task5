from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..domain.posts.use_cases.crud_posts import MethodsForPost
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIDException,
    PostDontCreateException,
    PostDontChangeException,
)
from ..infrastructure.sqlite.database import get_db
from ..schemas.posts import PostCreate, PostDetail, PostOut, PostUpdate
from src.core.security import get_current_user
from src.infrastructure.sqlite.models.user_models import UserModel

router = APIRouter(prefix='/posts', tags=['Посты'])


@router.get('/', response_model=List[PostOut], summary='Публикации:')
def list_posts(
    skip: int = 0,
    limit: int = 20,
    published_only: bool = False,
    DataBase: Session = Depends(get_db)
) -> List[PostOut]:
    use_case = MethodsForPost()
    return use_case.get(DataBase, skip, limit, published_only)


@router.get('/{post_id}', response_model=PostDetail, summary='Получить публикацию:')
def get_post(post_id: int, DataBase: Session = Depends(get_db)) -> PostDetail:
    use_case = MethodsForPost()
    try:
        return use_case.get_detail(DataBase, post_id)
    except PostNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post('/', response_model=PostOut, status_code=status.HTTP_201_CREATED, summary='Создать публикацию:')
def create_post(
    payload: PostCreate,
    DataBase: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
) -> PostOut:
    use_case = MethodsForPost()
    try:
        # Передаём author_id в use-case
        return use_case.create(DataBase, payload, author_id=current_user.id)
    except PostDontCreateException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.put('/{post_id}', response_model=PostOut, summary='Изменить публикацию:')
def update_post(
    post_id: int,
    payload: PostUpdate,
    DataBase: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
) -> PostOut:
    use_case = MethodsForPost()
    try:
        return use_case.update(DataBase, post_id, payload, current_user=current_user)
    except PostNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except PostDontChangeException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Удалить публикацию:')
def delete_post(
    post_id: int,
    DataBase: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    use_case = MethodsForPost()
    try:
        use_case.destroy(DataBase, post_id, current_user=current_user)
    except PostNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())