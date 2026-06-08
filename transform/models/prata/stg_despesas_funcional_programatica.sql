{{ config(
    materialized='table'
  , schema='prata'
) }}

with source as (
    select *
    from {{ source('bronze', 'despesas_funcional_programatica') }}
)

, tratado as (
    select
        cast(ano as integer) as ano
      , trim(codigoFuncao) as codigo_funcao
      , trim(codigoSubfuncao) as codigo_subfuncao
      , trim(funcao) as nome_funcao
      , trim(subfuncao) as nome_subfuncao
      , trim(programa) as nome_programa
      , trim(acao) as nome_acao
      , trim(codigoPrograma) as codigo_programa
      , trim(codigoAcao) as codigo_acao
      , trim(pacote) as pacote
      , cast(replace(trim(replace(replace(empenhado, '.', ''), ',', '.')), '- ', '-') as double) as valor_empenhado
      , cast(replace(trim(replace(replace(liquidado, '.', ''), ',', '.')), '- ', '-') as double) as valor_liquidado
      , cast(replace(trim(replace(replace(pago,      '.', ''), ',', '.')), '- ', '-') as double) as valor_pago
      , case
            when cast(ano as integer) % 4 = 2 then true
            when cast(ano as integer) % 4 = 0 then true
            else false
        end  as fl_ano_eleitoral
      , case
            when cast(ano as integer) % 4 = 2 then 'geral'
            when cast(ano as integer) % 4 = 0 then 'municipal'
            else null
        end as tipo_eleicao
      , __ingestion_id
      , cast(__ingestion_time as timestamp) as ingestion_time
      , __source
      , __endpoint
    from source
    where codigoFuncao is not null
      and ano is not null
)

select * from tratado