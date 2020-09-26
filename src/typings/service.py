from typing import Any

from nanoid import generate as nanoid
from pydantic import BaseModel, Field


class ServiceModel(BaseModel):
    _id: Any = Field(
        description="Mongo ObjectID",
    )

    sid: str = Field(
        description="Внутренний ID сервиса/аттракциона",
        default_factory=lambda: nanoid(size=16),
        max_length=16,
        min_length=16,
    )

    park: str = Field(
        description="Внутренний ID парка",
        max_length=16,
        min_length=16,
    )

    name: str = Field(
        description="Видимое для пользователя название услуги",
        min_length=1,
    )

    expireTime: int = Field(
        description="Время действия купленного билета в секундах",
        gt=1,
    )

    workingHours: str = Field(
        description="Часы работы, формат hh:mm-hh:mm",
        regex=r"^(([0,1][0-9])|(2[0-3])):[0-5][0-9]-(([0,1][0-9])|(2[0-3])):[0-5][0-9]$"
    )

    ageLimit: int = Field(
        description="Ограничение возраста",
        ge=0
    )
