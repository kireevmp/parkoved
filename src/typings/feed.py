from typing import Any

from nanoid import generate as nanoid
from pydantic import BaseModel, Field


class ParkModel(BaseModel):
    _id: Any = Field(
        default=...,
        description="Mongo ObjectID",
    )

    pid: str = Field(
        description="Внутренний ID Парка",
        default_factory=lambda: nanoid(size=16),
        max_length=16,
        min_length=16,
    )

    name: str = Field(
        description="Название парка",
        min_length=1
    )
