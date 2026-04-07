# 📊 Pipeline de Dados e Previsão de Gastos Públicos (Brasil – 2026)

Projeto de **engenharia de dados e ciência de dados ponta a ponta**, com foco na construção de um pipeline escalável para análise e previsão dos **gastos públicos federais brasileiros**, com ênfase no comportamento em **anos eleitorais (2026)**.

O projeto utiliza ferramentas **open source** para ingestão, processamento, armazenamento e modelagem de dados provenientes do **Portal da Transparência**.

---

# 🎯 Problema de Negócio

Os gastos públicos federais podem apresentar **variações sistemáticas em períodos eleitorais**. Em muitos países, estudos econômicos investigam esse fenômeno conhecido como **Political Budget Cycle (Ciclo Político Orçamentário)**.

No Brasil, prever esse comportamento apresenta desafios:

- dados **volumosos e descentralizados**
- ausência de pipelines padronizados
- múltiplas dimensões do orçamento público
- necessidade de dados estruturados para Machine Learning

---

# 🧠 Solução

Construção de um pipeline que:

- consome dados da API do Portal da Transparência
- armazena no ClickHouse
- organiza em **Bronze / Prata / Ouro**
- prepara dados para Machine Learning
- permite **previsão de gastos públicos**

---

# 🏛️ Escopo

Duas dimensões complementares:

- despesas por órgão  
- despesas por funcional-programática  

---

# 📡 APIs Utilizadas

## Despesas por Órgão

```
/api-de-dados/despesas/por-orgao
```

~ 2.585 registros

---

## Despesas por Funcional-Programática

```
/api-de-dados/despesas/por-funcional-programatica
```

~ 25.599 registros

---

# 📊 Estratégia de Análise

Para capturar diferentes comportamentos de gasto público, os dados foram organizados em **grupos analíticos**, baseados no tipo de impacto econômico e político.

## 📦 Análise por Órgãos

Os órgãos foram agrupados conforme o impacto potencial de seus gastos:

- **Núcleo eleitoral** → saúde, educação, assistência social, previdência  
- **Infraestrutura** → transportes, cidades, integração regional, energia  
- **Coordenação política** → fazenda, planejamento, presidência, justiça  

---

## 📦 Análise por Funções Orçamentárias

As funções foram agrupadas com base na literatura de ciclos políticos de gastos:

- **Gastos visíveis ao eleitor** → saúde, educação, assistência  
- **Investimentos públicos** → transporte, urbanismo, agricultura  
- **Gastos estruturais** → defesa, segurança, administração  

---

# 🏗️ Arquitetura do Pipeline

```
API Portal da Transparência
        ↓
Ingestão (Python)
        ↓
ClickHouse (bronze)
        ↓
ClickHouse (prata)
        ↓
ClickHouse (ouro)
        ↓
Feature Engineering
        ↓
Machine Learning
        ↓
Previsão de gastos
```

---

# ⚙️ Módulo de Ingestão

A pasta `ingestion` contém os componentes responsáveis pela coleta e ingestão dos dados da API.

Principais módulos:

- `client.py` → requisições HTTP  
- `fetcher.py` → paginação e coleta de dados  
- `params.py` → parâmetros das requisições  
- `writer.py` → persistência no ClickHouse  
- `main.py` → orquestra o pipeline  

Configurações são definidas em `config.py`.

## ⏱️ Controle de Taxa (Rate Limiting)

Foi implementado controle de taxa de requisições no pipeline, com intervalo de **0,4 segundos entre chamadas**.

Essa abordagem garante:

- conformidade com os limites da API do Portal da Transparência  
- estabilidade do pipeline de ingestão  
- prevenção de bloqueios por excesso de requisições  

---

# 📂 Estrutura do Projeto

```
PROJETOFINALDSBD
│
├── ingestion
│   ├── client.py
│   ├── config.py
│   ├── fetcher.py
│   ├── main.py
│   ├── params.py
│   ├── writer.py
│   │
│   └── schemas
│       ├── despesas_funcional_programatica.py
│       └── despesas_por_orgao.py
│
├── README.md
└── requirements.txt
```

---

# 🥉 Camada Bronze

Schema:

```
bronze
```

Tabelas:

```
bronze.despesas_por_orgao
bronze.despesas_funcional_programatica
```

Dados brutos da API.

---

## 🧩 Metadados de Ingestão

Cada registro contém metadados gerados pelo pipeline:

| coluna | descrição |
|------|------|
__ingestion_time | timestamp da ingestão |
__source | fonte do dado (Portal da Transparência) |
__endpoint | endpoint utilizado |
__ingestion_id | identificador da execução do pipeline |

---

## 🎯 Objetivo da Bronze

- preservar dados originais  
- garantir rastreabilidade  
- permitir reprocessamento  

---

# 🥈 Camada Prata

Schema:

```
prata
```

Transformações:

- limpeza de dados  
- padronização  
- conversão de valores  
- enriquecimento analítico  

Tabelas:

```
prata.despesas_por_orgao
prata.despesas_funcional_programatica
```

---

# 🥇 Camada Ouro

Schema:

```
ouro
```

Tabelas:

```
ouro.gastos_por_orgao
ouro.gastos_por_funcao
ouro.gastos_por_grupo
```

Uso:

- feature engineering  
- datasets para Machine Learning  
- previsão de gastos  

---

# ⚙️ Tecnologias Utilizadas

### Engenharia de Dados

- Python  
- ClickHouse  
- dbt Core  
- Airflow / Prefect  

### Ciência de Dados

- Scikit-learn  
- Prophet  
- Statsmodels  

---

# ▶️ Como Executar

```bash
git clone https://github.com/millaspjiorin/ProjetoFinalDSBD.git
cd ProjetoFinalDSBD
pip install -r requirements.txt
clickhouse server
python ingestion/main.py
```

---

# 📈 Próximos Passos

- implementação completa da camada Prata  
- implementação da camada Ouro  
- feature engineering  
- treinamento de modelos de ML  
- avaliação de previsões  
- análise de ciclos eleitorais  
- governança de dados (DataHub / Amundsen)  

---

# 👩‍💻 Autora

**Camilla Spjiorin**

Analista de Dados  
Especialização em **Data Science e Big Data – UFPR**