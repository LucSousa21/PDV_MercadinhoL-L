
import platform
import shutil
import zipfile
import os

from pathlib import Path, PurePosixPath

def remover_pasta_com_permissao(caminho):
    def corrigir_permissao(func, path, exc_info):
        import stat

        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(
        caminho,
        onerror=corrigir_permissao
    )

def preparar_atualizacao(arquivo_baixado):
    """
    Prepara a atualização em uma pasta temporária.
    Não substitui a instalação atual.
    """

    arquivo_baixado = Path(arquivo_baixado)

    if not arquivo_baixado.is_file():
        print("Arquivo de atualização não encontrado.")
        return None


    import tempfile

    pasta_temp = (
        Path(tempfile.gettempdir())
        / "PDV-Mercadinho-Staging"
    )

    pasta_temp.mkdir(parents=True, exist_ok=True)
    

    

    sistema = platform.system()

    try:

        # ==========================================
        # WINDOWS
        # ==========================================

        if sistema == "Windows":

            if arquivo_baixado.suffix.lower() != ".zip":
                raise ValueError("Arquivo Windows inválido.")

            destino = pasta_temp / "windows-update"

            if destino.exists():
                 remover_pasta_com_permissao(destino)
           
            destino.mkdir(parents=True)

            # Verificar integridade e caminhos do ZIP
            with zipfile.ZipFile(arquivo_baixado, "r") as pacote:

                erro = pacote.testzip()

                if erro:
                    raise ValueError(
                        f"Arquivo ZIP corrompido: {erro}"
                    )

                raiz = destino.resolve()

                for membro in pacote.infolist():

                    nome = membro.filename.replace("\\", "/")
                    caminho_relativo = PurePosixPath(nome)

                    if caminho_relativo.is_absolute() or ".." in caminho_relativo.parts:
                        raise ValueError(
                            f"Caminho inválido no ZIP: {nome}"
                        )

                    caminho = (destino / nome).resolve()

                    if not caminho.is_relative_to(raiz):
                        raise ValueError(
                            f"Caminho fora da pasta de destino: {nome}"
                        )

                pacote.extractall(destino)

            # Localizar o executável em qualquer subpasta
            executaveis = list(
                destino.rglob("PDV-Mercadinho.exe")
            )

            if not executaveis:
                raise FileNotFoundError(
                    "Executável Windows não encontrado no pacote."
                )

            executavel = executaveis[0]

            # Verificar se o version.json foi incluído
            versao = executavel.parent / "version.json"

            if not versao.is_file():
                raise FileNotFoundError(
                    "version.json não encontrado junto ao executável."
                )

            print("Atualização Windows preparada.")
            print(f"Executável: {executavel}")
            print(f"Versão: {versao}")

            return executavel.parent

        # ==========================================
        # LINUX
        # ==========================================

        elif sistema == "Linux":

            if arquivo_baixado.suffix.lower() != ".appimage":
                raise ValueError("Arquivo AppImage inválido.")

            destino = pasta_temp / "PDV-Mercadinho-Linux.AppImage"

            shutil.copy2(arquivo_baixado, destino)

            destino.chmod(0o755)

            if destino.stat().st_size == 0:
                raise ValueError("AppImage vazio.")

            print("Atualização Linux preparada.")

            return destino

        else:
            raise OSError(
                f"Sistema operacional não suportado: {sistema}"
            )

    except (
        OSError,
        zipfile.BadZipFile,
        ValueError,
        shutil.Error
    ) as erro:

        print(f"Erro ao preparar atualização: {erro}")

        return None
