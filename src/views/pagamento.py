from decimal import Decimal, InvalidOperation

import customtkinter as ctk


class JanelaPagamento(ctk.CTkToplevel):
    """
    Tela de pagamento da venda.

    Permite:
        1 - Dinheiro
        2 - PIX
        3 - Débito
        4 - Crédito
        5 - Alimentação

    Também permite dividir o pagamento
    entre várias formas.
    """

    FORMAS_PAGAMENTO = {
        "1": "Dinheiro",
        "2": "PIX",
        "3": "Débito",
        "4": "Crédito",
        "5": "Alimentação",
    }

    def __init__(self, master, total, ao_confirmar):
        super().__init__(master)

        self.total = Decimal(str(total))
        self.ao_confirmar = ao_confirmar

        # Guarda os pagamentos realizados
        self.pagamentos = []

        # Valor utilizado para quitar a venda
        self.total_pago = Decimal("0.00")

        # Troco
        self.troco = Decimal("0.00")

        self.forma_pagamento = None

        self.title("Pagamento")

        # Janela maior
        self.geometry("900x700")
        self.minsize(850, 650)
        self.resizable(False, False)

        self.transient(master)

        self.attributes("-topmost", True)

        self.grab_set()

        self._criar_interface()
        self._configurar_teclado()
        self._mostrar_formas_pagamento()

        self.lift()
        self.focus_force()

    # ==========================================================
    # INTERFACE PRINCIPAL
    # ==========================================================

    def _criar_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.label_titulo = ctk.CTkLabel(
            self,
            text="FINALIZAR VENDA",
            font=ctk.CTkFont(
                size=32,
                weight="bold",
            ),
        )

        self.label_titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(25, 10),
        )

        self.label_total = ctk.CTkLabel(
            self,
            text=f"TOTAL: R$ {self.total:.2f}".replace(".", ","),
            font=ctk.CTkFont(
                size=32,
                weight="bold",
            ),
        )

        self.label_total.grid(
            row=1,
            column=0,
            padx=20,
            pady=5,
        )

        self.area = ctk.CTkFrame(
            self,
            corner_radius=12,
        )

        self.area.grid(
            row=2,
            column=0,
            padx=25,
            pady=15,
            sticky="nsew",
        )

        self.area.grid_columnconfigure(
            0,
            weight=1,
        )

    # ==========================================================
    # TECLADO
    # ==========================================================

    def _configurar_teclado(self):
        self.bind(
            "<Escape>",
            self._voltar,
        )

        self.bind(
            "<Key-1>",
            lambda event: self._tecla_forma("1"),
        )

        self.bind(
            "<Key-2>",
            lambda event: self._tecla_forma("2"),
        )

        self.bind(
            "<Key-3>",
            lambda event: self._tecla_forma("3"),
        )

        self.bind(
            "<Key-4>",
            lambda event: self._tecla_forma("4"),
        )

        self.bind(
            "<Key-5>",
            lambda event: self._tecla_forma("5"),
        )

    def _tecla_forma(self, numero):
        if self.forma_pagamento is None:
            self._selecionar_forma(numero)

    # ==========================================================
    # FORMAS DE PAGAMENTO
    # ==========================================================

    def _mostrar_formas_pagamento(self):
        self.forma_pagamento = None

        self._limpar_area()

        titulo = ctk.CTkLabel(
            self.area,
            text="ESCOLHA A FORMA DE PAGAMENTO",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )

        titulo.pack(
            pady=(30, 25),
        )

        frame_formas = ctk.CTkFrame(
            self.area,
            fg_color="transparent",
        )

        frame_formas.pack(
            fill="x",
            padx=25,
            pady=15,
        )

        for numero, nome in self.FORMAS_PAGAMENTO.items():

            frame_formas.grid_columnconfigure(
                int(numero) - 1,
                weight=1,
            )

            botao = ctk.CTkButton(
                frame_formas,
                text=f"{numero}\n{nome}",
                height=90,
                font=ctk.CTkFont(
                    size=17,
                    weight="bold",
                ),
                command=lambda n=numero: self._selecionar_forma(n),
            )

            botao.grid(
                row=0,
                column=int(numero) - 1,
                padx=5,
                pady=5,
                sticky="ew",
            )

        instrucoes = ctk.CTkLabel(
            self.area,
            text="Digite o número da opção ou clique no botão",
            font=ctk.CTkFont(
                size=16,
            ),
        )

        instrucoes.pack(
            pady=(25, 5),
        )

        esc = ctk.CTkLabel(
            self.area,
            text="ESC - Voltar",
            font=ctk.CTkFont(
                size=15,
            ),
        )

        esc.pack(
            pady=5,
        )

        self.lift()
        self.focus_force()

    def _selecionar_forma(self, numero):
        if numero not in self.FORMAS_PAGAMENTO:
            return

        self.forma_pagamento = self.FORMAS_PAGAMENTO[numero]

        self._mostrar_valor_pagamento()

    # ==========================================================
    # INFORMAR VALOR
    # ==========================================================

    def _mostrar_valor_pagamento(self):
        self._limpar_area()

        restante = self._valor_restante()

        titulo = ctk.CTkLabel(
            self.area,
            text=self.forma_pagamento.upper(),
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )

        titulo.pack(
            pady=(30, 10),
        )

        label_restante_texto = ctk.CTkLabel(
            self.area,
            text="VALOR QUE FALTA PAGAR",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        label_restante_texto.pack(
            pady=(5, 0),
        )

        label_restante = ctk.CTkLabel(
            self.area,
            text=f"R$ {restante:.2f}".replace(".", ","),
            font=ctk.CTkFont(
                size=36,
                weight="bold",
            ),
        )

        label_restante.pack(
            pady=(0, 15),
        )

        self.entry_valor = ctk.CTkEntry(
            self.area,
            height=60,
            font=ctk.CTkFont(
                size=27,
                weight="bold",
            ),
            justify="right",
        )

        self.entry_valor.pack(
            fill="x",
            padx=120,
            pady=15,
        )

        self.entry_valor.bind(
            "<Return>",
            self._adicionar_pagamento_teclado,
        )

        self.label_info = ctk.CTkLabel(
            self.area,
            text="Digite o valor e pressione ENTER.",
            font=ctk.CTkFont(
                size=16,
            ),
        )

        self.label_info.pack(
            pady=5,
        )

        botao = ctk.CTkButton(
            self.area,
            text="ADICIONAR PAGAMENTO [ENTER]",
            height=55,
            font=ctk.CTkFont(
                size=17,
                weight="bold",
            ),
            command=self._adicionar_pagamento,
        )

        botao.pack(
            fill="x",
            padx=120,
            pady=12,
        )

        botao_voltar = ctk.CTkButton(
            self.area,
            text="VOLTAR [ESC]",
            height=45,
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
            command=self._mostrar_formas_pagamento,
        )

        botao_voltar.pack(
            padx=120,
            pady=5,
        )

        self.entry_valor.focus_set()

        self.entry_valor.insert(
            0,
            f"{restante:.2f}",
        )

        self.entry_valor.select_range(
            0,
            "end",
        )

        self.lift()
        self.focus_force()

        self.entry_valor.focus_set()

    # ==========================================================
    # ADICIONAR PAGAMENTO
    # ==========================================================

    def _adicionar_pagamento_teclado(self, event=None):
        self._adicionar_pagamento()

    def _adicionar_pagamento(self):

        valor = self._obter_valor()

        if valor is None:
            self.label_info.configure(
                text="DIGITE UM VALOR VÁLIDO."
            )
            return

        if valor <= 0:
            self.label_info.configure(
                text="O VALOR DEVE SER MAIOR QUE ZERO."
            )
            return

        restante = self._valor_restante()

        # ======================================================
        # DINHEIRO
        # ======================================================

        if self.forma_pagamento == "Dinheiro":

            # Cliente entregou mais dinheiro
            if valor > restante:

                troco = valor - restante

                # IMPORTANTE:
                # Agora guardamos o valor REAL entregue
                # pelo cliente.
                self.pagamentos.append(
                    {
                        "forma": self.forma_pagamento,
                        "valor": valor,
                    }
                )

                # Para quitar a venda, somente o restante
                # entra no total_pago.
                self.total_pago += restante

                self.troco += troco

                self._finalizar_pagamento()

                return

        # ======================================================
        # OUTRAS FORMAS
        # ======================================================

        if valor > restante:

            self.label_info.configure(
                text=(
                    f"O VALOR MÁXIMO É "
                    f"R$ {restante:.2f}".replace(".", ",")
                )
            )

            return

        self.pagamentos.append(
            {
                "forma": self.forma_pagamento,
                "valor": valor,
            }
        )

        self.total_pago += valor

        restante = self._valor_restante()

        # ======================================================
        # PAGAMENTO COMPLETO
        # ======================================================

        if restante <= Decimal("0.00"):

            self._finalizar_pagamento()

            return

        # ======================================================
        # AINDA FALTA PAGAR
        # ======================================================

        self._mostrar_resumo_e_nova_forma()

    # ==========================================================
    # RESUMO DOS PAGAMENTOS PARCIAIS
    # ==========================================================

    def _mostrar_resumo_e_nova_forma(self):

        self._limpar_area()

        restante = self._valor_restante()

        titulo = ctk.CTkLabel(
            self.area,
            text="PAGAMENTO PARCIAL",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )

        titulo.pack(
            pady=(25, 10),
        )

        self._mostrar_pagamentos_realizados()

        label_pago = ctk.CTkLabel(
            self.area,
            text=(
                f"TOTAL PAGO: "
                f"R$ {self.total_pago:.2f}"
            ).replace(".", ","),
            font=ctk.CTkFont(
                size=21,
                weight="bold",
            ),
        )

        label_pago.pack(
            pady=(10, 5),
        )

        label_falta = ctk.CTkLabel(
            self.area,
            text=(
                f"AINDA FALTA: "
                f"R$ {restante:.2f}"
            ).replace(".", ","),
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )

        label_falta.pack(
            pady=(5, 15),
        )

        label = ctk.CTkLabel(
            self.area,
            text="ESCOLHA COMO PAGAR O RESTANTE",
            font=ctk.CTkFont(
                size=17,
                weight="bold",
            ),
        )

        label.pack(
            pady=(5, 10),
        )

        frame_formas = ctk.CTkFrame(
            self.area,
            fg_color="transparent",
        )

        frame_formas.pack(
            fill="x",
            padx=20,
            pady=5,
        )

        for numero, nome in self.FORMAS_PAGAMENTO.items():

            frame_formas.grid_columnconfigure(
                int(numero) - 1,
                weight=1,
            )

            botao = ctk.CTkButton(
                frame_formas,
                text=f"{numero}\n{nome}",
                height=70,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold",
                ),
                command=lambda n=numero: self._selecionar_forma(n),
            )

            botao.grid(
                row=0,
                column=int(numero) - 1,
                padx=4,
                pady=4,
                sticky="ew",
            )

        self.forma_pagamento = None

        self.lift()
        self.focus_force()

    def _mostrar_pagamentos_realizados(self):

        titulo = ctk.CTkLabel(
            self.area,
            text="PAGAMENTOS REALIZADOS",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        titulo.pack(
            pady=(5, 8),
        )

        for pagamento in self.pagamentos:

            texto = (
                f"{pagamento['forma']}: "
                f"R$ {pagamento['valor']:.2f}"
            ).replace(".", ",")

            label = ctk.CTkLabel(
                self.area,
                text=texto,
                font=ctk.CTkFont(
                    size=18,
                    weight="bold",
                ),
            )

            label.pack(
                pady=3,
            )

    # ==========================================================
    # FINALIZAR
    # ==========================================================

    def _finalizar_pagamento(self):

        self.grab_release()
        self.destroy()

        # valor_recebido agora representa o valor REAL
        # entregue pelos clientes.
        valor_recebido = sum(
            (
                pagamento["valor"]
                for pagamento in self.pagamentos
            ),
            Decimal("0.00"),
        )

        self.ao_confirmar(
            pagamentos=self.pagamentos,
            valor_recebido=valor_recebido,
            troco=self.troco,
        )

    # ==========================================================
    # UTILITÁRIOS
    # ==========================================================

    def _obter_valor(self):

        texto = self.entry_valor.get().strip()

        if not texto:
            return None

        texto = texto.replace(",", ".")

        try:
            return Decimal(texto)

        except InvalidOperation:
            return None

    def _valor_restante(self):

        restante = self.total - self.total_pago

        if restante < Decimal("0.00"):
            return Decimal("0.00")

        return restante

    def _limpar_area(self):

        for widget in self.area.winfo_children():
            widget.destroy()

    def _voltar(self, event=None):

        if self.forma_pagamento is not None:
            self._mostrar_formas_pagamento()
            return

        self.grab_release()
        self.destroy()