
import os
import sys
import shutil
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.base import Base

# Registra os modelos no SQLAlchemy
from src.model.models import (
    Cliente,
    ItemVenda,
    Produto,
    Venda,
)


# =====================================================
# DIRETÓRIO DE DADOS MULTIPLATAFORMA
# =====================================================

def obter_diretorio_dados():
    """
    Retorna o diretório persistente do PDV
    de acordo com o sistema operacional.
    """

    if sys.platform == "win32":
        base = Path(
            os.environ.get(
                "LOCALAPPDATA",
                Path.home() / "AppData" / "Local"
            )
        )

        return base / "PDVMercadinho"

    if sys.platform.startswith("linux"):
        base = Path(
            os.environ.get(
                "XDG_DATA_HOME",
                Path.home() / ".local" / "share"
            )
        )

        return base / "pdv-mercadinho"

    raise OSError(
        f"Sistema operacional não suportado: {sys.platform}"
    )


APP_DATA_DIR = obter_diretorio_dados()

DATABASE_DIR = APP_DATA_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DB_PATH = DATABASE_DIR / "mercadinho.db"


# =====================================================
# MIGRAÇÃO DO BANCO ANTIGO
# =====================================================

LEGACY_DB_PATH = (
    Path(__file__).resolve().parent / "mercadinho.db"
)


def migrar_banco_antigo():
    """
    Copia o banco antigo para o novo diretório,
    somente se o banco definitivo ainda não existir.
    """

    if not DB_PATH.exists() and LEGACY_DB_PATH.exists():

        shutil.copy2(
            LEGACY_DB_PATH,
            DB_PATH
        )

        print("Banco antigo migrado com sucesso!")


migrar_banco_antigo()


# =====================================================
# CONEXÃO COM SQLITE
# =====================================================


engine = create_engine(
    f"sqlite:///{DB_PATH.as_posix()}",
    connect_args={
        "timeout": 30
    }
)

SessionLocal = sessionmaker(
    bind=engine
)


# =====================================================
# CRIAÇÃO DAS TABELAS
# =====================================================

def criar_banco():
    """Cria todas as tabelas do banco de dados."""

    Base.metadata.create_all(
        bind=engine
    )

    print("Banco de dados preparado com sucesso!")

    print(
        f"Localização: {DB_PATH}"
    )


if __name__ == "__main__":
    criar_banco()
