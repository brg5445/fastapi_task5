from pydantic import BaseModel, Field, field_validator
from datetime import datetime as dati

class CategoryUpdateAndCreate(BaseModel):
    slug: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    is_published: bool = Field(default=None)

    @field_validator("slug", mode="after")
    @staticmethod
    def check_slug(slug: str):
        len_slug = len(slug)
        if len_slug < 5 or len_slug > 40:
            raise ValueError(
                'slug должен быть длиннее 4 символов и короче 41 символа.'
            )
        return slug


class CategoryOut(CategoryUpdateAndCreate):
    id: int
    created_at: dati

    class Config:
        from_attributes = True