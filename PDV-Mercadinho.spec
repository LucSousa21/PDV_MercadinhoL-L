
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all
from pathlib import Path

datas = [
    ("version.json", "."),
]

binaries = []
hiddenimports = []

# CustomTkinter
ctk_datas, ctk_binaries, ctk_hidden = collect_all(
    "customtkinter"
)

datas += ctk_datas
binaries += ctk_binaries
hiddenimports += ctk_hidden

# SQLAlchemy
sql_datas, sql_binaries, sql_hidden = collect_all(
    "sqlalchemy"
)

datas += sql_datas
binaries += sql_binaries
hiddenimports += sql_hidden

# Assets
if Path("assets").exists():
    datas.append(("assets", "assets"))

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

pyz = PYZ(a.pure)

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

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="PDV-Mercadinho",
)
