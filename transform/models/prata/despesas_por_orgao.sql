{{ config(
    materialized='table'
) }}

select
    ano,
    orgao,
    codigoOrgao,
    orgaoSuperior,
    codigoOrgaoSuperior,
    try_cast(replace(replace(empenhado, '.', ''), ',', '.') as double) as empenhado,
    try_cast(replace(replace(liquidado, '.', ''), ',', '.') as double) as liquidado,
    try_cast(replace(replace(pago, '.', ''), ',', '.') as double) as pago,
    pacote,
    __source,
    __endpoint,
    __ingestion_time,
    __ingestion_id
from {{ source('bronze', 'despesas_por_orgao') }}