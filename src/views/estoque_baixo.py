
import customtkinter as ctk

from src.service.estoque_service import consultar_estoque_baixo


class JanelaEstoqueBaixo(ctk.CTkToplevel):
    """
    Janela que apresenta os produtos com estoque baixo.
    """

    def __init__(self, master):
        super().__init__(master)

        self.title("Alerta de Estoque Baixo")
        self.geometry("650x550")
        self.minsize(550, 450)

        self.transient(master)

        self._criar_interface()
        self._carregar_produtos()

        self.grab_set()
        self.focus_force()
                # Fechar janela com ENTER ou ESC
        self.bind("<Return>", lambda event: self.destroy())
        self.bind("<Escape>", lambda event: self.destroy())

    def _criar_interface(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Cabeçalho
        titulo = ctk.CTkLabel(
            self,
            text="⚠ ALERTA DE ESTOQUE",
            font=ctk.CTkFont(
                size=27,
                weight="bold",
            ),
            text_color="#E69B00",
        )

        titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(25, 5),
        )

        self.label_descricao = ctk.CTkLabel(
            self,
            text="Produtos com estoque abaixo do limite",
            font=ctk.CTkFont(size=14),
        )

        self.label_descricao.grid(
            row=0,
            column=0,
            pady=(75, 10),
        )

        # Lista de produtos
        self.lista = ctk.CTkScrollableFrame(
            self,
            label_text="Produtos que precisam de reposição",
        )

        self.lista.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="nsew",
        )

        self.lista.grid_columnconfigure(0, weight=1)

        # Rodapé
        self.label_total = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        self.label_total.grid(
            row=2,
            column=0,
            pady=10,
        )

        self.botao_fechar = ctk.CTkButton(
            self,
            text="CONTINUAR PARA O CAIXA",
            height=45,
            width=250,
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
            command=self.destroy,
        )

        self.botao_fechar.grid(
            row=3,
            column=0,
            padx=20,
            pady=(5, 20),
        )

    def _carregar_produtos(self):
        """
        Consulta e apresenta os produtos com estoque baixo.
        """

        try:
            produtos = consultar_estoque_baixo()

        except Exception as erro:

            ctk.CTkLabel(
                self.lista,
                text=f"Erro ao consultar estoque:\n{erro}",
                font=ctk.CTkFont(size=15),
                text_color="#E53935",
            ).pack(pady=30)

            self.label_total.configure(
                text="Não foi possível consultar o estoque."
            )

            return

        if not produtos:

            ctk.CTkLabel(
                self.lista,
                text="✓ Todos os produtos possuem estoque suficiente!",
                font=ctk.CTkFont(
                    size=18,
                    weight="bold",
                ),
                text_color="#2EAD62",
            ).pack(pady=40)

            self.label_total.configure(
                text="Nenhum produto precisa de reposição."
            )

            return

        for produto in produtos:

            self._criar_linha_produto(
                nome=produto.nome,
                estoque=produto.estoque,
            )

        self.label_total.configure(
            text=f"Total de produtos com estoque baixo: {len(produtos)}"
        )

    def _criar_linha_produto(self, nome, estoque):

        linha = ctk.CTkFrame(
            self.lista,
            corner_radius=10,
        )

        linha.pack(
            fill="x",
            padx=5,
            pady=5,
        )

        linha.grid_columnconfigure(0, weight=1)

        # Nome
        label_nome = ctk.CTkLabel(
            linha,
            text=nome,
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
            anchor="w",
        )

        label_nome.grid(
            row=0,
            column=0,
            padx=15,
            pady=12,
            sticky="w",
        )

        # Quantidade
        if estoque == 0:
            texto = "SEM ESTOQUE"
            cor = "#C62828"

        else:
            texto = f"{estoque} unidades"
            cor = "#E69B00"

        label_estoque = ctk.CTkLabel(
            linha,
            text=texto,
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
            text_color=cor,
        )

        label_estoque.grid(
            row=0,
            column=1,
            padx=15,
            pady=12,
        )
