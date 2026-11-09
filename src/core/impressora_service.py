
from src.service.impressao_cupom import ImpressaoCupom


class ImpressaoService:

    def __init__(self, impressora=None, largura_papel=80):
        self.impressora = impressora
        self.largura_papel = largura_papel

        self.cupom = ImpressaoCupom(
            impressora=impressora,
            largura_papel=largura_papel
        )

    def configurar_impressora(self, impressora):
        """
        Define a impressora que será utilizada.
        """

        self.impressora = impressora

        self.cupom.impressora = impressora

    def imprimir_venda(
            self,
            venda,
            pagamentos,
            valor_recebido,
            troco
    ):
            

        try:

            conteudo = self.cupom.imprimir(
                venda=venda,
                pagamentos=pagamentos,
                valor_recebido=valor_recebido,
                troco=troco
            )

            return {
                "sucesso": True,
                "mensagem": "Cupom preparado com sucesso.",
                "conteudo": conteudo
            }

        except Exception as erro:

            return {
                "sucesso": False,
                "mensagem": str(erro),
                "conteudo": None
            }