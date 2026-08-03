import pandas as pd

caminho = 'C:/Users/Nunes/Desktop/Teste/testeAnalistaBI/an_bi/files/raw/empresas_bolsa.csv'

df = pd.read_csv(
    caminho,
    sep=';',
    encoding='latin1'
)

print(df.head(100))


# cotacoes_bolsa.csv
# df_empresas.csv
# empresas_bolsa.csv
# empresas_nivel_atividade.csv
# empresas_porte.csv
# empresas_saude_tributaria.csv
# empresas_simples.csv