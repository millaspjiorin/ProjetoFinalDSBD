# 📊 Pipeline de Dados e Previsão de Gastos Públicos (Brasil – 2026)

Projeto de **engenharia de dados e ciência de dados ponta a ponta**, com foco na construção de um pipeline escalável para análise e previsão dos **gastos públicos federais brasileiros**, com ênfase no comportamento em **anos eleitorais (2026)**.

O projeto utiliza ferramentas **open source** para ingestão, processamento, armazenamento e modelagem de dados provenientes do **Portal da Transparência**.

---

# 🎯 Problema de Negócio

Os gastos públicos tendem a variar em anos eleitorais, porém:

- Os dados são **volumosos e descentralizados**
- Não existe um **pipeline padronizado de ingestão e tratamento**
- A previsão de gastos governamentais é **complexa**

Este projeto busca responder à seguinte pergunta:

> Como construir um pipeline de dados escalável e de baixo custo capaz de processar dados públicos e gerar previsões confiáveis de gastos em ano eleitoral?

---

# 🧠 Solução

Construção de um **pipeline automatizado de dados** que:

- Consome dados da API do Portal da Transparência
- Realiza ingestão estruturada via Python
- Organiza os dados em camadas analíticas (Bronze, Silver e Gold)
- Permite futuras análises e modelagem preditiva

---

# 🔌 Fonte de Dados

Os dados são obtidos através da **API do Portal da Transparência**.

Exemplo de requisição utilizada:

```bash
curl -X GET \
'https://api.portaldatransparencia.gov.br/api-de-dados/despesas/por-orgao?ano=2025&orgaoSuperior=36000&pagina=1' \
-H 'accept: */*' \
-H 'chave-api-dados: SUA_CHAVE_API'
```

Essa API retorna informações de **despesas públicas federais por órgão**.

---

# 🏗️ Arquitetura do Pipeline

O pipeline segue o conceito de **Medallion Architecture**:

### 🥉 Bronze
Dados brutos extraídos da API, armazenados sem transformação.

### 🥈 Silver
Dados tratados:
- padronização de tipos
- limpeza
- organização das tabelas.

### 🥇 Gold
Dados preparados para análise e modelagem preditiva.

Fluxo planejado:

```
API Portal da Transparência
        ↓
Pipeline de Ingestão (Python)
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
Modelagem preditiva
```

---

# 📦 Estrutura Atual do Projeto

Atualmente o projeto está na fase de **desenvolvimento do módulo de ingestão de dados**.

```
PROJETOFINALDSBD
│
├── ingestion
│   ├── client.py
│   ├── config.py
│   ├── fetcher.py
│   ├── main.py
│   └── params.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# ⚙️ Módulo de Ingestão

A pasta `ingestion` contém os componentes responsáveis por consumir a API do Portal da Transparência.

### `client.py`

Responsável por realizar as requisições HTTP para a API.

### `config.py`

Contém configurações do projeto, como:

- URL base da API
- headers
- chave da API

### `fetcher.py`

Responsável por:

- buscar os dados da API
- tratar paginação
- retornar os dados para processamento.

### `params.py`

Define parâmetros utilizados nas requisições, como:

- ano
- órgão
- página.

### `main.py`

Ponto de entrada do pipeline de ingestão.

Executa:

- configuração
- requisições
- coleta de dados.

---

# 📊 Estratégia de Análise

Para análise do comportamento de gastos, os órgãos foram agrupados em **pacotes estratégicos**.

## 📦 Pacote 1 — Núcleo Eleitoral

| Órgão | Código SIAFI |
|------|------|
| Ministério da Saúde | 36000 |
| Ministério da Educação | 26000 |
| Ministério do Desenvolvimento e Assistência Social | 55000 |
| Ministério da Previdência Social | 33000 |

Impacto direto no eleitorado.

---

## 📦 Pacote 2 — Infraestrutura e Capilaridade Regional

| Órgão | Código SIAFI |
|------|------|
| Ministério dos Transportes | 39000 |
| Ministério das Cidades | 56000 |
| Ministério da Integração e Desenvolvimento Regional | 53000 |
| Ministério de Minas e Energia | 32000 |

Normalmente apresentam **aceleração de gastos em períodos pré-eleitorais**.

---

## 📦 Pacote 3 — Coordenação Fiscal e Política

| Órgão | Código SIAFI |
|------|------|
| Ministério da Fazenda | 25000 |
| Ministério do Planejamento e Orçamento | 47000 |
| Presidência da República | 20000 |
| Ministério da Justiça e Segurança Pública | 30000 |

---

## 📦 Pacote 4 — Processo Eleitoral

| Órgão | Código SIAFI |
|------|------|
| Câmara dos Deputados | 01000 |
| Senado Federal | 02000 |
| Tribunal Superior Eleitoral | (consultar código SIAFI)

---

# ⚙️ Tecnologias Utilizadas

### Engenharia de Dados

- Python
- Parquet
- ClickHouse
- dbt Core
- Airflow / Prefect

### Ciência de Dados

- Scikit-learn
- Prophet
- Statsmodels

### Governança de Dados

- DataHub
- Amundsen

---

# ▶️ Como Executar

Clone o repositório:

```bash
git clone https://github.com/millaspjiorin/ProjetoFinalDSBD.git
```

Acesse o diretório:

```bash
cd ProjetoFinalDSBD
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o pipeline de ingestão:

```bash
python ingestion/main.py
```

---

# 📈 Próximos Passos

Evolução planejada do projeto:

- Implementação das camadas **Bronze, Silver e Gold**
- Armazenamento em **ClickHouse**
- Transformações com **dbt**
- Orquestração com **Airflow ou Prefect**
- Desenvolvimento do **modelo preditivo de gastos para 2026**

---

# 👩‍💻 Autora

**Camilla Spjiorin**

Analista de Dados  
Especialização em **Data Science e Big Data – UFPR**