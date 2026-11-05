""" from src.database.criar_banco import SessionLocal
from src.model.models import Produto
from src.schemas.produtos import ProdutoResponse
from sqlalchemy import select, or_

def exibir_produto(info_produto: str) -> ProdutoResponse | None:

    with SessionLocal() as session:

        stmt = select(Produto).where(
            or_(
                Produto.cd_barras == info_produto,
                Produto.nome.ilike(f"%{info_produto}%")
            )
        )

        produto = session.scalars(stmt).first()

        if produto:
            return ProdutoResponse(
                id=produto.id,
                nome=produto.nome,
                cd_barras=produto.cd_barras,
                preco=produto.preco,
                estoque=produto.estoque,
                ativo=produto.ativo
            )

        return None

    session.close() """

from sqlalchemy import or_, select

from src.database.criar_banco import SessionLocal
from src.model.models import Produto
from src.schemas.produtos import ProdutoResponse


def exibir_produto(info_produto: str) -> ProdutoResponse | None:
    """
    Busca um produto pelo código de barras ou pelo nome.

    Apenas produtos ativos podem ser encontrados para venda.

    Retorna:
        ProdutoResponse se encontrar o produto.
        None se não encontrar.
    """

    if not info_produto or not info_produto.strip():
        return None

    info_produto = info_produto.strip()

    with SessionLocal() as session:

        stmt = select(Produto).where(
            Produto.ativo.is_(True),
            or_(
                Produto.cd_barras == info_produto,
                Produto.nome.ilike(f"%{info_produto}%")
            )
        )

        produto = session.scalars(stmt).first()

        if produto is None:
            return None

        return ProdutoResponse(
            id=produto.id,
            nome=produto.nome,
            cd_barras=produto.cd_barras,
            preco=produto.preco,
            estoque=produto.estoque,
            ativo=produto.ativo
        )