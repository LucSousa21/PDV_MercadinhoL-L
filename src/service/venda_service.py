""" from decimal import Decimal

from .consultar_produto import exibir_produto

from src.schemas.item_vendas import ItemVendaCreate
from src.schemas.vendas import VendaCreate
from src.service.registrar_venda import registrar_venda


def calcular_subtotal():

    # Lista que vai armazenar os itens da venda.
    item_list = []

    # Subtotal da compra.
    subtotal = Decimal("0.00")

    # ==========================================================
    # CADASTRO DO CLIENTE
    # ==========================================================

    try:
        cliente_id = int(
            input("Informe o cadastro do cliente: ")
        )
    except ValueError:
        cliente_id = None

    # ==========================================================
    # LEITURA DOS PRODUTOS
    # ==========================================================

    while True:

        cod_barras = input(
            "Digite o código de barras do produto "
            "(ou 'sair' para encerrar): "
        )

        # Encerra a leitura dos produtos.
        if cod_barras.lower() == "sair":
            break

        # Busca o produto pelo código de barras.
        produto = exibir_produto(cod_barras)

        if produto is None:
            print("Produto não encontrado.")
            continue

        # ======================================================
        # QUANTIDADE
        # ======================================================

        try:
            quantidade = int(
                input("Digite a quantidade do produto: ")
            )
        except ValueError:
            print("Digite uma quantidade válida.")
            continue

        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            continue

        # ======================================================
        # CRIA O ITEM DA VENDA
        # ======================================================

        item_venda = ItemVendaCreate(
            produto_id=produto.id,
            quantidade=quantidade
        )

        # Adiciona o item à lista da venda.
        item_list.append(item_venda)

        # ======================================================
        # CALCULA O SUBTOTAL
        # ======================================================

        resultado = produto.preco * quantidade

        subtotal += resultado

        print(
            f"{produto.nome} - "
            f"{quantidade} x R$ {produto.preco:.2f} = "
            f"R$ {resultado:.2f}"
        )

        print(
            f"Subtotal atual: R$ {subtotal:.2f}"
        )

    # ==========================================================
    # VERIFICA SE EXISTEM ITENS
    # ==========================================================

    if not item_list:
        print("Nenhum produto foi adicionado à venda.")
        return None

    # ==========================================================
    # CRIA A VENDA
    # ==========================================================

    venda_create = VendaCreate(
        cliente_id=cliente_id,
        itens=item_list
    )

    # ==========================================================
    # REGISTRA A VENDA NO BANCO
    # ==========================================================

    try:

        venda_registrada = registrar_venda(venda_create)

    except Exception as erro:

        print(
            f"Erro ao registrar a venda: {erro}"
        )

        return None

    # ==========================================================
    # VENDA CONCLUÍDA
    # ==========================================================

    print()
    print("Venda concluída, Obrigado, volte sempre!")

    print(
        f"Total da compra: "
        f"R$ {venda_registrada.valor_total:.2f}"
    )

    # ==========================================================
    # RECEBE O DINHEIRO DO CLIENTE
    # ==========================================================

    while True:

        try:

            valor_pago = Decimal(
                input("Digite o valor recebido: R$ ")
                .replace(",", ".")
            )

        except ValueError:

            print("Digite um valor válido.")
            continue

        # ======================================================
        # VERIFICA SE O VALOR É SUFICIENTE
        # ======================================================

        if valor_pago < venda_registrada.valor_total:

            faltante = (
                venda_registrada.valor_total
                - valor_pago
            )

            print(
                f"Valor insuficiente. "
                f"Faltam R$ {faltante:.2f}"
            )

            continue

        # ======================================================
        # CALCULA O TROCO
        # ======================================================

        troco = (
            valor_pago
            - venda_registrada.valor_total
        )

        print(
            f"Valor recebido: R$ {valor_pago:.2f}"
        )

        print(
            f"Troco: R$ {troco:.2f}"
        )

        break

    return venda_registrada """

from decimal import Decimal

from src.schemas.item_vendas import ItemVendaCreate
from src.schemas.vendas import VendaCreate
from src.service.consultar_produto import exibir_produto
from src.service.registrar_venda import registrar_venda


def buscar_produto(info_produto: str):
    """
    Busca um produto pelo código de barras ou pelo nome.

    Retorna:
        ProdutoResponse | None
    """

    if not info_produto or not info_produto.strip():
        return None

    return exibir_produto(info_produto.strip())


def criar_item_venda(
    produto,
    quantidade: int
) -> ItemVendaCreate:
    """
    Cria um item de venda a partir de um produto
    e de uma quantidade.
    """

    if quantidade <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    if produto.estoque < quantidade:
        raise ValueError(
            f"Estoque insuficiente para o produto "
            f"'{produto.nome}'. "
            f"Disponível: {produto.estoque}. "
            f"Solicitado: {quantidade}."
        )

    return ItemVendaCreate(
        produto_id=produto.id,
        quantidade=quantidade,
    )


def calcular_subtotal_item(
    produto,
    quantidade: int
) -> Decimal:
    """
    Calcula o subtotal de um único item.
    """

    if quantidade <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    return produto.preco * quantidade


def calcular_total(itens: list[dict]) -> Decimal:
    """
    Calcula o total dos itens exibidos no PDV.

    Cada item deve possuir:
        - preco
        - quantidade
    """

    total = Decimal("0.00")

    for item in itens:
        preco = Decimal(str(item["preco"]))
        quantidade = int(item["quantidade"])

        if quantidade <= 0:
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        total += preco * quantidade

    return total


def criar_venda(
    itens: list[ItemVendaCreate],
    cliente_id: int | None = None,
) -> VendaCreate:
    """
    Cria o objeto VendaCreate que será enviado
    para o serviço de registro da venda.
    """

    if not itens:
        raise ValueError(
            "Nenhum produto foi adicionado à venda."
        )

    return VendaCreate(
        cliente_id=cliente_id,
        itens=itens,
    )


def finalizar_venda(
    itens: list[ItemVendaCreate],
    cliente_id: int | None = None,
):
    """
    Finaliza o registro da venda no banco.

    O pagamento deve ser confirmado pelo PDV
    antes desta função ser chamada.

    Retorna:
        VendaResponse
    """

    venda = criar_venda(
        itens=itens,
        cliente_id=cliente_id,
    )

    return registrar_venda(venda)