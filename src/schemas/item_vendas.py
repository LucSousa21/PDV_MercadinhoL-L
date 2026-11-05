""" from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int


class ItemVendaResponse(BaseModel):
    id: int
    venda_id: int
    produto_id: int
    nome: str
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True) """

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class ItemVendaResponse(BaseModel):
    id: int
    venda_id: int
    produto_id: int
    nome: str
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)