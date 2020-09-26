from fastapi import APIRouter, Depends, HTTPException
from pydantic import parse_obj_as

from ..db import users
from ..lib import with_auth
from ..typings.token import TokenModel
from ..typings.user import UserModel

router = APIRouter()


@router.get("/me", response_model=UserModel, response_model_exclude={"_id"})
def me(token: TokenModel = Depends(with_auth)):
    try:
        user = parse_obj_as(UserModel, users.find_one({"uid": token.uid}))
    except ValueError:
        return HTTPException(status_code=404, detail="user.notfound")

    return user
