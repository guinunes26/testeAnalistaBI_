def executar(df):

    def corrigir(valor):
        if isinstance(valor, str):
            try:
                return valor.encode("latin1").decode("utf-8")
            except:
                return valor
        return valor
    for coluna in df.select_dtypes(include="object"):
        df[coluna] = df[coluna].apply(corrigir)

    return df