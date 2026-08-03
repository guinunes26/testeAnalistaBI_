import os
import shutil


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SOURCE_DIR = os.path.join(BASE_DIR, "spreadsheets")
RAW_DIR = os.path.join(BASE_DIR, "files", "raw")

print("Iniciando extração dos arquivos...")

for arquivo in os.listdir(SOURCE_DIR):

    if not arquivo.lower().endswith(".csv"):
        continue

    arquivo_origem = os.path.join(SOURCE_DIR, arquivo)
    arquivo_destino = os.path.join(RAW_DIR, arquivo)

    shutil.copy2(arquivo_origem, arquivo_destino)
    print(f"[OK] {arquivo}")

print("Extração concluída!")