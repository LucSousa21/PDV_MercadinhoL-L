
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all
from pathlib import Path

# ==========================================
# ARQUIVOS DO PROJETO
# ==========================================

datas = []
binaries = []
hiddenimports = []

# Versionamento
if Path("version.json").exists():
    datas.append(("version.json", "."))

# ==========================================
# CUSTOMTKINTER
# ==========================================

ctk_datas, ctk_binaries, ctk_hidden = collect_all(
    "customtkinter"
)

datas += ctk_datas
binaries += ctk_binaries
hiddenimports += ctk_hidden

# ==========================================
# SQLALCHEMY
# ==========================================

sql_datas, sql_binaries, sql_hidden = collect_all(
    "sqlalchemy"
)

datas += sql_datas
binaries += sql_binaries
hiddenimports += sql_hidden

hiddenimports += [
    "sqlite3",
    "sqlalchemy.dialects.sqlite",
]

# ==========================================
# ASSETS
# ==========================================

if Path("assets").exists():
    datas.append(("assets", "assets"))

# ==========================================
# ANALYSIS
# ==========================================

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# ==========================================
# PYZ
# ==========================================

pyz = PYZ(a.pure)

# ==========================================
# EXECUTAVEL
# ==========================================

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PDV-Mercadinho",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

# ==========================================
# DISTRIBUICAO ONEDIR
# ==========================================

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="PDV-Mercadinho",
)
