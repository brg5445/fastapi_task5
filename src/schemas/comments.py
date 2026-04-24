from pydantic import BaseModel, Field, field_validator
from datetime import datetime as dati


class CommentUpdate(BaseModel):
    text: str = Field(default=None)

    @field_validator("text", mode="after")
    @staticmethod
    def check_text(text: str):
        len_text = len(text)
        if len_text == 0 or len_text > 500:
            raise ValueError(
                'Текст комментария должен содержать хотя б 1 символ и быть короче 501 символа.'
            )


class CommentCreate(CommentUpdate):
    post_id: int
    author_nickname: str

class CommentOut(CommentUpdate):
    post_id: int
    author_id: int
    id: int
    created_at: dati

    class Config:
        from_attributes = True