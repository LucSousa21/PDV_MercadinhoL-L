
import tkinter as tk
from tkinter import ttk


class JanelaAtualizacao(tk.Toplevel):

    def __init__(self, parent, versao_atual, nova_versao):
        super().__init__(parent)

        self.resultado = False

        self.title("Atualização do PDV")
        self.geometry("420x250")
        self.resizable(False, False)

        self.transient(parent)
        self.configure(bg="#F3F4F6")

        # Centralizar a janela
        self.update_idletasks()

        largura = 420
        altura = 250

        x = (self.winfo_screenwidth() - largura) // 2
        y = (self.winfo_screenheight() - altura) // 2

        self.geometry(f"{largura}x{altura}+{x}+{y}")

        # Impedir interação com a janela principal
        self.grab_set()

        # Ícone e título
        frame = tk.Frame(self, bg="#F3F4F6")
        frame.pack(fill="both", expand=True, padx=22, pady=18)

        tk.Label(
            frame,
            text="⬇",
            font=("Segoe UI", 28),
            fg="#16834A",
            bg="#F3F4F6"
        ).pack()

        tk.Label(
            frame,
            text="Nova atualização disponível!",
            font=("Segoe UI", 14, "bold"),
            fg="#222222",
            bg="#F3F4F6"
        ).pack(pady=(5, 8))

        tk.Label(
            frame,
            text=(
                f"Versão atual: {versao_atual}\n"
                f"Nova versão: {nova_versao}\n\n"
                "Deseja atualizar o PDV agora?"
            ),
            font=("Segoe UI", 10),
            fg="#444444",
            bg="#F3F4F6",
            justify="center"
        ).pack()

        # Área dos botões
        botoes = tk.Frame(frame, bg="#F3F4F6")
        botoes.pack(side="bottom", fill="x", pady=(15, 0))

        self.btn_sim = ttk.Button(
            botoes,
            text="Sim, atualizar",
            command=self.confirmar
        )

        self.btn_nao = ttk.Button(
            botoes,
            text="Não, depois",
            command=self.cancelar
        )

        self.btn_sim.pack(side="left", expand=True, padx=5)
        self.btn_nao.pack(side="right", expand=True, padx=5)

        # Navegação pelo teclado
        self.btn_sim.bind("<Left>", self.focar_nao)
        self.btn_sim.bind("<Right>", self.focar_nao)

        self.btn_nao.bind("<Left>", self.focar_sim)
        self.btn_nao.bind("<Right>", self.focar_sim)

        self.bind("<Return>", self.confirmar_teclado)
        self.bind("<Escape>", self.cancelar)

        # Fechar pelo X equivale a escolher Não
        self.protocol("WM_DELETE_WINDOW", self.cancelar)

        # Foco inicial na opção segura
        self.after(100, self.btn_nao.focus_set)

    def focar_sim(self, event=None):
        self.btn_sim.focus_set()
        return "break"

    def focar_nao(self, event=None):
        self.btn_nao.focus_set()
        return "break"

    def confirmar_teclado(self, event=None):
        widget = self.focus_get()

        if widget == self.btn_sim:
            self.confirmar()
        else:
            self.cancelar()

        return "break"

    def confirmar(self):
        self.resultado = True
        self.destroy()

    def cancelar(self):
        self.resultado = False
        self.destroy()


def perguntar_atualizacao(parent, versao_atual, nova_versao):

    janela = JanelaAtualizacao(
        parent,
        versao_atual,
        nova_versao
    )

    parent.wait_window(janela)

    return janela.resultado
