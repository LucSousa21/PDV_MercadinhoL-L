import customtkinter as ctk


class JanelaAdm(ctk.CTkToplevel):
    """
    Janela administrativa do sistema.

    As funções de cadastro e manutenção serão adicionadas
    posteriormente.
    """

    def __init__(self, master):
        super().__init__(master)

        self.title("Administração")
        self.geometry("800x600")
        self.minsize(700, 500)

        self.transient(master)

        self._criar_interface()

    def _criar_interface(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text="Administração",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )
        titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 15),
            sticky="w",
        )

        area = ctk.CTkFrame(self)
        area.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="nsew",
        )

        area.grid_columnconfigure(0, weight=1)
        area.grid_columnconfigure(1, weight=1)

        botao_produtos = ctk.CTkButton(
            area,
            text="Produtos",
            height=60,
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
            command=self._abrir_produtos,
        )
        botao_produtos.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky="ew",
        )

        botao_clientes = ctk.CTkButton(
            area,
            text="Clientes",
            height=60,
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
            command=self._abrir_clientes,
        )
        botao_clientes.grid(
            row=0,
            column=1,
            padx=20,
            pady=20,
            sticky="ew",
        )

    def _abrir_produtos(self):
        """
        Abre a tela de gerenciamento de produtos.
        """

        from src.views.produtos import JanelaProdutos

        JanelaProdutos(self)

    def _abrir_clientes(self):
        """
        Tela de clientes será implementada posteriormente.
        """

        janela = ctk.CTkToplevel(self)
        janela.title("Clientes")
        janela.geometry("500x300")
        janela.resizable(False, False)

        label = ctk.CTkLabel(
            janela,
            text="Cadastro de clientes\n"
                 "Será implementado posteriormente.",
            font=ctk.CTkFont(size=18),
            justify="center",
        )
        label.pack(
            expand=True,
            padx=20,
            pady=20,
        )