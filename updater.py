
import os
import sys
import shutil
import platform
import subprocess
import json
import shlex

from pathlib import Path
from datetime import datetime


def aplicar_atualizacao(caminho_preparado):

    caminho_preparado = Path(caminho_preparado).resolve()
    sistema = platform.system()

    try:

        if not caminho_preparado.is_dir():
            raise FileNotFoundError(
                "Diretorio preparado nao encontrado."
            )

        # ==========================================
        # WINDOWS
        # ==========================================

        if sistema == "Windows":

            if not getattr(sys, "frozen", False):
                raise RuntimeError(
                    "A aplicacao precisa estar empacotada."
                )

            executaveis = list(
                caminho_preparado.rglob("PDV-Mercadinho.exe")
            )

            if not executaveis:
                raise FileNotFoundError(
                    "Novo executavel nao encontrado."
                )

            if len(executaveis) > 1:
                raise RuntimeError(
                    "Mais de um executavel encontrado."
                )

            executavel_novo = executaveis[0]
            pasta_nova = executavel_novo.parent

            # Validar versao
            arquivos_versao = [
                pasta_nova / "version.json",
                pasta_nova / "_internal" / "version.json"
            ]

            arquivo_versao = next(
                (p for p in arquivos_versao if p.is_file()),
                None
            )

            if arquivo_versao is None:
                raise FileNotFoundError(
                    "version.json nao encontrado."
                )

            with arquivo_versao.open(
                "r",
                encoding="utf-8"
            ) as arquivo:

                versao = json.load(arquivo)

                if not isinstance(versao, dict):
                    raise ValueError(
                        "version.json invalido."
                    )

            executavel_atual = Path(
                sys.executable
            ).resolve()

            pasta_instalacao = executavel_atual.parent

            if pasta_nova == pasta_instalacao:
                raise RuntimeError(
                    "Origem e destino sao iguais."
                )

            # Verificar se a origem possui os componentes
            # esperados da distribuicao PyInstaller.

            pasta_internal = pasta_nova / "_internal"

            if not pasta_internal.is_dir():
                raise FileNotFoundError(
                    "Pasta _internal nao encontrada."
                )

            # Todos os arquivos auxiliares ficam fora
            # da pasta que sera atualizada.

            pasta_auxiliar = caminho_preparado

            pasta_auxiliar.mkdir(
                parents=True,
                exist_ok=True
            )

            script = (
                pasta_auxiliar / "aplicar_windows.ps1"
            )

            backup = (
                pasta_auxiliar / "backup"
            )

            log = (
                pasta_auxiliar / "atualizacao_windows.log"
            )

            conteudo = r'''
param(
    [string]$Origem,
    [string]$Destino,
    [string]$PIDApp,
    [string]$Backup,
    [string]$Log
)

$ErrorActionPreference = "Stop"

$BackupCriado = $false
$DestinoCriado = $false
$AtualizacaoIniciada = $false

$ItensGerenciados = @(
    "PDV-Mercadinho.exe",
    "_internal",
    "version.json"
)

function Remover-Distribuicao {

    foreach ($Item in $ItensGerenciados) {

        $Caminho = Join-Path $Destino $Item

        if (Test-Path -LiteralPath $Caminho) {

            Remove-Item `
                -LiteralPath $Caminho `
                -Recurse `
                -Force
        }
    }
}

function Copiar-Distribuicao {

    foreach ($Item in $ItensGerenciados) {

        $Fonte = Join-Path $Origem $Item

        if (Test-Path -LiteralPath $Fonte) {

            Copy-Item `
                -LiteralPath $Fonte `
                -Destination $Destino `
                -Recurse `
                -Force
        }
    }
}

Start-Transcript -Path $Log -Append

try {

    Write-Output "=================================="
    Write-Output "INICIO DA ATUALIZACAO"
    Write-Output "Origem: $Origem"
    Write-Output "Destino: $Destino"
    Write-Output "=================================="

    # Validar origem

    if (!(Test-Path -LiteralPath $Origem -PathType Container)) {
        throw "Origem nao encontrada."
    }

    $ExecutavelNovo = Join-Path `
        $Origem "PDV-Mercadinho.exe"

    $InternalNovo = Join-Path `
        $Origem "_internal"

    if (!(Test-Path -LiteralPath $ExecutavelNovo -PathType Leaf)) {
        throw "Executavel novo nao encontrado."
    }

    if (!(Test-Path -LiteralPath $InternalNovo -PathType Container)) {
        throw "Pasta _internal nao encontrada."
    }

    # Validar version.json

    $VersaoRoot = Join-Path $Origem "version.json"
    $VersaoInternal = Join-Path $InternalNovo "version.json"

    if (
        !(Test-Path $VersaoRoot) -and
        !(Test-Path $VersaoInternal)
    ) {
        throw "version.json nao encontrado."
    }

    # Aguardar o fechamento completo do aplicativo

    Write-Output "Aguardando encerramento do PDV..."

    if ($PIDApp -match '^\d+$') {

        Wait-Process `
            -Id ([int]$PIDApp) `
            -ErrorAction SilentlyContinue
    }

    Write-Output "PDV encerrado."

    # Preparar destino

    if (!(Test-Path -LiteralPath $Destino)) {

        New-Item `
            -ItemType Directory `
            -Path $Destino `
            -Force |
            Out-Null

        $DestinoCriado = $true
    }

    # Criar backup da distribuicao anterior

    $TemInstalacao = $false

    foreach ($Item in $ItensGerenciados) {

        if (Test-Path -LiteralPath (Join-Path $Destino $Item)) {
            $TemInstalacao = $true
            break
        }
    }

    if ($TemInstalacao) {

        Write-Output "Criando backup..."

        New-Item `
            -ItemType Directory `
            -Path $Backup `
            -Force |
            Out-Null

        foreach ($Item in $ItensGerenciados) {

            $Fonte = Join-Path $Destino $Item

            if (Test-Path -LiteralPath $Fonte) {

                Copy-Item `
                    -LiteralPath $Fonte `
                    -Destination $Backup `
                    -Recurse `
                    -Force
            }
        }

        $BackupCriado = $true

        Write-Output "Backup concluido."
    }

    # Remover somente os componentes gerenciados
    # Os demais arquivos do usuario permanecem intactos.

    Write-Output "Removendo distribuicao anterior..."

    Remover-Distribuicao

    # Instalar nova distribuicao

    Write-Output "Instalando nova versao..."

    Copiar-Distribuicao

    $ExecutavelFinal = Join-Path `
        $Destino "PDV-Mercadinho.exe"

    if (!(Test-Path -LiteralPath $ExecutavelFinal -PathType Leaf)) {
        throw "Executavel final nao encontrado."
    }

    if (!(Test-Path -LiteralPath (Join-Path $Destino "_internal"))) {
        throw "Distribuicao incompleta."
    }

    $AtualizacaoIniciada = $true

    # Iniciar novo aplicativo

    Write-Output "Iniciando novo PDV..."

    $Processo = Start-Process `
        -FilePath $ExecutavelFinal `
        -WorkingDirectory $Destino `
        -PassThru

    Start-Sleep -Seconds 5

    $Processo.Refresh()

    if ($Processo.HasExited) {

        throw "Novo PDV encerrou durante a inicializacao. Codigo: $($Processo.ExitCode)"
    }

    Write-Output "Novo PDV iniciado."
    Write-Output "PID: $($Processo.Id)"
    Write-Output "ATUALIZACAO CONCLUIDA."

}
catch {

    Write-Output "ERRO NA ATUALIZACAO:"
    Write-Output $_

    if ($BackupCriado) {

        Write-Output "Restaurando backup..."

        try {

            Remover-Distribuicao

            foreach ($Item in $ItensGerenciados) {

                $Fonte = Join-Path $Backup $Item

                if (Test-Path -LiteralPath $Fonte) {

                    Copy-Item `
                        -LiteralPath $Fonte `
                        -Destination $Destino `
                        -Recurse `
                        -Force
                }
            }

            Write-Output "Backup restaurado."

            # Tentar iniciar a versao anterior

            $ExecutavelAnterior = Join-Path `
                $Destino "PDV-Mercadinho.exe"

            if (Test-Path -LiteralPath $ExecutavelAnterior) {

                Start-Process `
                    -FilePath $ExecutavelAnterior `
                    -WorkingDirectory $Destino
            }

        }
        catch {

            Write-Output "FALHA CRITICA NA RESTAURACAO:"
            Write-Output $_
        }
    }
    elseif ($DestinoCriado) {

        if (Test-Path -LiteralPath $Destino) {

            Remove-Item `
                -LiteralPath $Destino `
                -Recurse `
                -Force
        }
    }

    exit 1
}
finally {

    Stop-Transcript
}
'''

            script.write_text(
                conteudo,
                encoding="utf-8"
            )

            # Backup exclusivo para cada tentativa

            backup = backup / datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            # O auxiliar aguarda o encerramento deste processo.

            comando = [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script),
                "-Origem",
                str(pasta_nova),
                "-Destino",
                str(pasta_instalacao),
                "-PIDApp",
                str(os.getpid()),
                "-Backup",
                str(backup),
                "-Log",
                str(log)
            ]

            subprocess.Popen(
                comando,
                creationflags=(
                    subprocess.CREATE_NEW_PROCESS_GROUP |
                    subprocess.DETACHED_PROCESS
                ),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )

            print(
                "Atualizador Windows iniciado."
            )

            return True

        # ==========================================
        # LINUX
        # ==========================================

        elif sistema == "Linux":

            if caminho_preparado.suffix.lower() != ".appimage":
                raise ValueError(
                    "Arquivo AppImage invalido."
                )

            appimage_atual = os.environ.get("APPIMAGE")

            if not appimage_atual:
                raise RuntimeError(
                    "APPIMAGE nao encontrado."
                )

            appimage_atual = Path(
                appimage_atual
            ).resolve()

            if not appimage_atual.is_file():
                raise FileNotFoundError(
                    "AppImage atual nao encontrado."
                )

            if not os.access(
                appimage_atual.parent,
                os.W_OK
            ):
                raise PermissionError(
                    "Sem permissao para atualizar o AppImage."
                )

            if not os.access(
                caminho_preparado,
                os.R_OK
            ):
                raise PermissionError(
                    "Sem permissao para ler o novo AppImage."
                )

            if not os.access(
                caminho_preparado,
                os.X_OK
            ):
                raise PermissionError(
                    "Novo AppImage sem permissao de execucao."
                )

            if appimage_atual == caminho_preparado:
                raise RuntimeError(
                    "Origem e destino sao iguais."
                )

            temporario = appimage_atual.with_name(
                appimage_atual.name + ".novo"
            )

            backup_linux = appimage_atual.with_name(
                appimage_atual.name + ".backup"
            )

            script_linux = appimage_atual.with_name(
                appimage_atual.name + ".updater.sh"
            )

            # Preparar arquivo novo sem substituir o atual.

            shutil.copy2(
                caminho_preparado,
                temporario
            )

            temporario.chmod(0o755)

            if temporario.stat().st_size == 0:
                raise ValueError(
                    "Novo AppImage esta vazio."
                )

            # Script auxiliar independente do PDV.

            conteudo_linux = r'''#!/bin/sh

set -u

PID_APP="$1"
TEMPORARIO="$2"
ATUAL="$3"
BACKUP="$4"

# Esperar o aplicativo encerrar completamente.

while kill -0 "$PID_APP" 2>/dev/null; do
    sleep 0.5
done

# Preservar versao anterior.

if ! cp -p "$ATUAL" "$BACKUP"; then
    exit 1
fi

# Substituicao atomica no mesmo diretorio.

if ! mv -f "$TEMPORARIO" "$ATUAL"; then
    exit 1
fi

chmod 755 "$ATUAL"

# Iniciar nova versao.

"$ATUAL" &
NOVO_PID=$!

sleep 5

if kill -0 "$NOVO_PID" 2>/dev/null; then
    exit 0
fi

# Falha de inicializacao: restaurar.

mv -f "$BACKUP" "$ATUAL"
chmod 755 "$ATUAL"

"$ATUAL" >/dev/null 2>&1 &

exit 1
'''

            script_linux.write_text(
                conteudo_linux,
                encoding="utf-8"
            )

            script_linux.chmod(0o700)

            comando = [
                "/bin/sh",
                str(script_linux),
                str(os.getpid()),
                str(temporario),
                str(appimage_atual),
                str(backup_linux)
            ]

            subprocess.Popen(
                comando,
                start_new_session=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )

            print(
                "Atualizador Linux iniciado."
            )

            return True

        else:

            raise OSError(
                f"Sistema nao suportado: {sistema}"
            )

    except (
        OSError,
        ValueError,
        RuntimeError,
        shutil.Error,
        json.JSONDecodeError
    ) as erro:

        print(
            f"Erro ao aplicar atualizacao: {erro}"
        )

        return False
