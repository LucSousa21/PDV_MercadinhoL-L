
from sqlalchemy import select

from src.database.criar_banco import SessionLocal
from src.model.models import Produto


def consultar_estoque_baixo():
    """
    Retorna todos os produtos ativos
    com estoque menor ou igual a 5.
    """

    with SessionLocal() as session:

        stmt = (
            select(Produto)
            .where(
                Produto.ativo.is_(True),
                Produto.estoque <= 5,
            )
            .order_by(Produto.estoque.asc())
        )

        produtos = session.scalars(stmt).all()

        return produtos
