import customtkinter as ctk


class LinhaProduto(ctk.CTkFrame):
    """
    Linha visual de um produto dentro da lista do PDV.
    """

    def __init__(
        self,
        master,
        numero: int,
        nome: str,
        quantidade: int,
        preco,
        subtotal,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.label_produto = ctk.CTkLabel(
            self,
            text=f"{numero}. {nome}",
            font=ctk.CTkFont(size=15),
            anchor="w",
        )
        self.label_produto.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="ew",
        )

        self.label_quantidade = ctk.CTkLabel(
            self,
            text=f"Qtd: {quantidade}",
            font=ctk.CTkFont(size=15),
        )
        self.label_quantidade.grid(
            row=0,
            column=1,
            padx=15,
            pady=10,
        )

        self.label_preco = ctk.CTkLabel(
            self,
            text=f"R$ {preco:.2f}",
            font=ctk.CTkFont(size=15),
        )
        self.label_preco.grid(
            row=0,
            column=2,
            padx=15,
            pady=10,
        )

        self.label_subtotal = ctk.CTkLabel(
            self,
            text=f"R$ {subtotal:.2f}",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )
        self.label_subtotal.grid(
            row=0,
            column=3,
            padx=15,
            pady=10,
        )