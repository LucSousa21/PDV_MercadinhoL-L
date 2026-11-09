
from decimal import Decimal


class ImpressaoCupom:

    def __init__(self, impressora=None, largura_papel=80):
        self.impressora = impressora
        self.largura_papel = largura_papel

    def montar_cupom(
        self,
        venda,
        pagamentos,
        valor_recebido,
        troco
    ):
        """
        Monta o conteúdo textual do cupom
        utilizando os dados registrados no banco.
        """

        largura = 32 if self.largura_papel == 58 else 48

        linhas = []

        # CABEÇALHO
        linhas.append("MERCADINHO L&L".center(largura))
        linhas.append("=" * largura)

        linhas.append("COMPROVANTE DE VENDA".center(largura))

        linhas.append(f"Venda: {venda.id}")
        linhas.append(
            f"Data: {venda.data.strftime('%d/%m/%Y %H:%M')}"
        )

        linhas.append("=" * largura)

        # PRODUTOS
        for item in venda.itens:

            nome = item.nome

            quantidade = item.quantidade

            preco = Decimal(str(item.preco_unitario))

            subtotal = Decimal(str(item.subtotal))

            linhas.append(nome[:largura])

            linhas.append(
                f"{quantidade} x R$ {preco:.2f}"
            )

            linhas.append(
                f"Subtotal: R$ {subtotal:.2f}"
            )

        # TOTAL
        linhas.append("=" * largura)

        linhas.append(
            f"TOTAL: R$ {venda.valor_total:.2f}"
        )

        # PAGAMENTO
        linhas.append("-" * largura)

        linhas.append("PAGAMENTO".center(largura))

        for pagamento in pagamentos:

            valor = Decimal(str(pagamento["valor"]))

            linhas.append(
                f"{pagamento['forma']}: R$ {valor:.2f}"
            )

        linhas.append("-" * largura)

        linhas.append(
            f"Recebido: R$ {Decimal(str(valor_recebido)):.2f}"
        )

        linhas.append(
            f"Troco: R$ {Decimal(str(troco)):.2f}"
        )

        # RODAPÉ
        linhas.append("=" * largura)

        linhas.append(
            "OBRIGADO PELA PREFERENCIA!".center(largura)
        )

        return "\n".join(linhas)

    def imprimir(
        self,
        venda,
        pagamentos,
        valor_recebido,
        troco
    ):
        """
        Prepara o conteúdo para impressão.
        """

        return self.montar_cupom(
            venda=venda,
            pagamentos=pagamentos,
            valor_recebido=valor_recebido,
            troco=troco
        )
