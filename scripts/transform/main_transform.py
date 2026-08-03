import os
import pandas as pd

import etl_acentuacao
#import etl_decimal
import etl_tipos
import etl_nulos
import etl_duplicados
import etl_outliers
import etl_validacoes


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

RAW = os.path.join(BASE_DIR, "files", "raw")
CLEAN = os.path.join(BASE_DIR, "files", "clean")


for arquivo in os.listdir(RAW):

    if not arquivo.endswith(".csv"):
        continue

    print(f"Processando {arquivo}")

    arquivo_origem = os.path.join(RAW, arquivo)
    arquivo_destino = os.path.join(CLEAN, arquivo)

    df = pd.read_csv(
        arquivo_origem,
        sep=";",
        encoding="latin1"
    )

    df = etl_acentuacao.executar(df)
    df = etl_tipos.executar(df)
    df = etl_nulos.executar(df)
    df = etl_duplicados.executar(df)
    df = etl_outliers.executar(df, arquivo)
    df = etl_validacoes.executar(df)

    colunas_remover = [
        "__index_level_0__",
        "created_at",
        "updated_at"
    ]

    df = df.drop(
        columns=colunas_remover,
        errors="ignore"
    )

    # Padronizando os nomes
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
    )

    df.to_csv(
        arquivo_destino,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print(f"{arquivo} concluído.")
print("Transformação finalizada.")