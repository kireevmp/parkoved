from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import parse_obj_as, BaseModel, Field

from .common import pwd_ctx
from ..db import users, admins
from ..lib import with_auth
from ..typings.admin import AdminModel
from ..typings.token import TokenModel
from ..typings.user import UserModel

router = APIRouter()


@router.get("/me", response_model=UserModel, response_model_exclude={"_id"}, description="Получить данные самого себя")
def me(token: TokenModel = Depends(with_auth)):
    try:
        user = parse_obj_as(UserModel, users.find_one({"uid": token.id}))
    except ValueError:
        raise HTTPException(status_code=404, detail="user.notfound")

    return user


class CreateAdminRequestModel(BaseModel):
    login: str = Field(
        description="Логин нового админа",
        min_length=6,
        max_length=32,
    )
    password: str = Field(
        description="Пароль нового админа",
        min_length=6,
        max_length=32,
    )
    parks: List[str] = Field(
        description="Список парков для администратора",
        default=[],
    )


class CreateAdminResponseModel(BaseModel):
    success: bool = True


@router.post("/admin/create")
def create_admin(data: CreateAdminRequestModel = Body(..., embed=False)):
    if admins.find_one({"login": data.login}) is not None:
        raise HTTPException(status_code=409, detail="login.exists")

    admin = AdminModel(parks=data.parks, password=pwd_ctx.hash(data.password), login=data.login)

    admins.insert_one(admin.dict())

    return {
        "success": True
    }
