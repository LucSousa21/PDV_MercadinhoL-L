
import customtkinter as ctk
from tkinter import messagebox

from src.views.pdv import PDV
from src.core.updater_service import check_atualizacao, obter_versao_atual
from src.views.janela_atualizacao import perguntar_atualizacao

from src.core.updater_service import baixar_atualizacao
from src.core.installer import preparar_atualizacao



def verificar_atualizacoes(janela):
    resultado = check_atualizacao()

    if resultado is None:
        return

    if not resultado["atualizacao_disponivel"]:
        return

    aceitou = perguntar_atualizacao(
        janela,
        obter_versao_atual(),
        resultado["versao"]
    )

    if not aceitou:
        return

    # Baixar atualização
    arquivo = baixar_atualizacao(resultado["release"])

    if not arquivo:
        messagebox.showerror(
            "Erro na atualização",
            "Não foi possível baixar a atualização.\n\n"
            "O PDV continuará funcionando normalmente."
        )
        return

    # Preparar atualização
    preparado = preparar_atualizacao(arquivo)

    if not preparado:
        messagebox.showerror(
            "Erro na atualização",
            "Não foi possível preparar os arquivos.\n\n"
            "Sua versão atual foi preservada."
        )
        return

    messagebox.showinfo(
        "Atualização preparada",
        "O download foi concluído com sucesso!\n\n"
        "A atualização está preparada para instalação."
    )



def iniciar_pdv():

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("PDV Mercadinho")
    janela.geometry("1000x700")
    janela.minsize(800, 600)

    pdv = PDV(janela)
    pdv.pack(fill="both", expand=True)

    janela.after(
        2000,
        lambda: verificar_atualizacoes(janela)
    )

    janela.mainloop()
