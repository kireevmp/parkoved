from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import parse_obj_as, BaseModel

from ..db import services
from ..lib import with_auth
from ..typings.service import ServiceModel, ServiceType, ServicePosition
from ..typings.token import TokenModel

router = APIRouter()


class ChangeServiceModel(ServiceModel):
    sid: Optional[str]
    park: Optional[str]
    kind: Optional[ServiceType]
    name: Optional[str]
    expireTime: Optional[int]
    workingHours: Optional[str]
    ageLimit: Optional[int]
    priceAdults: Optional[int]
    priceChildren: Optional[Union[int, None]]
    pictures: Optional[List[str]]
    desc: Optional[str]
    longDesc: Optional[str]
    position: Optional[ServicePosition]


class ChangeServiceResponseModel(BaseModel):
    success: bool = True


@router.post("/", response_model=ChangeServiceResponseModel, name="Create Service")
def create_service(park: str = Query(...), service: ChangeServiceModel = Body(..., embed=False),
                   ):
    # TODO: add with_admin_auth
    services.insert_one({
        **service.dict(),
        "park": park
    })

    return {"success": True}


@router.put("/", response_model=ChangeServiceResponseModel, name="Update Service")
def update_service(service_id: str = Query(...),
                   service: ChangeServiceModel = Body(..., embed=False),
                   ):
    # TODO: add with_admin_auth
    services.update_one({"sid": service_id}, {"$set": {**service.dict(exclude_none=True)}})

    return {"success": True}


@router.get("/", response_model=List[ServiceModel])
def get_services(park: str = Query(...), token: TokenModel = Depends(with_auth)):
    try:
        serv = parse_obj_as(List[ServiceModel], [*services.find({"park": park})])
    except ValueError:
        raise HTTPException(status_code=404, detail="park.notfound")

    return serv
