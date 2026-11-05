""" from decimal import Decimal

from src.database.criar_banco import SessionLocal
from src.model.models import Produto, Venda, ItemVenda
from src.schemas.vendas import VendaCreate


def registrar_venda(venda: VendaCreate):
    session = SessionLocal()

    try:
        # Começa o total da venda em zero
        total_venda = Decimal("0.00")

        # Cria a venda
        # O valor_total será preenchido depois
        # que os itens forem calculados.
        venda_bd = Venda(
            cliente_id=venda.cliente_id,
            valor_total=Decimal("0.00")
        )

        # Percorre todos os itens enviados na VendaCreate
        for item in venda.itens:

            # Busca o produto pelo ID
            produto = session.get(
                Produto,
                item.produto_id
            )

            # Se o produto não existir, cancela a operação
            if produto is None:
                raise ValueError(
                    f"Produto {item.produto_id} não encontrado."
                )

            # Calcula o subtotal do item
            subtotal = (
                produto.preco * item.quantidade
            )

            # Cria o ItemVenda que será salvo no banco
            item_bd = ItemVenda(
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=produto.preco,
                subtotal=subtotal
            )

            # Associa o item à venda
            #
            # O SQLAlchemy vai cuidar do venda_id
            # através do relacionamento.
            venda_bd.itens.append(item_bd)

            # Soma o subtotal ao total da venda
            total_venda += subtotal

        # Depois de calcular todos os itens,
        # coloca o total na venda.
        venda_bd.valor_total = total_venda

        # Adiciona a venda à sessão.
        # Os ItemVenda associados também serão persistidos.
        session.add(venda_bd)

        # Salva tudo no banco.
        session.commit()

        # Atualiza o objeto com os dados gerados pelo banco.
        session.refresh(venda_bd)

        return venda_bd

    except Exception:
        # Se qualquer coisa der errado,
        # desfaz a transação.
        session.rollback()
        raise

    finally:
        # Fecha a conexão.
        session.close() """

from decimal import Decimal

from src.database.criar_banco import SessionLocal
from src.model.models import ItemVenda, Produto, Venda
from src.schemas.vendas import VendaCreate, VendaResponse


def registrar_venda(venda: VendaCreate) -> VendaResponse:
    """
    Registra uma venda no banco de dados.

    Responsabilidades:
        - validar os produtos;
        - validar o estoque;
        - criar a venda;
        - criar os itens da venda;
        - atualizar o estoque;
        - calcular o valor total;
        - salvar tudo em uma única transação.

    A função deve ser chamada somente depois
    que o pagamento tiver sido confirmado pelo PDV.
    """

    with SessionLocal() as session:
        try:
            total_venda = Decimal("0.00")

            venda_bd = Venda(
                cliente_id=venda.cliente_id,
                valor_total=Decimal("0.00"),
            )

            for item in venda.itens:
                produto = session.get(
                    Produto,
                    item.produto_id,
                )

                if produto is None:
                    raise ValueError(
                        f"Produto {item.produto_id} não encontrado."
                    )

                if item.quantidade <= 0:
                    raise ValueError(
                        "A quantidade do produto "
                        "deve ser maior que zero."
                    )

                if produto.estoque < item.quantidade:
                    raise ValueError(
                        f"Estoque insuficiente para o produto "
                        f"'{produto.nome}'. "
                        f"Disponível: {produto.estoque}. "
                        f"Solicitado: {item.quantidade}."
                    )

                subtotal = (
                    produto.preco *
                    item.quantidade
                )

                item_bd = ItemVenda(
                    produto_id=produto.id,
                    quantidade=item.quantidade,
                    preco_unitario=produto.preco,
                    subtotal=subtotal,
                )

                venda_bd.itens.append(item_bd)

                total_venda += subtotal

                produto.estoque -= item.quantidade

            venda_bd.valor_total = total_venda

            session.add(venda_bd)
            session.commit()
            session.refresh(venda_bd)

            return VendaResponse.model_validate(
                venda_bd
            )

        except Exception:
            session.rollback()
            raise