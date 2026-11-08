
import requests as rep
import os
import sys
import json
import platform
import tempfile
import hashlib

from pathlib import Path
from packaging import version


GITHUB_API = (
    "https://api.github.com/repos/"
    "LucSousa21/PDV_MercadinhoL-L/releases/latest"
)

ARQUIVOS_RELEASE = {
    "Windows": "PDV-Mercadinho-Windows.zip",
    "Linux": "PDV-Mercadinho-Linux.AppImage"
}


def caminho_version():
    """
    Localiza o version.json no desenvolvimento e na produção.
    """

    if getattr(sys, "frozen", False):

        # Linux AppImage
        if os.environ.get("APPIMAGE"):
            return Path(os.environ["APPIMAGE"]).resolve().parent / "version.json"

        # Windows PyInstaller
        return Path(sys.executable).resolve().parent / "version.json"

    # Desenvolvimento
    return Path(__file__).resolve().parents[2] / "version.json"


def obter_versao_atual():
    try:
        caminho = caminho_version()

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados["version"]

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as erro:
        print(f"Erro ao obter versão: {erro}")
        return None


def check_atualizacao():
    try:
        versao_atual = obter_versao_atual()

        if not versao_atual:
            return None

        response = rep.get(
            GITHUB_API,
            timeout=15,
            headers={"Accept": "application/vnd.github+json"}
        )

        response.raise_for_status()

        data = response.json()

        ultima_versao = data["tag_name"].lstrip("v")

        nova = version.parse(ultima_versao)
        atual = version.parse(versao_atual.lstrip("v"))

        if nova > atual:
            return {
                "atualizacao_disponivel": True,
                "versao": ultima_versao,
                "release": data
            }

        return {
            "atualizacao_disponivel": False,
            "versao": ultima_versao
        }

    except (rep.RequestException, KeyError, ValueError) as erro:
        print(f"Erro ao verificar atualização: {erro}")
        return None


def baixar_atualizacao(release):
    caminho_download = None

    try:
        sistema = platform.system()
        nome_arquivo = ARQUIVOS_RELEASE.get(sistema)

        if not nome_arquivo:
            return None

        assets = release.get("assets", [])

        asset = next(
            (item for item in assets if item["name"] == nome_arquivo),
            None
        )

        if not asset:
            print("Arquivo não encontrado na Release.")
            return None

        url = asset["browser_download_url"]
        tamanho_esperado = asset["size"]
        digest = asset.get("digest")

        pasta_temp = (
            Path(tempfile.gettempdir())
            / "PDV-Mercadinho-Update"
        )

        pasta_temp.mkdir(parents=True, exist_ok=True)

        caminho_download = pasta_temp / nome_arquivo

        sha256 = hashlib.sha256()
        tamanho_baixado = 0

        with rep.get(
            url,
            stream=True,
            timeout=(15, 120)
        ) as response:

            response.raise_for_status()

            with open(caminho_download, "wb") as arquivo:

                for bloco in response.iter_content(
                    chunk_size=1024 * 1024
                ):
                    if bloco:
                        arquivo.write(bloco)
                        sha256.update(bloco)
                        tamanho_baixado += len(bloco)

        if tamanho_baixado != tamanho_esperado:
            raise ValueError("Tamanho do download incorreto.")

        if digest and digest.startswith("sha256:"):
            hash_esperado = digest.split(":", 1)[1]

            if sha256.hexdigest().lower() != hash_esperado.lower():
                raise ValueError("Falha na validação SHA-256.")

        return caminho_download

    except (rep.RequestException, OSError, KeyError, ValueError) as erro:
        print(f"Erro ao baixar atualização: {erro}")

        if caminho_download and caminho_download.exists():
            caminho_download.unlink()

        return None
