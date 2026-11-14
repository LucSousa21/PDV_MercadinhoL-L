
import os
import sys
import shutil
import platform
import subprocess

from pathlib import Path


def aplicar_atualizacao(caminho_preparado):
    """
    Aplica a atualização preparada do PDV.

    Windows:
        Utiliza PowerShell auxiliar para substituir os arquivos
        depois que o aplicativo atual for encerrado.

    Linux:
        Substitui o AppImage atual pelo novo arquivo.
    """

    caminho_preparado = Path(caminho_preparado).resolve()

    sistema = platform.system()

    try:

        # ==========================================
        # WINDOWS
        # ==========================================

        if sistema == "Windows":

            executaveis = list(
                caminho_preparado.rglob("PDV-Mercadinho.exe")
        )

            if not executaveis:
                raise FileNotFoundError(
                    "Novo executável não encontrado."
                )

            executavel_novo = executaveis[0]

            pasta_nova = executavel_novo.parent

            

            versao = pasta_nova / "version.json"

            if not versao.is_file():
                raise FileNotFoundError(
                    "version.json não encontrado."
                )

            if not getattr(sys, "frozen", False):
                raise RuntimeError(
                    "A aplicação precisa estar empacotada para atualizar."
                )

            executavel_atual = Path(sys.executable).resolve()
            pasta_instalacao = executavel_atual.parent

            if executavel_novo.parent == pasta_instalacao:
                raise RuntimeError(
                    "A pasta de preparação não pode ser a instalação atual."
                )

            script = caminho_preparado / "aplicar_windows.ps1"

            backup = caminho_preparado / "backup"

            conteudo = r'''
param(
    [string]$Origem,
    [string]$Destino,
    [string]$Executavel,
    [int]$PIDApp,
    [string]$Backup
)

$ErrorActionPreference = "Stop"

try {

    # Aguarda o encerramento do aplicativo
    Wait-Process -Id $PIDApp -ErrorAction SilentlyContinue

    # Cria backup da instalação atual
    New-Item -ItemType Directory -Force -Path $Backup | Out-Null

    Copy-Item "$Destino\*" $Backup -Recurse -Force

    # Instala os novos arquivos
    Copy-Item "$Origem\*" $Destino -Recurse -Force

    # Inicia a nova versão
    Start-Process -FilePath $Executavel

}
catch {

    Write-Error $_

    # Tenta restaurar o backup
    if (Test-Path $Backup) {
        Copy-Item "$Backup\*" $Destino -Recurse -Force
    }

    exit 1
}
'''

            script.write_text(conteudo, encoding="utf-8")

            comando = [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", str(script),
                "-Origem", str(pasta_nova),
                "-Destino", str(pasta_instalacao),
                "-Executavel", str(executavel_novo),
                "-PIDApp", str(os.getpid()),
                "-Backup", str(backup)
            ]

            subprocess.Popen(
                comando,
                creationflags=(
                    subprocess.CREATE_NEW_PROCESS_GROUP |
                    subprocess.DETACHED_PROCESS
                ),
                close_fds=True
            )

            print("Aplicador Windows iniciado.")

            return True

        # ==========================================
        # LINUX
        # ==========================================

        elif sistema == "Linux":

            if caminho_preparado.suffix.lower() != ".appimage":
                raise ValueError("AppImage inválido.")

            appimage_atual = os.environ.get("APPIMAGE")

            if not appimage_atual:
                raise RuntimeError(
                    "Não foi possível localizar o AppImage atual."
                )

            appimage_atual = Path(appimage_atual).resolve()

            if not appimage_atual.is_file():
                raise FileNotFoundError(
                    "AppImage instalado não encontrado."
                )

            if not os.access(appimage_atual.parent, os.W_OK):
                raise PermissionError(
                    "Sem permissão para atualizar o AppImage."
                )

            temporario = appimage_atual.with_name(
                appimage_atual.name + ".novo"
            )

            try:
                shutil.copy2(caminho_preparado, temporario)

                temporario.chmod(0o755)

                if temporario.stat().st_size == 0:
                    raise ValueError("Novo AppImage está vazio.")

                os.replace(temporario, appimage_atual)

            finally:
                if temporario.exists():
                    temporario.unlink()

            print("AppImage atualizado com sucesso.")

            return True

        else:
            raise OSError(
                f"Sistema não suportado: {sistema}"
            )

    except (
        OSError,
        ValueError,
        RuntimeError,
        shutil.Error
    ) as erro:

        print(f"Erro ao aplicar atualização: {erro}")

        return False
