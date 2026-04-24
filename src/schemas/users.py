from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime as dati
import re

def valid_first_or_last_name(name: str, meaning: str) -> str:
    len_name = len(name)
    if len_name < 2 or len_name >= 31:
        raise ValueError(
            f'{meaning} должно состоять хотя бы из 2 букв и быть не длинее 30 символов.'
        )
    if not re.match(r'^[а-яёА-ЯЁa-zA-Z]+$', name):
        raise ValueError(
            f'{meaning} должно состоять только из букв латинского алфавита или кириллицы.'
        )
    if not re.match(r'[A-ZА-ЯЁ]', name[0]):
        raise ValueError(
            f'{meaning} должно начинаться с заглавной буквы.'
        )
    if not re.match(r'^.[а-яёa-z]+$', name):
        raise ValueError(
            f'{meaning} может только начинаться с заглавной буквы.'
        )
    return name


def valid_nickname(nickname: str):
    len_nickname = len(nickname)
    if len_nickname < 3 or len_nickname > 30:
        raise ValueError(
            'Никнейм должен быть длиннее 2 символов и короче 21 символа.'
        )
    return nickname


class UserUpdate(BaseModel):
    first_name: str = Field()
    last_name: str = Field()
    bio_info: str = Field()
    email: EmailStr = Field()

    @field_validator("first_name", mode="after")
    @staticmethod
    def check_first_name(first_name: str):
        return valid_first_or_last_name(first_name, 'Имя')

    @field_validator("last_name", mode="after")
    @staticmethod
    def check_last_name(last_name: str):
        return valid_first_or_last_name(last_name, 'Фамилия')


class UserCreate(UserUpdate):
    nickname: str = Field()
    password: str = Field()

    @field_validator("nickname", mode="after")
    @staticmethod
    def check_nickname(nickname: str):
        return valid_nickname(nickname)

    @field_validator("password", mode="after")
    @staticmethod
    def check_password(password: str):
        password_bytes = password.encode('utf-8')
        if len(password_bytes) < 10:
            raise ValueError('Пароль должен содержать минимум 10 байт.')
        if len(password_bytes) > 72:
            raise ValueError('Пароль слишком длинный (максимум 72 байта).')
        return password


class UserOut(UserUpdate):
    id: int
    nickname: str
    active: bool
    date_joined: dati

    @field_validator("nickname", mode="after")
    @staticmethod
    def check_nickname(nickname: str):
        return valid_nickname(nickname)

    class Config:
        from_attributes = True