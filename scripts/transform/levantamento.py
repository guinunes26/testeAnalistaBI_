# a ideia do script é fazer um levantamento sobre as colunas e a schema de cada csv

import pandas as pd

caminho = 'C:/Users/Nunes/Desktop/Teste/testeAnalistaBI/an_bi/files/raw/empresas_simples.csv'

df = pd.read_csv(
    caminho,
    sep=';',
    encoding='latin1'
)

df.info()