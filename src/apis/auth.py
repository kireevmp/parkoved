from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field

from ..db import users
from ..lib import build_jwt
from ..typings.user import UserModel

router = APIRouter()


class RegisterResponseModel(BaseModel):
    success: bool = True


class RegisterRequestModel(BaseModel):
    phone: str = Field(
        description="Номер телефона",
    )


@router.post("/register", response_model=RegisterResponseModel, name="Request Code")
def register(data: RegisterRequestModel = Body(..., embed=False)):
    return {
        "success": True
    }


class ConfirmResponseModel(BaseModel):
    token: str


class ConfirmRequestModel(BaseModel):
    phone: str = Field(
        description="Номер телефона",
    )
    code: str = Field(
        description="Код из СМС",
        regex=r"^\d{6}$"
    )


@router.post("/confirm", name="Confirm Phone", response_model=ConfirmResponseModel)
def confirm(data: ConfirmRequestModel = Body(..., embed=False)):
    phone = data.phone
    if users.find_one({"phone": phone}) is not None:
        raise HTTPException(status_code=409, detail="phone.exists")

    user = UserModel(phone=phone)
    users.insert_one(user.dict())

    return {
        "token": build_jwt(user.uid)
    }
