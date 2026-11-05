""" from src.model.models import Cliente
from src.schemas.clientes import ClienteCreate, ClienteResponse
from src.database.criar_banco import SessionLocal

def cadastrar_cliente(cliente: ClienteCreate):
    session = SessionLocal()
    try:
        cliente_bd = Cliente(
            nome=cliente.nome,
            email=cliente.email,
            telefone=cliente.telefone
        )
        session.add(cliente_bd)
        session.commit()
        session.refresh(cliente_bd)
    finally:
        session.close() """

from src.database.criar_banco import SessionLocal
from src.model.models import Cliente
from src.schemas.clientes import ClienteCreate, ClienteResponse


def cadastrar_cliente(cliente: ClienteCreate) -> ClienteResponse:
    """
    Cadastra um novo cliente no banco de dados.

    Retorna:
        ClienteResponse com os dados do cliente cadastrado.
    """

    with SessionLocal() as session:
        try:
            cliente_bd = Cliente(
                nome=cliente.nome,
                email=cliente.email,
                telefone=cliente.telefone
            )

            session.add(cliente_bd)
            session.commit()
            session.refresh(cliente_bd)

            return ClienteResponse.model_validate(cliente_bd)

        except Exception:
            session.rollback()
            raise