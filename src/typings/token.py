from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    uid: str = Field(
        description="ID юзера",
        max_length=16,
        min_length=16,
    )
