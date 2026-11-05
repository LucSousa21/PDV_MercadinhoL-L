import customtkinter as ctk


# ==========================================================
# FONTES
# ==========================================================

FONTE_TITULO = ctk.CTkFont(
    size=28,
    weight="bold",
)

FONTE_SUBTITULO = ctk.CTkFont(
    size=18,
    weight="bold",
)

FONTE_NORMAL = ctk.CTkFont(
    size=15,
)

FONTE_PEQUENA = ctk.CTkFont(
    size=13,
)

FONTE_DESTAQUE = ctk.CTkFont(
    size=24,
    weight="bold",
)


# ==========================================================
# TAMANHOS
# ==========================================================

ALTURA_ENTRY = 45
ALTURA_BOTAO = 45
ALTURA_BOTAO_GRANDE = 55


# ==========================================================
# ESPAÇAMENTOS
# ==========================================================

PADRAO_X = 15
PADRAO_Y = 10


def configurar_aparencia():
    """
    Configura a aparência geral do sistema.
    """

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")