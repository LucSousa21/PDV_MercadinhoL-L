""" from src.model.models import Cliente
from src.schemas.mov_estoque import MovimentacaoEstoqueCreate, MovimentacaoEstoqueResponse
from src.database.criar_banco import SessionLocal

def cadastrar_movimentacao(produto: MovimentacaoEstoqueCreate):
    session = SessionLocal()
    try:
        produto_bd = MovimentacaoEstoqueCreate(
            produto_id=produto.produto_id,
            quantidade=produto.quantidade,
            tipo=produto.tipo
        )
        session.add(produto_bd)
        session.commit()
        session.refresh(produto_bd)
    finally:
        session.close() """

from src.database.criar_banco import SessionLocal
from src.model.models import MovimentacaoEstoque
from src.schemas.mov_estoque import (
    MovimentacaoEstoqueCreate,
    MovimentacaoEstoqueResponse,
)


def cadastrar_movimentacao(
    movimentacao: MovimentacaoEstoqueCreate,
) -> MovimentacaoEstoqueResponse:
    """
    Registra uma movimentação de estoque no banco de dados.

    Retorna:
        MovimentacaoEstoqueResponse com os dados registrados.
    """

    with SessionLocal() as session:
        try:
            movimentacao_bd = MovimentacaoEstoque(
                produto_id=movimentacao.produto_id,
                quantidade=movimentacao.quantidade,
                tipo=movimentacao.tipo,
            )

            session.add(movimentacao_bd)
            session.commit()
            session.refresh(movimentacao_bd)

            return MovimentacaoEstoqueResponse.model_validate(
                movimentacao_bd
            )

        except Exception:
            session.rollback()
            raise