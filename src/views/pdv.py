import customtkinter as ctk

from decimal import Decimal

from src.schemas.item_vendas import ItemVendaCreate
from src.service.venda_service import finalizar_venda
from src.service.consultar_produto import exibir_produto
from src.views.componentes import LinhaProduto
from src.views.pagamento import JanelaPagamento
from src.views.venda import VendaView
from src.core.updater_service import check_atualizacao
from src.views.janela_atualizacao import perguntar_atualizacao
from src.core.impressora_service import ImpressaoService


class PDV(ctk.CTkFrame):
    """
    Tela principal do caixa.
    """

    def __init__(self, master):
            
        super().__init__(master)

        self.venda = VendaView()
        self.quantidade_pendente = 1

        self.impressao_service = ImpressaoService()

        self._criar_interface()
        self._configurar_teclas()

        self.entry_codigo.focus_set()

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def _criar_interface(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._criar_cabecalho()
        self._criar_area_produto()
        self._criar_lista_itens()
        self._criar_rodape()

    def _criar_cabecalho(self):
        frame = ctk.CTkFrame(self)

        frame.grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 10),
            sticky="ew",
        )

        frame.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            frame,
            text="CAIXA",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )

        titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(15, 2),
            sticky="w",
        )

        subtitulo = ctk.CTkLabel(
            frame,
            text="PDV Mercadinho L&L",
            font=ctk.CTkFont(size=14),
        )

        subtitulo.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="w",
        )

    def _criar_area_produto(self):
        frame = ctk.CTkFrame(self)

        frame.grid(
            row=1,
            column=0,
            padx=15,
            pady=5,
            sticky="ew",
        )

        frame.grid_columnconfigure(0, weight=1)

        self.label_status = ctk.CTkLabel(
            frame,
            text="Passe o código de barras ou digite para buscar",
            font=ctk.CTkFont(size=16),
        )

        self.label_status.grid(
            row=0,
            column=0,
            padx=15,
            pady=(12, 5),
            sticky="w",
        )

        self.entry_codigo = ctk.CTkEntry(
            frame,
            placeholder_text="Código de barras ou nome do produto",
            height=45,
            font=ctk.CTkFont(size=18),
        )

        self.entry_codigo.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 12),
            sticky="ew",
        )

        self.entry_codigo.bind(
            "<Return>",
            self._adicionar_produto,
        )

    def _criar_lista_itens(self):
        frame = ctk.CTkFrame(self)

        frame.grid(
            row=2,
            column=0,
            padx=15,
            pady=5,
            sticky="nsew",
        )

        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        cabecalho = ctk.CTkLabel(
            frame,
            text="Itens da venda",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        cabecalho.grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="w",
        )

        self.lista = ctk.CTkScrollableFrame(frame)

        self.lista.grid(
            row=1,
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="nsew",
        )

    def _criar_rodape(self):
        frame = ctk.CTkFrame(self)

        frame.grid(
            row=3,
            column=0,
            padx=15,
            pady=(5, 15),
            sticky="ew",
        )

        frame.grid_columnconfigure(0, weight=1)

        atalhos = ctk.CTkLabel(
            frame,
            text=(
                "F2 Buscar  |  F4 Quantidade  |  "
                "F6 Remover  |  F8 Cancelar  |  F10 Pagar"
            ),
            font=ctk.CTkFont(size=13),
        )

        atalhos.grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="w",
        )

        self.label_total = ctk.CTkLabel(
            frame,
            text="TOTAL: R$ 0,00",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )

        self.label_total.grid(
            row=0,
            column=1,
            padx=20,
            pady=10,
        )

    
    # ==========================================================
    # TECLADO
    # ==========================================================

    def _configurar_teclas(self):
        janela = self.winfo_toplevel()

        janela.bind(
            "<F2>",
            self._f2_buscar,
        )

        janela.bind(
            "<F4>",
            self._f4_quantidade,
        )

        janela.bind(
            "<F6>",
            self._f6_remover,
        )

        janela.bind(
            "<F8>",
            self._f8_cancelar,
        )

        janela.bind(
            "<F10>",
            self._f10_pagamento,
        )

        janela.bind(
            "<Escape>",
            self._escape,
        )

    def _f2_buscar(self, event=None):
        self.entry_codigo.focus_set()

        self.entry_codigo.select_range(
            0,
            "end",
        )

        self.label_status.configure(
            text="Digite o código de barras ou nome do produto"
        )

    # ==========================================================
    # PRODUTOS
    # ==========================================================

    def _adicionar_produto(self, event=None):

        codigo = self.entry_codigo.get().strip()

        if not codigo:
            return

        produto = exibir_produto(codigo)

        if produto is None:
            self.label_status.configure(
                text="Produto não encontrado."
            )

            self.entry_codigo.select_range(
                0,
                "end",
            )

            return

        if produto.estoque <= 0:
            self.label_status.configure(
                text=f"Produto sem estoque: {produto.nome}"
            )

            self.entry_codigo.select_range(
                0,
                "end",
            )

            return

        quantidade = self.quantidade_pendente

        if produto.estoque < quantidade:
            self.label_status.configure(
                text=(
                    f"Estoque insuficiente. "
                    f"Disponível: {produto.estoque}"
                )
            )

            self.quantidade_pendente = 1

            self.entry_codigo.select_range(
                0,
                "end",
            )

            return

        self.venda.adicionar_item(
            produto_id=produto.id,
            nome=produto.nome,
            codigo_barras=produto.cd_barras,
            preco=Decimal(str(produto.preco)),
            quantidade=quantidade,
        )

        self.quantidade_pendente = 1

        self._atualizar_lista()

        self.entry_codigo.delete(
            0,
            "end",
        )

        self.entry_codigo.focus_set()

        self.label_status.configure(
            text="Passe o próximo produto"
        )

    # ==========================================================
    # LISTA
    # ==========================================================

    def _atualizar_lista(self):

        for widget in self.lista.winfo_children():
            widget.destroy()

        for indice, item in enumerate(self.venda.itens):

            LinhaProduto(
                master=self.lista,
                numero=indice + 1,
                nome=item.nome,
                quantidade=item.quantidade,
                preco=item.preco,
                subtotal=item.subtotal,
            ).pack(
                fill="x",
                padx=5,
                pady=3,
            )

        self._atualizar_total()

        self.after(
            50,
            self._rolar_para_baixo,
        )

    def _rolar_para_baixo(self):

        try:
            self.lista._parent_canvas.yview_moveto(1.0)

        except Exception:
            pass

    # ==========================================================
    # TOTAL
    # ==========================================================

    def _atualizar_total(self):

        total = self.venda.total

        self.label_total.configure(
            text=f"TOTAL: R$ {total:.2f}".replace(".", ",")
        )

    # ==========================================================
    # QUANTIDADE
    # ==========================================================

    def _f4_quantidade(self, event=None):

        janela = ctk.CTkInputDialog(
            text="Digite a quantidade:",
            title="Quantidade",
        )

        valor = janela.get_input()

        if valor is None:
            return

        try:
            quantidade = int(valor)

        except ValueError:
            self.label_status.configure(
                text="Quantidade inválida."
            )
            return

        if quantidade <= 0:
            self.label_status.configure(
                text="A quantidade deve ser maior que zero."
            )
            return

        self.quantidade_pendente = quantidade

        self.label_status.configure(
            text=f"Próximo produto: quantidade {quantidade}"
        )

        self.entry_codigo.focus_set()

    # ==========================================================
    # REMOVER ITEM
    # ==========================================================

    def _f6_remover(self, event=None):

        if self.venda.esta_vazia():

            self.label_status.configure(
                text="Não há produtos para remover."
            )

            return

        janela = ctk.CTkInputDialog(
            text="Digite o número do item para remover:",
            title="Remover item",
        )

        valor = janela.get_input()

        if valor is None:
            return

        try:
            indice = int(valor) - 1

        except ValueError:
            self.label_status.configure(
                text="Número de item inválido."
            )

            return

        try:
            self.venda.remover_item(indice)

        except IndexError:
            self.label_status.configure(
                text="Item não encontrado."
            )

            return

        self._atualizar_lista()

        self.label_status.configure(
            text="Item removido."
        )

        self.entry_codigo.focus_set()

    # ==========================================================
    # CANCELAR VENDA
    # ==========================================================

    def _f8_cancelar(self, event=None):

        if self.venda.esta_vazia():

            self.label_status.configure(
                text="Não há venda para cancelar."
            )

            return

        confirmar = ctk.CTkInputDialog(
            text="Digite SIM para cancelar a venda:",
            title="Cancelar venda",
        )

        resposta = confirmar.get_input()

        if resposta is None:
            return

        if resposta.strip().upper() != "SIM":
            return

        self.limpar_venda()

        self.label_status.configure(
            text="Venda cancelada. Caixa pronto para nova venda."
        )

    # ==========================================================
    # PAGAMENTO
    # ==========================================================

    def _f10_pagamento(self, event=None):

        if self.venda.esta_vazia():

            self.label_status.configure(
                text="Adicione pelo menos um produto."
            )

            return

        JanelaPagamento(
            master=self.winfo_toplevel(),
            total=self.venda.total,
            ao_confirmar=self._pagamento_confirmado,
        )

    # ==========================================================
    # PAGAMENTO CONFIRMADO
    # ==========================================================

    
    def _pagamento_confirmado(
            self,
            pagamentos,
            valor_recebido,
            troco,
    ):
            
        """
        Registra a venda e prepara a impressão do cupom.
        """

        total_venda = self.venda.total

        itens_venda = []

        for item in self.venda.itens:

            itens_venda.append(
                ItemVendaCreate(
                    produto_id=item.produto_id,
                    quantidade=item.quantidade,
                )
            )

        try:

            venda_registrada = finalizar_venda(
                itens=itens_venda,
            )

        except Exception as erro:

            self.label_status.configure(
                text=f"Erro ao registrar venda: {erro}"
            )

            return

    # ======================================================
    # PREPARAR CUPOM
    # ======================================================

        resultado_impressao = self.impressao_service.imprimir_venda(
            venda=venda_registrada,
            pagamentos=pagamentos,
            valor_recebido=valor_recebido,
            troco=troco,
        )

        # ======================================================
        # VERIFICAR RESULTADO
        # ======================================================

        if resultado_impressao["sucesso"]:

            print("\n========== CUPOM GERADO ==========\n")
            print(resultado_impressao["conteudo"])
            print("\n==================================\n")

        else:

            print(
                "Não foi possível preparar o cupom:",
                resultado_impressao["mensagem"]
            )

        # ======================================================
        # MOSTRAR RESUMO DO PAGAMENTO
        # ======================================================

        self._mostrar_resumo_pagamento(
            pagamentos=pagamentos,
            total=total_venda,
            valor_recebido=valor_recebido,
            troco=troco,
        )

        # ======================================================
        # LIMPAR VENDA
        # ======================================================

        self.limpar_venda()

        self.label_status.configure(
            text=(
                f"Venda #{venda_registrada.id} concluída. "
                f"Troco: R$ {troco:.2f}"
            ).replace(".", ",")
        )


    def _mostrar_resumo_pagamento(
        self,
        pagamentos,
        total,
        valor_recebido,
        troco,
    ):
        """
        Mostra uma janela grande com:

        - Total da venda
        - Cada forma de pagamento
        - Valor recebido
        - Troco
        """

        janela = ctk.CTkToplevel(
            self.winfo_toplevel()
        )

        janela.title(
            "Pagamento confirmado"
        )

        # Janela maior
        janela.geometry(
            "650x650"
        )

        janela.minsize(
            650,
            650,
        )

        janela.resizable(
            False,
            False,
        )

        janela.transient(
            self.winfo_toplevel()
        )

        janela.attributes(
            "-topmost",
            True,
        )

        janela.grab_set()

        # ======================================================
        # TÍTULO
        # ======================================================

        titulo = ctk.CTkLabel(
            janela,
            text="PAGAMENTO CONFIRMADO",
            font=ctk.CTkFont(
                size=32,
                weight="bold",
            ),
        )

        titulo.pack(
            pady=(30, 20),
        )

        # ======================================================
        # TOTAL DA VENDA
        # ======================================================

        label_total_titulo = ctk.CTkLabel(
            janela,
            text="TOTAL DA VENDA",
            font=ctk.CTkFont(
                size=19,
                weight="bold",
            ),
        )

        label_total_titulo.pack(
            pady=(5, 0),
        )

        label_total = ctk.CTkLabel(
            janela,
            text=f"R$ {total:.2f}".replace(".", ","),
            font=ctk.CTkFont(
                size=38,
                weight="bold",
            ),
        )

        label_total.pack(
            pady=(0, 20),
        )

        # ======================================================
        # FORMAS DE PAGAMENTO
        # ======================================================

        titulo_formas = ctk.CTkLabel(
            janela,
            text="FORMA(S) DE PAGAMENTO",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        )

        titulo_formas.pack(
            pady=(5, 10),
        )

        frame_pagamentos = ctk.CTkFrame(
            janela,
            corner_radius=10,
        )

        frame_pagamentos.pack(
            fill="x",
            padx=70,
            pady=5,
        )

        for pagamento in pagamentos:

            forma = pagamento["forma"]
            valor = Decimal(
                str(pagamento["valor"])
            )

            linha = ctk.CTkFrame(
                frame_pagamentos,
                fg_color="transparent",
            )

            linha.pack(
                fill="x",
                padx=20,
                pady=7,
            )

            label_forma = ctk.CTkLabel(
                linha,
                text=forma,
                font=ctk.CTkFont(
                    size=19,
                    weight="bold",
                ),
            )

            label_forma.pack(
                side="left",
            )

            label_valor = ctk.CTkLabel(
                linha,
                text=f"R$ {valor:.2f}".replace(
                    ".",
                    ",",
                ),
                font=ctk.CTkFont(
                    size=19,
                    weight="bold",
                ),
            )

            label_valor.pack(
                side="right",
            )

        # ======================================================
        # SEPARADOR
        # ======================================================

        separador = ctk.CTkFrame(
            janela,
            height=2,
        )

        separador.pack(
            fill="x",
            padx=70,
            pady=15,
        )

        # ======================================================
        # VALOR RECEBIDO
        # ======================================================

        label_recebido = ctk.CTkLabel(
            janela,
            text=(
                f"VALOR RECEBIDO: "
                f"R$ {valor_recebido:.2f}"
            ).replace(
                ".",
                ",",
            ),
            font=ctk.CTkFont(
                size=23,
                weight="bold",
            ),
        )

        label_recebido.pack(
            pady=5,
        )

        # ======================================================
        # TROCO
        # ======================================================

        label_troco = ctk.CTkLabel(
            janela,
            text=(
                f"TROCO: "
                f"R$ {troco:.2f}"
            ).replace(
                ".",
                ",",
            ),
            font=ctk.CTkFont(
                size=30,
                weight="bold",
            ),
        )

        label_troco.pack(
            pady=(5, 20),
        )

        # ======================================================
        # BOTÃO OK
        # ======================================================

        botao = ctk.CTkButton(
            janela,
            text="OK",
            height=55,
            width=240,
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
            command=janela.destroy,
        )

        botao.pack(
            pady=10,
        )

        janela.lift()
        janela.focus_force()

    # ==========================================================
    # ESC
    # ==========================================================

    def _escape(self, event=None):
        self.entry_codigo.focus_set()

    # ==========================================================
    # LIMPAR VENDA
    # ==========================================================

    def limpar_venda(self):
        """
        Limpa completamente a venda atual
        e prepara o caixa para uma nova venda.
        """

        # Limpa os itens
        self.venda.limpar()

        # Reseta quantidade
        self.quantidade_pendente = 1

        # Atualiza a lista
        self._atualizar_lista()

        # Limpa código
        self.entry_codigo.delete(
            0,
            "end",
        )

        # Volta foco
        self.entry_codigo.focus_set()

        # Garante total zerado
        self.label_total.configure(
            text="TOTAL: R$ 0,00"
        )
