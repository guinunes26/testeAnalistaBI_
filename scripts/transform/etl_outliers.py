import numpy as np

# Este script de Outliers é somente para o arquivo de cotações
# Regra usada para os Outliers é Calcular a mediana de cada

def executar(df, nome_arquivo):
    if nome_arquivo != "cotacoes_bolsa.csv":
        return df

    colunas = [
        "vl_abertura",
        "vl_maximo",
        "vl_minimo",
        "vl_medio",
        "vl_fechamento"
    ]
  
    if not set(colunas + ["cd_acao"]).issubset(df.columns):
        return df
    
    medianas = (
        df
        .groupby("cd_acao")[colunas]
        .transform("median")
    )

    fator = 10

    for coluna in colunas:

        df[coluna] = np.where(
            df[coluna] > medianas[coluna] * fator,
            np.nan,
            df[coluna]
        )

    return df