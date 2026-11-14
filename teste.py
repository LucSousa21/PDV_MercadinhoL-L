
import zipfile
import shutil
import traceback

from pathlib import Path

arquivo = (
    Path.home()
    / "AppData"
    / "Local"
    / "Temp"
    / "PDV-Mercadinho-Update"
    / "PDV-Mercadinho-Windows.zip"
)

destino = Path.home() / "PDV-Teste-Python"

try:
    print("ZIP:", arquivo)
    print("Existe:", arquivo.is_file())

    if destino.exists():
        shutil.rmtree(destino)

    destino.mkdir(parents=True)

    with zipfile.ZipFile(arquivo, "r") as pacote:
        print("Testando integridade...")
        print("Resultado:", pacote.testzip())

        print("Extraindo arquivos...")
        pacote.extractall(destino)

    executavel = (
        destino
        / "PDV-Mercadinho"
        / "PDV-Mercadinho.exe"
    )

    print("Executável encontrado:", executavel.is_file())

    if executavel.exists():
        print("Tamanho:", executavel.stat().st_size)

except Exception:
    traceback.print_exc()
