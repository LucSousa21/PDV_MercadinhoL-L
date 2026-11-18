
import customtkinter as ctk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation

from src.schemas.produtos import ProdutoCreate
from src.service.cadastro_produto import cadastrar_produto

from src.service.consultar_produto import buscar_produto_por_codigo
from src.service.atualizar_produto import atualizar_produto

class CadastroProduto(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.produto_id = None
        self.modo_edicao = False

        self.title("Cadastro de Produto")
        self.geometry("550x620")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._criar_interface()

        # Atalho para fechar a janela
        self.bind("<Escape>", lambda event: self.destroy())

        # Começa diretamente no leitor de código
        self.after(200, self.codigo_entry.focus_set)

    def _criar_interface(self):

        # =====================================
        # CABEÇALHO
        # =====================================

        titulo = ctk.CTkLabel(
            self,
            text="Cadastro de Produto",
            font=("Arial", 25, "bold")
        )
        titulo.pack(pady=(25, 5))

        subtitulo = ctk.CTkLabel(
            self,
            text="Escaneie o código de barras para começar",
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 20))

        # =====================================
        # FORMULÁRIO
        # =====================================

        formulario = ctk.CTkFrame(self, fg_color="transparent")
        formulario.pack(fill="both", expand=True, padx=35)

        # CÓDIGO DE BARRAS
        ctk.CTkLabel(
            formulario,
            text="Código de barras",
            anchor="w"
        ).pack(fill="x", pady=(5, 5))

        self.codigo_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Passe o produto no leitor...",
            height=42
        )
        self.codigo_entry.pack(fill="x")

        # NOME
        ctk.CTkLabel(
            formulario,
            text="Nome do produto",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))

        self.nome_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite o nome do produto",
            height=42
        )
        self.nome_entry.pack(fill="x")

        # PREÇO
        ctk.CTkLabel(
            formulario,
            text="Preço de venda (R$)",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))

        self.preco_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 10,50",
            height=42
        )
        self.preco_entry.pack(fill="x")

        # ESTOQUE
        ctk.CTkLabel(
            formulario,
            text="Quantidade em estoque",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))

        self.estoque_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 50",
            height=42
        )
        self.estoque_entry.pack(fill="x")

        # PRODUTO ATIVO
        self.ativo_var = ctk.BooleanVar(value=True)

        self.ativo_check = ctk.CTkCheckBox(
            formulario,
            text="Produto ativo",
            variable=self.ativo_var
        )
        self.ativo_check.pack(anchor="w", pady=20)

        # =====================================
        # BOTÃO SALVAR
        # =====================================

        self.salvar_btn = ctk.CTkButton(
            formulario,
            text="SALVAR PRODUTO  [ENTER]",
            height=48,
            font=("Arial", 15, "bold"),
            command=self.salvar
        )
        self.salvar_btn.pack(fill="x", pady=(10, 5))

        # =====================================
        # NAVEGAÇÃO PELO ENTER
        # =====================================

        self.codigo_entry.bind(
            "<Return>",
            self.buscar_codigo
        )

        self.nome_entry.bind(
            "<Return>",
            lambda event: self.preco_entry.focus_set()
        )

        self.preco_entry.bind(
            "<Return>",
            lambda event: self.estoque_entry.focus_set()
        )

        self.estoque_entry.bind(
            "<Return>",
            lambda event: self.salvar_btn.focus_set()
        )

        self.salvar_btn.bind(
            "<Return>",
            lambda event: self.salvar()
        )

    def buscar_codigo(self, event=None):

        codigo = self.codigo_entry.get().strip()

        if not codigo:
            return

        produto = buscar_produto_por_codigo(codigo)

        if produto is None:

            self.produto_id = None
            self.modo_edicao = False

            self.nome_entry.delete(0, "end")
            self.preco_entry.delete(0, "end")
            self.estoque_entry.delete(0, "end")

            self.ativo_var.set(True)

            self.salvar_btn.configure(
                text="SALVAR PRODUTO [ENTER]",
                command=self.salvar,
            )

            self.nome_entry.focus_set()

            return

        # Produto encontrado
        self.produto_id = produto.id
        self.modo_edicao = True

        self.nome_entry.delete(0, "end")
        self.nome_entry.insert(0, produto.nome)

        self.preco_entry.delete(0, "end")
        self.preco_entry.insert(0, str(produto.preco))

        self.estoque_entry.delete(0, "end")
        self.estoque_entry.insert(0, str(produto.estoque))

        self.ativo_var.set(produto.ativo)

        self.salvar_btn.configure(
            text="ATUALIZAR PRODUTO [ENTER]",
            command=self.salvar,
        )

        self.nome_entry.focus_set()
    # =====================================
    # VALIDAÇÃO E CADASTRO
    # =====================================

    def salvar(self):

        codigo = self.codigo_entry.get().strip()
        nome = self.nome_entry.get().strip()
        preco_texto = self.preco_entry.get().strip()
        estoque_texto = self.estoque_entry.get().strip()

        # Verifica campos obrigatórios
        campos = [
            (codigo, self.codigo_entry),
            (nome, self.nome_entry),
            (preco_texto, self.preco_entry),
            (estoque_texto, self.estoque_entry)
        ]

        for valor, campo in campos:
            if not valor:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Preencha todos os campos antes de cadastrar.",
                    parent=self
                )
                campo.focus_set()
                return

        # Valida preço
        try:
            preco = Decimal(
                preco_texto.replace(",", ".")
            )

            if not preco.is_finite() or preco < 0:
                raise ValueError

        except (InvalidOperation, ValueError):
            messagebox.showerror(
                "Preço inválido",
                "Informe um preço válido e não negativo.",
                parent=self
            )
            self.preco_entry.focus_set()
            return

        # Valida estoque
        try:
            estoque = int(estoque_texto)

            if estoque < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Estoque inválido",
                "Informe uma quantidade inteira não negativa.",
                parent=self
            )
            self.estoque_entry.focus_set()
            return

        # =================================
        # CRIA OBJETO DO SCHEMA
        # =================================

        try:
            produto = ProdutoCreate(
                nome=nome,
                cd_barras=codigo,
                preco=preco,
                estoque=estoque,
                ativo=self.ativo_var.get()
            )

            
            if self.modo_edicao and self.produto_id is not None:

                atualizar_produto(
                    produto_id=self.produto_id,
                    dados=produto,
                )

                messagebox.showinfo(
                    "Atualização realizada",
                    f"Produto '{nome}' atualizado com sucesso!",
                    parent=self
                )

            else:

                cadastrar_produto(produto)

                messagebox.showinfo(
                    "Cadastro realizado",
                    f"Produto '{nome}' cadastrado com sucesso!",
                    parent=self
                )

            self.limpar_campos()


            self.limpar_campos()

        except Exception as erro:

            messagebox.showerror(
                "Erro ao cadastrar",
                f"Não foi possível cadastrar o produto.\n\n{erro}",
                parent=self
            )

    # =====================================
    # LIMPAR FORMULÁRIO
    # =====================================

    def limpar_campos(self):

        self.codigo_entry.delete(0, "end")
        self.nome_entry.delete(0, "end")
        self.preco_entry.delete(0, "end")
        self.estoque_entry.delete(0, "end")

        self.ativo_var.set(True)

        # Volta para o leitor
        self.codigo_entry.focus_set()

        self.produto_id = None
        self.modo_edicao = False

        self.salvar_btn.configure(
            text="SALVAR PRODUTO [ENTER]",
            command=self.salvar,
        )


def abrir_cadastro(parent):
    return CadastroProduto(parent)
