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

Para apoiar a análise, os dados são organizados em grupos analíticos definidos na etapa de ingestão, com base nos códigos de órgão e de função orçamentária.

## Análise por órgãos

Os órgãos do Poder Executivo foram agrupados conforme o tipo de impacto potencial de seus gastos:

- núcleo eleitoral: saúde, educação, assistência social e previdência;
- infraestrutura: transportes, cidades, integração regional e energia;
- coordenação política: fazenda, planejamento, presidência e justiça.

## Análise por funções orçamentárias

As funções orçamentárias foram agrupadas com base na literatura sobre ciclos políticos de gastos:

- políticas sociais: saúde, educação e assistência social;
- infraestrutura: transporte, urbanismo e agricultura;
- segurança do estado: defesa e segurança pública;
- administração do governo: administração e trabalho.

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

Durante a ingestão, cada registro recebe uma coluna `pacote` com a classificação analítica correspondente, atribuída com base no código de órgão ou de função orçamentária conforme dicionários definidos no módulo de configuração.

---

# Camadas Analíticas

## Camada Bronze

A camada bronze armazena os dados brutos provenientes da API, sem nenhuma transformação. Os campos monetários são mantidos como VARCHAR com formatação brasileira, e os metadados de ingestão são adicionados pelo pipeline.

Tabelas:

    bronze.despesas_por_orgao
    bronze.despesas_funcional_programatica

---

## Camada Prata

A camada prata contém dados tratados, padronizados e enriquecidos. As duas tabelas são tratadas de forma independente, sem junção entre si, pois os endpoints retornam dados com granularidades distintas e sem chave comum.

Tratamentos aplicados:

- conversão de tipos: `ano` para integer, campos monetários de VARCHAR para double com tratamento de formatação brasileira e valores negativos, `__ingestion_time` para timestamp;
- padronização de campos textuais com `trim` em códigos e nomes;
- cálculo de flags eleitorais com base no calendário brasileiro: anos com resto 2 na divisão por 4 correspondem a eleições gerais, anos divisíveis por 4 correspondem a eleições municipais;
- preservação dos metadados de ingestão.

Tabelas:

    prata.stg_despesas_por_orgao
    prata.stg_despesas_funcional_programatica

---

## Camada Ouro

A camada ouro é destinada ao consumo analítico e à modelagem preditiva. As duas tabelas permanecem independentes, refletindo as duas perspectivas de análise dos gastos públicos.

Transformações aplicadas em ambas as tabelas:

- agregação dos valores por ano, entidade e pacote;
- cálculo do contexto eleitoral ampliado: flag de ano pré-eleitoral via `lag` de `fl_ano_eleitoral` e flag de ano pós-eleitoral via `lead`;
- identificação do governo em exercício no ano, com tratamento explícito do ano de 2016 como período de transição em razão do impeachment;
- cálculo de features de série temporal: `valor_pago_lag_1`, `valor_pago_lag_2`, `variacao_yoy_abs`, `variacao_yoy_pct` e `rolling_mean_3`.

Tabelas:

    ouro.despesas_por_orgao
    ouro.despesas_por_funcao

### Decisões de modelagem

As duas tabelas ouro não são unidas por JOIN. A ausência de chave comum entre as perspectivas de órgão e de função orçamentária reflete a estrutura real dos dados retornados pela API, que agrega cada dimensão de forma independente. A comparação entre as duas perspectivas é realizada por meio do campo `pacote`, utilizado como dimensão analítica comum nas análises exploratórias e nos modelos preditivos.

O campo `governo` recebe o valor `Transicao` para o ano de 2016, em razão do impeachment ocorrido em maio daquele ano, que impossibilita a atribuição do exercício completo a um único governo.

---

# Estrutura do Projeto

    PROJETOFINALDSBD
    │
    ├── ingestion                        # coleta e gravação da camada bronze
    ├── sql/duckdb                       # scripts SQL para criação das views bronze
    ├── transform                        # projeto dbt das camadas prata e ouro
    │   ├── dbt_project.yml
    │   ├── profiles.yml
    │   └── models
    │       ├── sources.yml              # declaração das fontes bronze
    │       ├── prata
    │       │   ├── stg_despesas_por_orgao.sql
    │       │   ├── stg_despesas_por_orgao.yml
    │       │   ├── stg_despesas_funcional_programatica.sql
    │       │   └── stg_despesas_funcional_programatica.yml
    │       └── ouro
    │           ├── despesas_por_orgao.sql
    │           ├── despesas_por_orgao.yml
    │           ├── despesas_por_funcao.sql
    │           └── despesas_por_funcao.yml
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
- ausência de chave comum entre as duas dimensões de análise, resolvida com a criação do campo `pacote` na ingestão e com a adoção de tabelas independentes nas camadas prata e ouro;
- inconsistências nos valores monetários retornados pela API, como separadores de milhar e valores negativos com espaço entre o sinal e os dígitos, tratadas na camada prata;
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
- camada prata construída com tratamento de tipos, padronização de campos, conversão de valores monetários e enriquecimento com flags eleitorais;
- camada ouro construída com agregações por ano e entidade, features de série temporal e contexto político-eleitoral;
- testes de qualidade implementados com dbt para ambas as camadas.

---

# Próximos Passos

- realizar análise exploratória dos dados das camadas prata e ouro;
- validar a consistência das flags eleitorais e do campo governo ao longo da série histórica;
- desenvolver e comparar modelos preditivos com Statsmodels, Prophet e Scikit-learn;
- avaliar os resultados dos modelos;
- gerar previsões de gastos públicos para 2026.

---

# Autora

Camilla Severo Spjiorin

Analista de Dados
Especialização em Data Science e Big Data – UFPR