{{ config(
    materialized='table'
  , schema='prata'
) }}

with source as (
    select *
    from {{ source('bronze', 'despesas_por_orgao') }}
)

, tratado as (
    select
        cast(ano as integer) as ano
      , trim(codigoOrgao) as codigo_orgao
      , trim(codigoOrgaoSuperior) as codigo_orgao_superior
      , trim(orgao) as nome_orgao
      , trim(orgaoSuperior) as nome_orgao_superior
      , trim(pacote) as pacote
      , cast(trim(replace(replace(empenhado, '.', ''), ',', '.')) as double) as valor_empenhado
      , cast(trim(replace(replace(liquidado, '.', ''), ',', '.')) as double) as valor_liquidado
      , cast(trim(replace(replace(pago,      '.', ''), ',', '.')) as double) as valor_pago
      , __ingestion_id
      , cast(__ingestion_time as timestamp) as ingestion_time
      , __source
      , __endpoint
    from source
    where codigoOrgao is not null
      and ano is not null
)

select * from tratado