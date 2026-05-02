# ================================
# Intervalo temporal analisado
# ================================

START_YEAR = 2014
END_YEAR = 2026

ANOS = list(range(START_YEAR, END_YEAR + 1))


# ================================
# Parâmetros - API despesas por órgão
# Endpoint:
# /api-de-dados/despesas/por-orgao
# ================================

PACOTES_ORGAOS = {
    "nucleo_eleitoral": [
        "36000",  # Ministério da Saúde
        "26000",  # Ministério da Educação
        "55000",  # Ministério do Desenvolvimento e Assistência Social
        "33000",  # Ministério da Previdência Social
    ],
    "infraestrutura": [
        "39000",  # Ministério dos Transportes
        "56000",  # Ministério das Cidades
        "53000",  # Ministério da Integração e Desenvolvimento Regional
        "32000",  # Ministério de Minas e Energia
    ],
    "coordenacao_politica": [
        "25000",  # Ministério da Fazenda
        "47000",  # Ministério do Planejamento e Orçamento
        "20000",  # Presidência da República
        "30000",  # Ministério da Justiça e Segurança Pública
    ],
}

# ================================
# Parâmetros - API funcional programática
# Endpoint:
# /api-de-dados/despesas/por-funcional-programatica
# ================================

# Funções orçamentárias relevantes para análise de gasto público

PACOTES_FUNCOES = {

    "politicas_sociais": [
        "08",  # Assistência Social
        "10",  # Saúde
        "12",  # Educação
    ],

    "infraestrutura": [
        "15",  # Urbanismo
        "26",  # Transporte
        "20",  # Agricultura
    ],

    "seguranca_estado": [
        "06",  # Segurança Pública
        "05",  # Defesa Nacional
    ],

    "administracao_governo": [
        "04",  # Administração
        "11",  # Trabalho
    ],
}

# ================================
# Intervalo latencia
# ================================
REQUESTS_PER_MINUTE = 180
SAFETY_FACTOR = 1.2