from fastapi import APIRouter, Body, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from ..db import users, admins
from ..lib import build_jwt
from ..typings.admin import AdminModel
from ..typings.token import UserRole
from ..typings.user import UserModel

router = APIRouter()
pwd_ctx = CryptContext(schemes=["bcrypt"])


class RegisterResponseModel(BaseModel):
    success: bool = True


class RegisterRequestModel(BaseModel):
    phone: str = Field(
        description="Номер телефона",
    )


@router.post("/request", response_model=RegisterResponseModel, name="Request Code", status_code=202)
def register(data: RegisterRequestModel = Body(..., embed=False)):
    # TODO: send SMS
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


@router.post("/confirm", name="Confirm Phone", response_model=ConfirmResponseModel, status_code=201)
def confirm(data: ConfirmRequestModel = Body(..., embed=False)):
    phone = data.phone
    # if users.find_one({"phone": phone}) is None:
    #     raise HTTPException(status_code=409, detail="phone.notexists")

    user = UserModel(phone=phone)
    users.insert_one(user.dict())

    return {
        "token": build_jwt(user.uid, UserRole.user)
    }


class AdminLoginRequestModel(BaseModel):
    password: str
    login: str


class AdminLoginResponseModel(BaseModel):
    token: str


@router.post("/admin", tags=["Admin"], description="Войти под администратором парка", name="Login as Admin")
def login(data: AdminLoginRequestModel = Body(..., embed=False)):
    user: AdminModel = AdminModel.parse_obj(admins.find_one({"login": data.login}))
    if user is None or not pwd_ctx.verify(data.password, user.password):
        return HTTPException(status_code=403, detail="data.wrong")

    return {
        "token": build_jwt(user.uid, UserRole.admin)
    }
