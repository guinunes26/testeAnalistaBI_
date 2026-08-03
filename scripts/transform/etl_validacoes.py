def executar(df):
    if {
        "vl_maximo",
        "vl_minimo",
        "vl_abertura"
    }.issubset(df.columns):
        df = df[
            df["vl_maximo"] >= df["vl_minimo"]
        ]
    return df