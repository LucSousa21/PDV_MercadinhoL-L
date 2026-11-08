import requests as rep
import os
import json
from packaging import version
import platform

from version.json

GITHUB_API = "https://api.github.com/repos/LucSousa21/PDV_MercadinhoL-L/releases/latest"

def obter_versao_atual():
    try:
        caminho = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "version.json"
        )

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados["version"]

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as erro:
        print(f"Erro ao obter versão: {erro}")
        return None

VERSAO_ATUAL = obter_versao_atual()

def check_atualizacao():
    try:
        
        response = rep.get(GITHUB_API, timeout=15, headers={"Accept": "application/vnd.github+json"})

        response.raise_for_status()

        data = response.json()

        ultima_versao = data["tag_name"]

        if version.parse(ultima_versao) > version.parse(VERSAO_ATUAL):
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


def baixar_atualizacao():
    try:
       GITHUB_API = "https://api.github.com/repos/LucSousa21/PDV_MercadinhoL-L/releases/latest"

       response = rep.get(GITHUB_API)

       if response.status_code != 200:
           return False



def instalr_atualizacao():


{
  "tag_name": "v0.1.3",
  "name": "v0.1.3",
  "assets": [
    {
      "name": "PDV-Mercadinho-Windows.zip",
      "browser_download_url": "..."
    },
    {
      "name": "PDV-Mercadinho-Linux.AppImage",
      "browser_download_url": "..."
    }
  ]
}