# 📊 Market Intelligence Dashboard – Empresas Listadas na B3

## Sobre o Projeto

O **Market Intelligence Dashboard** foi desenvolvido como parte de um desafio técnico, tendo como objetivo transformar dados brutos do mercado de capitais brasileiro em informações analíticas capazes de apoiar a tomada de decisão.

O projeto contempla todas as etapas de um fluxo moderno de Business Intelligence:

- Extração dos dados
- Tratamento (ETL)
- Modelagem Dimensional
- Construção do Dashboard no Power BI
- Storytelling Analítico

Todo o processo de preparação dos dados foi desenvolvido em **Python**, enquanto a camada analítica foi construída em **Power BI**, utilizando modelagem dimensional (Star Schema) e medidas DAX.

---

# Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Power BI
- DAX
- Modelagem Dimensional (Star Schema)

---

# Estrutura do Projeto

```
Projeto
│
├── spreadsheets/
│      Arquivos CSV originais
│
├── files/
│      ├── raw/
│      ├── clean/
│      └── enrich/
│
├── scripts/
│      1_extract.py
│      main_transform.py
│      3_load.py
│
└── Dashboard.pbix
```

---

# Pipeline ETL

O projeto foi dividido em três etapas principais.

---

## 1. Extract

Script:

```
1_extract.py
```

Objetivo

Copiar automaticamente todos os arquivos CSV da pasta **spreadsheets** para a pasta **raw**, criando uma camada de ingestão dos dados sem alterar os arquivos originais.

Nesta etapa foram realizados:

- leitura da pasta de origem;
- identificação automática dos arquivos CSV;
- cópia para a camada RAW.

---

## 2. Transform

Script principal

```
main_transform.py
```

Nesta etapa foram executadas diversas rotinas de limpeza e padronização dos dados.

### Correção de acentuação

```
etl_acentuacao.py
```

Corrige problemas de codificação provenientes de arquivos em Latin-1.

---

### Conversão de tipos

```
etl_tipos.py
```

Conversão de datas para formato datetime.

---

### Remoção de registros nulos

```
etl_nulos.py
```

Elimina registros completamente vazios.

---

### Remoção de duplicidades

```
etl_duplicados.py
```

Remoção de registros duplicados utilizando:

- Código da ação
- Data do pregão

---

### Tratamento de Outliers

```
etl_outliers.py
```

Aplicado exclusivamente ao arquivo de cotações.

Foi utilizada uma regra baseada na mediana de cada ativo.

Valores extremamente superiores (10 vezes a mediana do ativo) foram considerados inconsistentes e substituídos por valores nulos.

Campos tratados:

- Valor de abertura
- Valor máximo
- Valor mínimo
- Valor médio
- Valor de fechamento

---

### Validação dos registros

```
etl_validacoes.py
```

Aplicação de regras de consistência, como:

- Valor Máximo ≥ Valor Mínimo

---

### Padronização

Também foram realizadas:

- padronização dos nomes das colunas;
- remoção de colunas técnicas;
- exportação da camada CLEAN.

---

## 3. Load / Modelagem

Script

```
3_load.py
```

Nesta etapa foi construída toda a modelagem dimensional do projeto.

Foram geradas as seguintes tabelas:

### Dimensão Empresas

```
dim_empresas.csv
```

Informações cadastrais das empresas:

- CNPJ
- CNAE
- Porte
- Região
- Município
- UF
- Situação Cadastral
- Natureza Jurídica

---

### Dimensão Ativos

```
dim_ativos.csv
```

Informações dos ativos negociados:

- Ticker
- Empresa
- Setor Econômico
- Subsetor
- Segmento

---

### Fato Cotações

```
fato_cotacoes.csv
```

Tabela fato contendo:

- Data do pregão
- Abertura
- Máxima
- Mínima
- Fechamento
- Volume financeiro
- Quantidade de negócios

---

# Modelagem

Foi adotado um modelo Star Schema.

```
                          Dim Calendário
                                 │
                                 │
Dim Empresas ── Dim Ativos ── Fato Cotações
```

Relacionamentos:

- Dim Empresas → CNPJ
- Dim Ativos → CNPJ
- Dim Ativos → Código da Ação
- Fato Cotações → Código da Ação
  
- Fato Cotações -> Data
- Dim Calendario -> Data

---

# Dashboard

O dashboard foi desenvolvido seguindo princípios de Storytelling, conduzindo o usuário de uma visão macro do mercado até uma análise detalhada de uma empresa específica.

---

# Página Inicial

Objetivo

Apresentar o projeto e servir como ponto de navegação para as análises.

---

# Página 1 – Visão Geral do Mercado

Objetivo

Responder à pergunta:

> Como está o mercado?

Indicadores:

- Empresas analisadas
- Ativos negociados
- Preço médio de fechamento
- Volume financeiro
- Total de negócios
- Volatilidade média
- Volume médio diário

Principais análises:

- Evolução do preço médio das ações
- Liquidez do mercado
- Ranking dos setores econômicos

Filtros:

- Ano
- Empresa
- Setor Econômico
- Setor
- Subsetor

---

# Página 2 – Análise das Empresas

Objetivo

Responder:

> Quais empresas se destacaram no período?

Indicadores:

- Empresa destaque
- Maior rentabilidade
- Maior volume financeiro
- Preço médio de fechamento

Principais análises:

- Evolução do preço médio das empresas
- Ranking das empresas por volume financeiro
- Comparativo entre empresas

Filtros:

- Empresa
- Ano
- Mês

---

# Página 3 – Perfil da Empresa

Objetivo

Responder:

> Como uma empresa específica se comportou ao longo do período?

Indicadores:

- Empresa selecionada
- Ticker
- Setor Econômico
- Preço atual
- Volume financeiro

Principais análises:

### Histórico das Cotações

Gráfico Candlestick contendo:

- Abertura
- Fechamento
- Máxima
- Mínima

---

### Evolução Mensal do Volume Financeiro

Comparação mensal contendo:

- Volume Atual
- Volume do mês anterior
- MoM (%)

---

### Evolução do Preço Médio

Análise temporal da evolução do preço médio de fechamento.

Filtros:

- Empresa
- Ano
- Mês

---

# Storytelling Analítico

O dashboard foi desenvolvido seguindo uma narrativa de exploração dos dados.

```
Home

↓

Visão Geral do Mercado

↓

Análise das Empresas

↓

Perfil da Empresa
```

Essa estrutura permite ao usuário iniciar com uma visão macro do mercado, identificar empresas relevantes e, por fim, aprofundar a investigação em uma empresa específica.

---

# Diferenciais do Projeto

✔ Pipeline ETL desenvolvido em Python

✔ Separação das camadas RAW, CLEAN e ENRICH

✔ Tratamento automatizado de qualidade dos dados

✔ Modelagem Dimensional (Star Schema)

✔ Desenvolvimento de medidas DAX

✔ Dashboard orientado por Storytelling

✔ Layout responsivo e padronizado

✔ Navegação intuitiva entre páginas

✔ Análises executivas para apoio à tomada de decisão

---

# Autor

**Guilherme Silva**

Analista de Dados | Business Intelligence | Power BI | Python | SQL

