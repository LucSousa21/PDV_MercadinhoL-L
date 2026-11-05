""" from src.model.models import Produto
from src.schemas.produtos import ProdutoCreate, ProdutoResponse
from src.database.criar_banco import SessionLocal

def cadastrar_produto(produto: ProdutoCreate):
    session = SessionLocal()
    try:
        produto_bd = Produto(
            nome=produto.nome,
            cd_barras=produto.cd_barras,
            preco=produto.preco,
            estoque=produto.estoque,
            ativo=produto.ativo
        )
        session.add(produto_bd)
        session.commit()
        session.refresh(produto_bd)
    finally:
        session.close() """

from src.database.criar_banco import SessionLocal
from src.model.models import Produto
from src.schemas.produtos import (
    ProdutoCreate,
    ProdutoResponse,
)


def cadastrar_produto(
    produto: ProdutoCreate,
) -> ProdutoResponse:
    """
    Cadastra um produto no banco de dados.

    Retorna:
        ProdutoResponse com os dados do produto cadastrado.
    """

    with SessionLocal() as session:
        try:
            produto_bd = Produto(
                nome=produto.nome,
                cd_barras=produto.cd_barras,
                preco=produto.preco,
                estoque=produto.estoque,
                ativo=produto.ativo,
            )

            session.add(produto_bd)
            session.commit()
            session.refresh(produto_bd)

            return ProdutoResponse.model_validate(
                produto_bd
            )

        except Exception:
            session.rollback()
            raise