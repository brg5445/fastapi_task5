from sqlalchemy.exc import IntegrityError
from typing import List

from sqlalchemy import insert
from sqlalchemy.orm import Session

from ..models.user_models import UserModel
from ....schemas.users import UserCreate, UserUpdate
from src.core.exceptions.database_exceptions import (UserNotFoundException,
                                                     UserByNicknameAlreadyExistsException,
                                                     UserByEmailAlreadyExistsException)


class UserRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session, skip: int, limit: int) -> List[UserModel]:
        return DataBase.query(UserModel).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, nickname: str) -> UserModel:
        user = DataBase.query(UserModel).filter(UserModel.nickname == nickname).first()
        if not user:
            raise UserNotFoundException()
        return user

    def create(self, DataBase: Session, payload: UserCreate) -> UserModel:
        user = UserModel(
            **payload.model_dump()
        )
        try:
            DataBase.add(user)
            DataBase.commit()
        except IntegrityError as e:
            str_error = str(e.orig)
            if 'nickname' in str_error:
                raise UserByNicknameAlreadyExistsException()
            elif 'email' in str_error:
                raise UserByEmailAlreadyExistsException()
            else:
                raise IntegrityError
        DataBase.refresh(user)
        return user

    def update(self, DataBase: Session, nickname: str, payload: UserUpdate) -> UserModel:
        user = DataBase.query(UserModel).filter(UserModel.nickname == nickname).first()
        if not user:
            raise UserNotFoundException()
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        try:
            DataBase.commit()
        except IntegrityError:
            raise UserByEmailAlreadyExistsException()
        DataBase.refresh(user)
        return user

    def destroy(self, DataBase: Session, nickname: str):
        user = DataBase.query(UserModel).filter(UserModel.nickname == nickname).first()
        if not user:
            raise UserNotFoundException()
        DataBase.delete(user)
        DataBase.commit()
