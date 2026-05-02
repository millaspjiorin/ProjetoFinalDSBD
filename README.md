# Pipeline de Dados e Previsão de Gastos Públicos (Brasil – 2026)

Este projeto tem como objetivo a construção de um pipeline de dados para análise e previsão dos gastos públicos federais brasileiros, com foco no comportamento desses gastos em anos eleitorais, especialmente em 2026.

A solução integra etapas de engenharia de dados e ciência de dados, utilizando ferramentas open source para ingestão, armazenamento, transformação e modelagem de dados provenientes do Portal da Transparência.

---

# Problema de Negócio

Os gastos públicos federais podem apresentar variações ao longo do tempo, especialmente em períodos eleitorais. A literatura econômica denomina esse fenômeno como Political Budget Cycle, ou Ciclo Político Orçamentário, no qual governos tendem a ampliar gastos com maior visibilidade junto ao eleitorado.

No contexto brasileiro, a análise e previsão desses gastos apresentam desafios como:

- grande volume de dados;
- diferentes níveis de granularidade das informações;
- necessidade de padronização e tratamento dos dados;
- preparação de bases adequadas para análises e modelos preditivos.

---

# Solução Proposta

O projeto propõe a construção de um pipeline de dados que:

- realiza ingestão automatizada de dados via API do Portal da Transparência;
- grava a camada bronze em Apache Iceberg com arquivos Parquet;
- utiliza DuckDB como motor analítico local;
- utiliza dbt para construção das camadas prata e ouro;
- prepara dados para análise exploratória, criação de métricas e modelagem preditiva;
- possibilita a previsão de gastos públicos para o ano eleitoral de 2026.

---

# Escopo da Análise

A análise considera os gastos públicos federais no âmbito do Poder Executivo Federal, por concentrar políticas públicas com maior possibilidade de variação em períodos eleitorais e maior aderência ao objetivo do projeto.

O escopo considera duas dimensões principais dos gastos públicos:

- despesas por órgão;
- despesas por funcional-programática.

Essas perspectivas permitem observar tanto a distribuição institucional dos gastos quanto sua finalidade orçamentária.

---

# Fontes de Dados

Os dados são obtidos por meio da API do Portal da Transparência.

Endpoints utilizados:

    /api-de-dados/despesas/por-orgao

    /api-de-dados/despesas/por-funcional-programatica

As consultas retornam dados agregados, sendo o volume dependente dos filtros aplicados e sujeito a atualizações contínuas.

---

# Estratégia de Análise

Para apoiar a análise, os dados são organizados em grupos analíticos.

## Análise por órgãos

Os órgãos do Poder Executivo foram agrupados conforme o tipo de impacto potencial de seus gastos:

- núcleo eleitoral: saúde, educação, assistência social e previdência;
- infraestrutura: transportes, cidades, integração regional e energia;
- coordenação política: fazenda, planejamento, presidência e justiça.

## Análise por funções orçamentárias

As funções orçamentárias foram agrupadas com base na literatura sobre ciclos políticos de gastos:

- gastos com maior visibilidade ao eleitor: saúde, educação e assistência social;
- investimentos públicos: transporte, urbanismo e agricultura;
- gastos estruturais: defesa, segurança pública e administração.

---

# Arquitetura do Pipeline

O pipeline segue uma arquitetura em camadas, inspirada no modelo medalhão:

    API Portal da Transparência
            ↓
    Consumo dos dados com Python
            ↓
    Escrita da camada Bronze com PySpark em Apache Iceberg
            ↓
    Armazenamento físico em Parquet e criação dos metadados Iceberg
            ↓
    Consulta da camada Bronze com DuckDB por meio de views
            ↓
    Transformações com dbt
            ↓
    Camada Prata materializada como tabela no DuckDB
            ↓
    Camada Ouro materializada como tabela no DuckDB
            ↓
    Feature Engineering
            ↓
    Modelagem Preditiva
            ↓
    Previsão de Gastos Públicos

A camada bronze é gravada com PySpark em Apache Iceberg, com armazenamento físico em Parquet. O DuckDB consulta essa camada por meio de views, e o dbt executa as transformações responsáveis pela construção das camadas prata e ouro, materializadas como tabelas no DuckDB.

---

# Tecnologias Utilizadas

## Engenharia de Dados

- Python;
- PySpark;
- Apache Iceberg;
- Parquet;
- DuckDB;
- dbt Core;
- dbt-duckdb;
- Docker;
- Docker Compose.

## Modelagem Preditiva

- Scikit-learn;
- Prophet;
- Statsmodels.

---

# Papel das Principais Tecnologias

## Python

Utilizado para consumo da API do Portal da Transparência e orquestração inicial do pipeline.

## PySpark

Utilizado para gravar os dados da camada bronze no formato Apache Iceberg.

## Apache Iceberg

Utilizado como formato de tabela para dados analíticos. Ao gravar os dados em Iceberg, os arquivos são armazenados fisicamente em Parquet e os metadados da tabela são criados e gerenciados pelo próprio Iceberg.

## Parquet

Formato físico colunar utilizado para armazenamento dos dados.

## DuckDB

Motor analítico local utilizado para consultar a camada bronze e armazenar as camadas prata e ouro materializadas pelo dbt.

## dbt

Utilizado para organizar e executar as transformações SQL das camadas prata e ouro.

## Docker e Docker Compose

