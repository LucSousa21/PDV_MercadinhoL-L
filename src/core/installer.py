
import platform
import shutil
import zipfile

from pathlib import Path


def preparar_atualizacao(arquivo_baixado):
    """
    Prepara a atualização em uma pasta temporária.
    Não substitui a instalação atual.
    """

    arquivo_baixado = Path(arquivo_baixado)

    if not arquivo_baixado.exists():
        print("Arquivo de atualização não encontrado.")
        return None

    pasta_temp = Path.home() / ".pdv-update-staging"
    pasta_temp.mkdir(parents=True, exist_ok=True)

    sistema = platform.system()

    try:

        if sistema == "Windows":

            if arquivo_baixado.suffix.lower() != ".zip":
                raise ValueError("Arquivo Windows inválido.")

            destino = pasta_temp / "windows"

            if destino.exists():
                shutil.rmtree(destino)

            destino.mkdir(parents=True)

            # Verificar integridade do ZIP
            with zipfile.ZipFile(arquivo_baixado, "r") as pacote:

                erro = pacote.testzip()

                if erro:
                    raise ValueError(
                        f"Arquivo ZIP corrompido: {erro}"
                    )

                # Evitar extração de caminhos maliciosos
                raiz = destino.resolve()

                for membro in pacote.infolist():
                    caminho = (destino / membro.filename).resolve()

                    if not caminho.is_relative_to(raiz):
                        raise ValueError(
                            "O ZIP contém um caminho inválido."
                        )

                pacote.extractall(destino)

            executavel = destino / "PDV-Mercadinho" / "PDV-Mercadinho.exe"

            if not executavel.is_file():
                raise FileNotFoundError(
                    "Executável Windows não encontrado no pacote."
                )

            print("Atualização Windows preparada.")

            return destino

        elif sistema == "Linux":

            if arquivo_baixado.suffix.lower() != ".appimage":
                raise ValueError("Arquivo AppImage inválido.")

            destino = pasta_temp / "PDV-Mercadinho-Linux.AppImage"

            shutil.copy2(arquivo_baixado, destino)

            # Permitir execução do AppImage
            destino.chmod(0o755)

            if destino.stat().st_size == 0:
                raise ValueError("AppImage vazio.")

            print("Atualização Linux preparada.")

            return destino

        else:
            print("Sistema operacional não suportado.")
            return None

    except (OSError, zipfile.BadZipFile, ValueError) as erro:
        print(f"Erro ao preparar atualização: {erro}")
        return None
