import customtkinter as ctk

from decimal import Decimal, InvalidOperation

from src.schemas.produtos import ProdutoCreate
from src.service.cadastro_produto import cadastrar_produto


class JanelaProdutos(ctk.CTkToplevel):
    """
    Tela administrativa para cadastro de produtos.
    """

    def __init__(self, master):
        super().__init__(master)

        self.title("Cadastro de Produtos")
        self.geometry("650x600")
        self.minsize(600, 550)

        self.transient(master)

        self._criar_interface()

    def _criar_interface(self):
        self.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text="Cadastro de Produto",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )
        titulo.grid(
            row=0,
            column=0,
            padx=30,
            pady=(25, 25),
        )

        formulario = ctk.CTkFrame(self)
        formulario.grid(
            row=1,
            column=0,
            padx=30,
            pady=5,
            sticky="ew",
        )

        formulario.grid_columnconfigure(0, weight=1)

        # ------------------------------------------------------
        # Nome
        # ------------------------------------------------------

        label_nome = ctk.CTkLabel(
            formulario,
            text="Nome do produto",
            anchor="w",
        )
        label_nome.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 5),
            sticky="w",
        )

        self.entry_nome = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: Arroz 5kg",
            height=40,
        )
        self.entry_nome.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 10),
            sticky="ew",
        )

        # ------------------------------------------------------
        # Código de barras
        # ------------------------------------------------------

        label_barras = ctk.CTkLabel(
            formulario,
            text="Código de barras",
            anchor="w",
        )
        label_barras.grid(
            row=2,
            column=0,
            padx=20,
            pady=(10, 5),
            sticky="w",
        )

        self.entry_barras = ctk.CTkEntry(
            formulario,
            placeholder_text="Código de barras",
            height=40,
        )
        self.entry_barras.grid(
            row=3,
            column=0,
            padx=20,
            pady=(0, 10),
            sticky="ew",
        )

        # ------------------------------------------------------
        # Preço
        # ------------------------------------------------------

        label_preco = ctk.CTkLabel(
            formulario,
            text="Preço de venda",
            anchor="w",
        )
        label_preco.grid(
            row=4,
            column=0,
            padx=20,
            pady=(10, 5),
            sticky="w",
        )

        self.entry_preco = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 25,50",
            height=40,
        )
        self.entry_preco.grid(
            row=5,
            column=0,
            padx=20,
            pady=(0, 10),
            sticky="ew",
        )

        # ------------------------------------------------------
        # Estoque
        # ------------------------------------------------------

        label_estoque = ctk.CTkLabel(
            formulario,
            text="Estoque inicial",
            anchor="w",
        )
        label_estoque.grid(
            row=6,
            column=0,
            padx=20,
            pady=(10, 5),
            sticky="w",
        )

        self.entry_estoque = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 100",
            height=40,
        )
        self.entry_estoque.grid(
            row=7,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="ew",
        )

        # ------------------------------------------------------
        # Status
        # ------------------------------------------------------

        self.label_status = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=14),
        )
        self.label_status.grid(
            row=2,
            column=0,
            padx=30,
            pady=(15, 5),
        )

        # ------------------------------------------------------
        # Botão
        # ------------------------------------------------------

        self.botao_cadastrar = ctk.CTkButton(
            self,
            text="Cadastrar produto",
            height=50,
            font=ctk.CTkFont(
                size=17,
                weight="bold",
            ),
            command=self._cadastrar,
        )
        self.botao_cadastrar.grid(
            row=3,
            column=0,
            padx=30,
            pady=(5, 25),
            sticky="ew",
        )

        self.entry_nome.focus_set()

    def _cadastrar(self):
        """
        Valida os campos e cadastra o produto.
        """

        nome = self.entry_nome.get().strip()
        codigo_barras = self.entry_barras.get().strip()
        texto_preco = self.entry_preco.get().strip()
        texto_estoque = self.entry_estoque.get().strip()

        # ------------------------------------------------------
        # Validação do nome
        # ------------------------------------------------------

        if not nome:
            self._mostrar_erro(
                "Informe o nome do produto."
            )
            self.entry_nome.focus_set()
            return

        # ------------------------------------------------------
        # Validação do código de barras
        # ------------------------------------------------------

        if not codigo_barras:
            self._mostrar_erro(
                "Informe o código de barras."
            )
            self.entry_barras.focus_set()
            return

        # ------------------------------------------------------
        # Validação do preço
        # ------------------------------------------------------

        texto_preco = texto_preco.replace(",", ".")

        try:
            preco = Decimal(texto_preco)
        except InvalidOperation:
            self._mostrar_erro(
                "Informe um preço válido."
            )
            self.entry_preco.focus_set()
            return

        if preco < 0:
            self._mostrar_erro(
                "O preço não pode ser negativo."
            )
            self.entry_preco.focus_set()
            return

        # ------------------------------------------------------
        # Validação do estoque
        # ------------------------------------------------------

        try:
            estoque = int(texto_estoque)
        except ValueError:
            self._mostrar_erro(
                "Informe um estoque válido."
            )
            self.entry_estoque.focus_set()
            return

        if estoque < 0:
            self._mostrar_erro(
                "O estoque não pode ser negativo."
            )
            self.entry_estoque.focus_set()
            return

        # ------------------------------------------------------
        # Criação do schema
        # ------------------------------------------------------

        produto = ProdutoCreate(
            nome=nome,
            cd_barras=codigo_barras,
            preco=preco,
            estoque=estoque,
            ativo=True,
        )

        # ------------------------------------------------------
        # Cadastro
        # ------------------------------------------------------

        try:
            cadastrar_produto(produto)

        except Exception as erro:
            self._mostrar_erro(
                f"Não foi possível cadastrar o produto.\n{erro}"
            )
            return

        self._mostrar_sucesso(
            "Produto cadastrado com sucesso!"
        )

        self._limpar_formulario()

    def _mostrar_erro(self, mensagem):
        self.label_status.configure(
            text=mensagem
        )

    def _mostrar_sucesso(self, mensagem):
        self.label_status.configure(
            text=mensagem
        )

    def _limpar_formulario(self):
        self.entry_nome.delete(0, "end")
        self.entry_barras.delete(0, "end")
        self.entry_preco.delete(0, "end")
        self.entry_estoque.delete(0, "end")

        self.entry_nome.focus_set()