from enum import Enum
from typing import Any, Union, List

from nanoid import generate as nanoid
from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    cafe = "cafe"
    space = "space"
    # park = "park"
    attraction = "attraction"


class ServicePosition(BaseModel):
    lat: float = Field(
        description="Широта"
    )
    lon: float = Field(
        description="Долгота"
    )


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

    kind: ServiceType = Field(
        description="Вид сервиса (кафе, пространство, аттракцион или билет в сам парк)"
    )

    name: str = Field(
        description="Видимое для пользователя название услуги",
        min_length=1,
    )

    expireTime: int = Field(
        description="Время действия купленного билета в секундах (со времени покупки)",
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

    priceAdults: int = Field(
        description="Цена взрослого билета",
        ge=0
    )

    priceChildren: Union[int, None] = Field(
        description="Цена детского билета",
        ge=0,
    )

    picture: List[str] = Field(
        description="Ссылки на картинки этого места"
    )

    desc: str = Field(
        description="Краткое описание (1 предложение)"
    )

    longDesc: str = Field(
        description="Длинное описание"
    )

    position: ServicePosition = Field(
        description="Местоположение сервиса"
    )
