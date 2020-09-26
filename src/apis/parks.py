from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import parse_obj_as

from ..db import parks
from ..lib import with_auth
from ..typings.park import ParkModel
from ..typings.token import TokenModel

router = APIRouter()


@router.get("/", response_model=List[ParkModel], response_model_exclude={"_id"}, name="List all Parks")
def list_parks(token: TokenModel = Depends(with_auth)):
    try:
        data = parse_obj_as(List[ParkModel], [*parks.find({})])
    except ValueError:
        return HTTPException(status_code=404, detail="unknown")

    return data
