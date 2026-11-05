import customtkinter as ctk

from src.views.pdv import PDV


def iniciar_pdv():
    """
    Inicia a aplicação do PDV.
    """

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("PDV Mercadinho")
    janela.geometry("1000x700")
    janela.minsize(800, 600)

    pdv = PDV(janela)
    pdv.pack(
        fill="both",
        expand=True,
    )

    janela.mainloop()