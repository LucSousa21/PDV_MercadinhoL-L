
import customtkinter as ctk
from tkinter import messagebox

from src.views.pdv import PDV
from src.core.updater_service import check_atualizacao, obter_versao_atual
from src.views.janela_atualizacao import perguntar_atualizacao

from src.core.updater_service import baixar_atualizacao
from src.core.installer import preparar_atualizacao

from updater import aplicar_atualizacao




""" def verificar_atualizacoes(janela):


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

    # ==========================================
    # 1. BAIXAR ATUALIZAÇÃO
    # ==========================================

    arquivo = baixar_atualizacao(resultado["release"])

    if not arquivo:
        messagebox.showerror(
            "Erro na atualização",
            "Não foi possível baixar a atualização.\n\n"
            "O PDV continuará funcionando normalmente.",
            parent=janela
        )
        return

    # ==========================================
    # 2. PREPARAR ATUALIZAÇÃO
    # ==========================================

    preparado = preparar_atualizacao(arquivo)

    if not preparado:
        messagebox.showerror(
            "Erro na atualização",
            "Não foi possível preparar os arquivos.\n\n"
            "Sua versão atual foi preservada.",
            parent=janela
        )
        return

    # ==========================================
    # 3. CONFIRMAR INSTALAÇÃO
    # ==========================================

    instalar = messagebox.askyesno(
        "Instalar atualização",
        "O download foi concluído e os arquivos foram preparados.\n\n"
        "Deseja fechar o PDV e instalar a nova versão agora?",
        parent=janela
    )

    if not instalar:
        messagebox.showinfo(
            "Atualização preparada",
            "A atualização foi baixada e preparada.\n"
            "Ela poderá ser instalada posteriormente.",
            parent=janela
        )
        return

    # ==========================================
    # 4. APLICAR ATUALIZAÇÃO
    # ==========================================

    sucesso = aplicar_atualizacao(preparado)

    if sucesso:
        # O aplicador precisa continuar trabalhando
        # independentemente da janela do PDV.
        janela.destroy()
        return

    messagebox.showerror(
        "Erro na atualização",
        "Não foi possível iniciar a instalação.\n\n"
        "O PDV continuará utilizando a versão atual.",
        parent=janela
    ) """




def iniciar_pdv():

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("PDV Mercadinho")
    # Abre em tela cheia
    janela.attributes("-fullscreen", True)

    pdv = PDV(janela)
    pdv.pack(fill="both", expand=True)

    """ janela.after(
        2000,
        lambda: verificar_atualizacoes(janela)
    ) """

    janela.mainloop()
