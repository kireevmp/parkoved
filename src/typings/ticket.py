import time
from typing import Any

from nanoid import generate as nanoid
from pydantic import BaseModel, Field


class TicketModel(BaseModel):
    _id: Any = Field(
        default=...,
        description="Mongo ObjectID",
    )

    tid: str = Field(
        description="Внутренний ID билета",
        default_factory=lambda: nanoid(size=16),
        max_length=16,
        min_length=16,
    )

    service: str = Field(
        description="Внутренний ID вида аттракциона/сервиса/...",
        max_length=16,
        min_length=16,
    )

    uses: int = Field(
        description="Оставшееся количество использований билета",
        ge=0,
    )

    isForChild: bool = Field(
        description="Является ли билет детским",
    )

    owner: str = Field(
        description="uid пользователя",
        max_length=16,
        min_length=16,
    )

    expiresAt: int = Field(
        description="Время (UNIX seconds) окончания действия билета",
        # default_factory=lambda: time.time()
    )
    createdAt: int = Field(
        description="Время (UNIX seconds) создания/покупки билета",
        default_factory=lambda: time.time()
    )
