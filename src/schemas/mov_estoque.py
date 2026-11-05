from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MovimentacaoEstoqueCreate(BaseModel):
    produto_id: int
    quantidade: int
    tipo: str


class MovimentacaoEstoqueResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    tipo: str
    data: datetime

    model_config = ConfigDict(from_attributes=True)