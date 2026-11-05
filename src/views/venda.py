from decimal import Decimal


class ItemVendaView:
    """
    Representa um item exibido na venda do PDV.

    Esta classe pertence à interface e não salva nada
    diretamente no banco de dados.
    """

    def __init__(
        self,
        produto_id: int,
        nome: str,
        codigo_barras: str,
        preco: Decimal,
        quantidade: int = 1,
    ):
        self.produto_id = produto_id
        self.nome = nome
        self.codigo_barras = codigo_barras
        self.preco = Decimal(str(preco))
        self.quantidade = quantidade

    @property
    def subtotal(self) -> Decimal:
        """
        Retorna o subtotal deste item.
        """

        return self.preco * self.quantidade


class VendaView:
    """
    Representa a venda que está sendo montada no caixa.

    A venda só existe na memória enquanto o operador
    está passando os produtos.
    """

    def __init__(self):
        self.itens: list[ItemVendaView] = []

    @property
    def total(self) -> Decimal:
        """
        Calcula o valor total da venda.
        """

        total = Decimal("0.00")

        for item in self.itens:
            total += item.subtotal

        return total

    def adicionar_item(
        self,
        produto_id: int,
        nome: str,
        codigo_barras: str,
        preco: Decimal,
        quantidade: int = 1,
    ):
        """
        Adiciona uma nova passagem de produto à venda.

        Mesmo que o produto já exista na venda,
        uma nova linha será criada.
        """

        if quantidade <= 0:
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        item = ItemVendaView(
            produto_id=produto_id,
            nome=nome,
            codigo_barras=codigo_barras,
            preco=preco,
            quantidade=quantidade,
        )

        self.itens.append(item)

    def remover_item(self, indice: int):
        """
        Remove um item pelo índice.
        """

        if indice < 0 or indice >= len(self.itens):
            raise IndexError(
                "Índice de item inválido."
            )

        self.itens.pop(indice)

    def limpar(self):
        """
        Cancela a venda atual e remove todos os itens.
        """

        self.itens.clear()

    def esta_vazia(self) -> bool:
        """
        Informa se não existem itens na venda.
        """

        return len(self.itens) == 0