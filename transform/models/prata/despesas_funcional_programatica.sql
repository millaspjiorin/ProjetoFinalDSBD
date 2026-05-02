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
    try_cast(replace(replace(empenhado, '.', ''), ',', '.') as double) as empenhado,
    try_cast(replace(replace(liquidado, '.', ''), ',', '.') as double) as liquidado,
    try_cast(replace(replace(pago, '.', ''), ',', '.') as double) as pago,
    pacote,
    __source,
    __endpoint,
    __ingestion_time,
    __ingestion_id
from {{ source('bronze', 'despesas_funcional_programatica') }}