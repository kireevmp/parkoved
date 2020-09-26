from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import parse_obj_as

from ..db import services
from ..lib import with_auth
from ..typings.service import ServiceModel
from ..typings.token import TokenModel

router = APIRouter()


@router.get("/{park}", response_model=List[ServiceModel])
def get_services(park: str, token: TokenModel = Depends(with_auth)):
    try:
        serv = parse_obj_as(List[ServiceModel], [*services.find({"park": park})])
    except ValueError:
        return HTTPException(status_code=404, detail="park.notfound")

    return serv
