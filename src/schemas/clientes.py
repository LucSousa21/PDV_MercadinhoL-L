from pydantic import BaseModel, ConfigDict


class ClienteCreate(BaseModel):
    nome: str
    email: str | None = None
    telefone: str | None = None
    


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str | None
    telefone: str | None
    

    model_config = ConfigDict(from_attributes=True)