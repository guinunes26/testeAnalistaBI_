import pandas as pd


def executar(df):
    if "dt_pregao" in df.columns:
        df["dt_pregao"] = pd.to_datetime(
            df["dt_pregao"],
            format="%Y%m%d",
            errors="coerce"
        )
    return df