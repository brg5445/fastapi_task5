from pydantic import BaseModel, Field, field_validator
from datetime import datetime as dati


class LocationUpdateAndCreate(BaseModel):
    name: str = Field(default=None)
    is_published: bool = Field(default=None)

    @field_validator("name", mode="after")
    @staticmethod
    def check_name(name: str):
        len_name = len(name)
        if len_name < 5 or len_name > 40:
            raise ValueError(
                'Название локации должно быть длиннее 4 символов и короче 41 символа.'
            )
        return name


class LocationOut(LocationUpdateAndCreate):
    id: int
    created_at: dati

    class Config:
        from_attributes = True