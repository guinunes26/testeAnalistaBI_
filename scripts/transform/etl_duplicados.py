def executar(df):
    if {"cd_acao","dt_pregao"}.issubset(df.columns):
        df = df.drop_duplicates(
            subset=["cd_acao","dt_pregao"],
            keep="first"
        )
    else:
        df = df.drop_duplicates()
    return df