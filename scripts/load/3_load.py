import os
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

CLEAN_DIR = os.path.join(BASE_DIR, "files", "clean")
ENRICH_DIR = os.path.join(BASE_DIR, "files", "enrich")

os.makedirs(ENRICH_DIR, exist_ok=True)

print("=" * 60)
print("INICIANDO MODELAGEM DIMENSIONAL (STAR SCHEMA)")
print("=" * 60)


def ler_csv(nome_arquivo):
    caminho = os.path.join(CLEAN_DIR, nome_arquivo)
    return pd.read_csv(caminho, sep=";", encoding="utf-8-sig", dtype=str)

print("Lendo bases limpas...")
df_empresas = ler_csv("df_empresas.csv")
df_porte = ler_csv("empresas_porte.csv")
df_simples = ler_csv("empresas_simples.csv")
df_atividade = ler_csv("empresas_nivel_atividade.csv")
df_saude = ler_csv("empresas_saude_tributaria.csv")
df_bolsa = ler_csv("empresas_bolsa.csv")
df_cotacoes = ler_csv("cotacoes_bolsa.csv")


# PAdronizando as o cnpj, onde irei usá-lo com chaves nos futoros joins

for tabela in [df_empresas, df_porte, df_simples, df_atividade, df_saude, df_bolsa]:
    if "cnpj" in tabela.columns:
        tabela["cnpj"] = (
            tabela["cnpj"]
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.zfill(14) # Garante que todo CNPJ tenha 14 dígitos
        )


# Criando a dimensão empresas - dim_empresa.csv
print("\nCriando dim_empresas.csv...")

dim_empresa = df_empresas[[
    "cnpj", "dt_abertura", "de_cnae_principal", "de_ramo_atividade", 
    "de_setor", "endereco_municipio", "endereco_uf", "endereco_regiao", "situacao_cadastral"
]].copy()

dim_empresa = dim_empresa.merge(df_porte, on="cnpj", how="left")
dim_empresa = dim_empresa.merge(df_simples, on="cnpj", how="left")
dim_empresa = dim_empresa.merge(df_atividade, on="cnpj", how="left")
dim_empresa = dim_empresa.merge(df_saude, on="cnpj", how="left")

# removendo possiveis duplicidades
dim_empresa = dim_empresa.drop_duplicates(subset="cnpj")

# exportando dim_empresa.csv criada
dim_empresa.to_csv(os.path.join(ENRICH_DIR, "dim_empresas.csv"), sep=";", index=False, encoding="utf-8-sig")
print("[OK] dim_empresas.csv salvo.")

print("\nCriando dim_ativos.csv...")

# Primeiramente padronizando os nomes das colunas de CNPJ - 
if "tx_cnpj" in df_bolsa.columns:
    df_bolsa.rename(columns={"tx_cnpj": "cnpj"}, inplace=True)
elif "vl_cnpj" in df_bolsa.columns:
    df_bolsa.rename(columns={"vl_cnpj": "cnpj"}, inplace=True)

colunas_ativos = [
    "cd_acao_rdz", "cd_acao", "nm_empresa", 
    "setor_economico", "subsetor", "segmento", "cnpj"
]
colunas_ativos = [c for c in colunas_ativos if c in df_bolsa.columns]

dim_ativos = df_bolsa[colunas_ativos].copy()

# Removemos linhas que não tenham o código da ação
dim_ativos = dim_ativos.dropna(subset=["cd_acao_rdz"])

# removendo possiveis duplicidades
dim_ativos = dim_ativos.drop_duplicates(subset="cd_acao_rdz")

# exportando dim_ativos.csv criado
dim_ativos.to_csv(os.path.join(ENRICH_DIR, "dim_ativos.csv"), sep=";", index=False, encoding="utf-8-sig")
print("[OK] dim_ativos.csv salvo com a chave CNPJ.")


# Criando a fato cotacoes - fato_cotacoes.csv
print("\nCriando fato_cotacoes.csv...")

# Removendo colunas desnecessárias
colunas_remover = [
    "__index_level_0__", "created_at", "updated_at", 
    "tp_reg", "cd_bdi", "in_opc", "ft_cotacao", "vl_exec_opc", "vl_exec_moeda_corrente"
]
df_cotacoes = df_cotacoes.drop(columns=colunas_remover, errors="ignore")

# passando o nome "dt_pregao" para "data", para padronizar com a dim_calendario e evitar mais estapas no power query
if "dt_pregao" in df_cotacoes.columns:
    df_cotacoes.rename(columns={"dt_pregao": "data"}, inplace=True)

# exportando a fato_cotacoes.csv
df_cotacoes.to_csv(os.path.join(ENRICH_DIR, "fato_cotacoes.csv"), sep=";", index=False, encoding="utf-8-sig")
print("[OK] fato_cotacoes.csv salvo.")


# Relatório final

print("\n" + "=" * 60)
print("MAPA DE RELACIONAMENTOS (PARA CONFIGURAR NO POWER BI):")
print("=" * 60)
print("1. Na guia de relacionamentos, ligue:")
print("   Tabela [dim_empresas]  -> coluna 'cnpj'")
print("   Tabela [dim_ativos]    -> coluna 'cnpj'")
print("   (Sentido Único, 1 para Muitos)\n")
print("2. Depois, ligue:")
print("   Tabela [dim_ativos]    -> coluna 'cd_acao_rdz'")
print("   Tabela [fato_cotacoes] -> coluna 'cd_acao_rdz'")
print("   (Sentido Único, 1 para Muitos)")
print("=" * 60)