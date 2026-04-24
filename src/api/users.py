from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..domain.users.use_cases.crud_users import MethodsForUser
from src.core.exceptions.domain_exceptions import (
    UserNicknameIsNotUniqueException,
    UserNotFoundByNicknameException,
    UserEmailIsNotUniqueException,
)
from ..infrastructure.sqlite.database import get_db
from ..schemas.users import UserCreate, UserOut, UserUpdate
from src.core.security import get_current_user
from src.infrastructure.sqlite.models.user_models import UserModel

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/', response_model=List[UserOut], summary='Пользователи:')
def list_users(skip: int = 0, limit: int = 20, DataBase: Session = Depends(get_db)) -> List[UserOut]:
    use_case = MethodsForUser()
    return use_case.get(DataBase, skip, limit)


@router.get('/{nickname}', response_model=UserOut, summary='Получить пользователя:')
def get_user(nickname: str, DataBase: Session = Depends(get_db)) -> UserOut:
    use_case = MethodsForUser()
    try:
        return use_case.get_detail(DataBase, nickname)
    except UserNotFoundByNicknameException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED, summary='Создать пользователя:')
def create_user(payload: UserCreate, DataBase: Session = Depends(get_db)) -> UserOut:
    use_case = MethodsForUser()
    try:
        return use_case.create(DataBase, payload)
    except UserNicknameIsNotUniqueException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())
    except UserEmailIsNotUniqueException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.put('/{nickname}', response_model=UserOut, summary='Редактировать профиль:')
def update_user(
    nickname: str,
    payload: UserUpdate,
    DataBase: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
) -> UserOut:
    if current_user.nickname != nickname:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    use_case = MethodsForUser()
    try:
        return use_case.update(DataBase, nickname, payload)
    except UserNotFoundByNicknameException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except UserEmailIsNotUniqueException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.delete('/{nickname}', status_code=status.HTTP_204_NO_CONTENT, summary='Удалить аккаунт:')
def delete_user(
    nickname: str,
    DataBase: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.nickname != nickname:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    use_case = MethodsForUser()
    try:
        use_case.destroy(DataBase, nickname)
    except UserNotFoundByNicknameException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())