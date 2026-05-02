{{ config(
    materialized='table'
) }}

select
    ano,
    funcao,
    codigoFuncao,
    subfuncao,
    codigoSubfuncao,
    programa,
    codigoPrograma,
    acao,
    codigoAcao,
    toFloat64(replaceAll(replaceAll(empenhado, '.', ''), ',', '.')) as empenhado,
    toFloat64(replaceAll(replaceAll(liquidado, '.', ''), ',', '.')) as liquidado,
    toFloat64(replaceAll(replaceAll(pago, '.', ''), ',', '.')) as pago,
    pacote,
    __source,
    __endpoint,
    __ingestion_time,
    __ingestion_id
from {{ source('bronze', 'despesas_funcional_programatica') }}