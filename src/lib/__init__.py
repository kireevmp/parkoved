import os
import time

import jwt
from fastapi import Header, HTTPException
from nanoid import generate as nanoid
from pydantic import parse_obj_as

from ..typings.token import TokenModel, UserRole

JWT_TIME = 1000 * 60 * 60 * 24 * 30


def build_jwt(uid: str, role: UserRole):
    return jwt.encode({
        "id": uid,
        "jti": nanoid(),
        "role": role,
        "exp": time.time() * 1000 + JWT_TIME
    }, key=os.getenv("SECRET"))


def with_auth(authorization: str = Header(None)):
    try:
        bearer, token = authorization.split(" ")
        assert bearer.lower() == "bearer"
        data = parse_obj_as(TokenModel, jwt.decode(token, key=os.getenv("SECRET")))
    except (AssertionError, jwt.InvalidTokenError, ValueError):
        return HTTPException(status_code=400, detail="token.invalid")

    return data
