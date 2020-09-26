from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    root = "root"


class TokenModel(BaseModel):
    id: str = Field(
        description="ID юзера",
        max_length=16,
        min_length=16,
    )

    role: UserRole
