""" from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.schemas.item_vendas import ItemVendaCreate, ItemVendaResponse


class VendaCreate(BaseModel):
    cliente_id: int | None = None
    itens: list[ItemVendaCreate]


class VendaResponse(BaseModel):
    id: int
    valor_total: Decimal
    data: datetime
    cliente_id: int | None
    itens: list[ItemVendaResponse]

    model_config = ConfigDict(from_attributes=True) """

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.item_vendas import (
    ItemVendaCreate,
    ItemVendaResponse,
)


class VendaCreate(BaseModel):
    cliente_id: int | None = None
    itens: list[ItemVendaCreate] = Field(min_length=1)


class VendaResponse(BaseModel):
    id: int
    valor_total: Decimal
    data: datetime
    cliente_id: int | None
    itens: list[ItemVendaResponse]

    model_config = ConfigDict(from_attributes=True)