Utilizados para padronizar a execução do projeto e facilitar a subida dos componentes necessários.

---

# Módulo de Ingestão

A pasta `ingestion` contém os componentes responsáveis pela coleta dos dados da API do Portal da Transparência e pela preparação dos registros para gravação da camada bronze.

Essa etapa realiza chamadas HTTP para os endpoints definidos, controla a paginação dos resultados, aplica os parâmetros de consulta e respeita o limite de requisições da API.

Os dados coletados são encaminhados para gravação da camada bronze em Apache Iceberg, com armazenamento físico em arquivos Parquet.

---

# Camadas Analíticas

## Camada Bronze

A camada bronze armazena os dados brutos provenientes da API.

Essa camada é gravada com PySpark em Apache Iceberg, utilizando arquivos Parquet como formato físico.

Tabelas:

    bronze.despesas_por_orgao
    bronze.despesas_funcional_programatica

## Metadados de Ingestão

Cada registro contém metadados gerados pelo pipeline:

| Coluna | Descrição |
|---|---|
| `__ingestion_time` | Timestamp da ingestão |
| `__source` | Origem dos dados |
| `__endpoint` | Endpoint utilizado |
| `__ingestion_id` | Identificador da execução |

---

## Camada Prata

A camada prata contém dados tratados, padronizados e enriquecidos.

Essa camada é construída com dbt e materializada como tabela no DuckDB.

Principais tratamentos previstos:

- conversão de tipos;
- padronização de valores;
- tratamento de campos monetários;
- tratamento de campos temporais;
- padronização de nomes, códigos de órgãos e funções.

Tabelas iniciais:

    prata.despesas_por_orgao
    prata.despesas_funcional_programatica

---

## Camada Ouro

A camada ouro é destinada ao consumo analítico e à modelagem preditiva.

Essa camada consolida os dados tratados em estruturas voltadas para análise, criação de métricas e construção de features.

Tabelas previstas:

    ouro.gastos_por_orgao
    ouro.gastos_por_funcao
    ouro.gastos_por_grupo

Essa camada será utilizada para:

- construção de métricas analíticas;
- análise temporal de gastos;
- análise de ciclos eleitorais;
- criação de features;
- geração de datasets para modelos preditivos.

---

# Estrutura do Projeto

    PROJETOFINALDSBD
    │
    ├── ingestion          # coleta e gravação da camada bronze
    ├── sql/duckdb         # scripts SQL para criação das views bronze
    ├── transform          # projeto dbt das camadas prata e ouro
    └── docker-compose.yml

---

# Pré-requisitos

Para execução do projeto, é necessário ter:

- Docker instalado e em execução;
- Docker Compose disponível;
- chave de acesso válida da API do Portal da Transparência;
- arquivo `.env` configurado localmente na raiz do projeto.

Exemplo de configuração do `.env`:

    API_KEY_NAME={your_api_key_name}
    API_KEY_VALUE={your_api_key_value}
    API_BASE_URL=https://api.portaldatransparencia.gov.br

    DATA_LAKE_BASE_PATH=/data

---

# Como Executar o Projeto

Clone o repositório:

    git clone https://github.com/millaspjiorin/ProjetoFinalDSBD.git
    cd ProjetoFinalDSBD

Execute o projeto com Docker Compose:

    docker compose up --build

Esse comando constrói a imagem do projeto e executa o pipeline conforme definido no `docker-compose.yml`.

---

# Principais Desafios Técnicos

Durante a construção do projeto, foram identificados alguns desafios técnicos:

- limite de requisições da API do Portal da Transparência, tratado com controle de taxa para evitar bloqueios durante a ingestão;
- necessidade de paginação para coleta completa dos dados;
- volume e granularidade dos dados;
- limitação histórica dos dados disponíveis, principalmente a partir de 2014;
- necessidade de recorte do escopo para o Poder Executivo Federal, considerando disponibilidade, consistência e relevância dos dados para análise de ciclos eleitorais;
- tentativa inicial de uso do ClickHouse para leitura de tabelas Iceberg locais, substituída pelo DuckDB devido a limitações na integração com `IcebergLocal`;
- integração dos componentes via Docker e Docker Compose.

---

# Estado Atual do Projeto

Atualmente, o projeto possui:

- consumo da API estruturado;
- controle de taxa de requisições implementado;
- escrita da camada bronze em Iceberg/Parquet com PySpark;
- estrutura Docker criada;
- Docker Compose configurado;
- leitura da camada bronze com DuckDB por meio de views;
- dbt configurado para construção das camadas prata e ouro;
- modelos iniciais da camada prata estruturados.

---

# Próximos Passos

- desenhar a arquitetura lógica completa da camada prata;
- definir tabelas intermediárias;
- mapear relacionamentos entre despesas por órgão e despesas por funcional-programática;
- definir métricas analíticas para acompanhamento dos gastos;
- criar indicadores de variação dos gastos ao longo do tempo;
- criar métricas por órgão, função, programa, grupo analítico e ano;
- estruturar a camada ouro com datasets prontos para análise e modelagem;
- realizar feature engineering;
- criar variáveis explicativas relacionadas a períodos eleitorais e grupos de gastos;
- desenvolver e comparar modelos preditivos;
- avaliar os resultados dos modelos;
- gerar previsões de gastos para 2026.


---

# Autora

Camilla Severo Spjiorin

Analista de Dados  
Especialização em Data Science e Big Data – UFPR