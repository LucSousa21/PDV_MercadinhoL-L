from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProdutoCreate(BaseModel):
    nome: str
    cd_barras: str
    preco: Decimal
    estoque: int = 0
    ativo: bool = True


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    cd_barras: str
    preco: Decimal
    estoque: int
    ativo: bool
    model_config = ConfigDict(from_attributes=True)