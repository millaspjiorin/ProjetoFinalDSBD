{{ config(
    materialized='table'
  , schema='ouro'
) }}

with base as (
    select
        ano
      , codigo_orgao
      , nome_orgao
      , codigo_orgao_superior
      , nome_orgao_superior
      , pacote
      , fl_ano_eleitoral
      , tipo_eleicao
      , sum(valor_empenhado) as valor_empenhado
      , sum(valor_liquidado) as valor_liquidado
      , sum(valor_pago)      as valor_pago
    from {{ ref('stg_despesas_por_orgao') }}
    group by 1, 2, 3, 4, 5, 6, 7, 8
)

, com_features as (
    select
        ano
      , codigo_orgao
      , nome_orgao
      , codigo_orgao_superior
      , nome_orgao_superior
      , pacote
      , fl_ano_eleitoral
      , tipo_eleicao
      , lag(fl_ano_eleitoral, 1) over (
            partition by codigo_orgao order by ano
        ) as fl_ano_pre_eleitoral
      , lead(fl_ano_eleitoral, 1) over (
            partition by codigo_orgao order by ano
        ) as fl_ano_pos_eleitoral
      , case
            when ano between 2003 and 2006 then 'Lula 1'
            when ano between 2007 and 2010 then 'Lula 2'
            when ano between 2011 and 2014 then 'Dilma 1'
            when ano between 2015 and 2015 then 'Dilma 2'
            when ano = 2016                then 'Transicao'
            when ano between 2017 and 2018 then 'Temer'
            when ano between 2019 and 2022 then 'Bolsonaro'
            when ano >= 2023               then 'Lula 3'
        end as governo
      , valor_empenhado
      , valor_liquidado
      , valor_pago
      , lag(valor_pago, 1) over (
            partition by codigo_orgao order by ano
        ) as valor_pago_lag_1
      , lag(valor_pago, 2) over (
            partition by codigo_orgao order by ano
        ) as valor_pago_lag_2
      , valor_pago - lag(valor_pago, 1) over (
            partition by codigo_orgao order by ano
        ) as variacao_yoy_abs
      , case
            when lag(valor_pago, 1) over (
                partition by codigo_orgao order by ano
            ) > 0
            then round(
                (valor_pago - lag(valor_pago, 1) over (
                    partition by codigo_orgao order by ano
                )) / lag(valor_pago, 1) over (
                    partition by codigo_orgao order by ano
                ) * 100
            , 2)
            else null
        end as variacao_yoy_pct
      , avg(valor_pago) over (
            partition by codigo_orgao
            order by ano
            rows between 2 preceding and current row
        ) as rolling_mean_3
    from base
)

select * from com_features