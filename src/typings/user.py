from typing import Any, Optional

from nanoid import generate as nanoid
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    _id: Any = Field(
        default=...,
        description="Mongo ObjectID",
    )

    uid: str = Field(
        description="ID юзера",
        max_length=16,
        min_length=16,
        default_factory=lambda: nanoid(size=16)
    )

    phone: str = Field(
        description="Телефон пользователя"
    )

    name: Optional[str] = Field(
        description="Имя пользователя",
        default=...
    )

    email: Optional[EmailStr] = Field(
        default=...,
        description="Мыло пользователя"
    )

    # notifications: bool = Field(
    #     default=False,
    #     description="Получать ли уведомления"
    # )
