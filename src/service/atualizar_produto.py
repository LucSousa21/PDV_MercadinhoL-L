from src.database.criar_banco import SessionLocal
from src.model.models import Produto
from src.schemas.produtos import (
    ProdutoCreate,
    ProdutoResponse,
)


def atualizar_produto(
    produto_id: int,
    dados: ProdutoCreate,
) -> ProdutoResponse:

    with SessionLocal() as session:

        try:
            produto_bd = session.get(
                Produto,
                produto_id,
            )

            if produto_bd is None:
                raise ValueError(
                    "Produto não encontrado."
                )

            produto_bd.nome = dados.nome
            produto_bd.cd_barras = dados.cd_barras
            produto_bd.preco = dados.preco
            produto_bd.estoque = dados.estoque
            produto_bd.ativo = dados.ativo

            session.commit()
            session.refresh(produto_bd)

            return ProdutoResponse.model_validate(
                produto_bd
            )

        except Exception:
            session.rollback()
            raise