import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import parse_obj_as, BaseModel, Field

from ..db import tickets, services
from ..lib import with_auth
from ..typings.service import ServiceModel
from ..typings.ticket import TicketModel
from ..typings.token import TokenModel

router = APIRouter()


@router.get("/", response_model=List[TicketModel], response_model_exclude={"_id"}, name="My Tickets")
def mine(token: TokenModel = Depends(with_auth)):
    try:
        data = parse_obj_as(List[TicketModel], [*tickets.find({"owner": token.id})])
    except ValueError:
        raise HTTPException(status_code=404, detail="user.notfound")

    return data


class PurchaseRequestModel(BaseModel):
    service: str = Field(
        description="Внутренний ID сервиса/аттракциона",
        max_length=16,
        min_length=16,
    )

    count: int = Field(
        description="Количество билетов",
        gt=0
    )

    isForChild: bool = Field(
        description="Является ли билет детским"
    )


@router.post("/", response_model_exclude={"_id"}, name="Purchase Ticket", status_code=201)
def purchase(token: TokenModel = Depends(with_auth), data: PurchaseRequestModel = Body(..., embed=False)):
    try:
        serv: ServiceModel = parse_obj_as(ServiceModel, services.find_one({"sid": data.service}))
    except ValueError as err:
        print(err)
        raise HTTPException(status_code=404, detail="service.notfound")

    ticket = TicketModel(service=data.service, uses=data.count, owner=token.id, isForChild=data.isForChild,
                         createdAt=time.time(), expiresAt=time.time() + serv.expireTime)

    tickets.insert_one(ticket.dict())

    return ticket
