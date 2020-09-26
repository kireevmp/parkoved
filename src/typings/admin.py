from typing import Any, List

from nanoid import generate as nanoid
from pydantic import BaseModel, Field


class AdminModel(BaseModel):
    _id: Any = Field(
        default=...,
        description="Mongo ObjectID",
    )

    uid: str = Field(
        description="ID администратора",
        max_length=16,
        min_length=16,
        default_factory=lambda: nanoid(size=16)
    )

    parks: List[str] = Field(
        description="Список парков, которые администрирует пользователь"
    )

    login: str = Field(
        description="Логин администратора",
        min_length=6,
        max_length=32
    )

    password: str = Field(
        description="Хэш пароля",
    )
