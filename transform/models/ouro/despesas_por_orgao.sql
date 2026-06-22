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
      , sum(valor_empenhado) as valor_empenhado
      , sum(valor_liquidado) as valor_liquidado
      , sum(valor_pago) as valor_pago
    from {{ ref('stg_despesas_por_orgao') }}
    group by
        ano
      , codigo_orgao
      , nome_orgao
      , codigo_orgao_superior
      , nome_orgao_superior
      , pacote

)

, com_lags as (
    select
        *
        , lag(valor_pago, 1) over (
            partition by codigo_orgao, pacote
            order by ano
        ) as valor_pago_lag_1
        , lag(valor_pago, 2) over (
            partition by codigo_orgao, pacote
            order by ano
        ) as valor_pago_lag_2
        , avg(valor_pago) over (
            partition by codigo_orgao, pacote
            order by ano
            rows between 2 preceding and current row
        ) as rolling_mean_3
    from base
)

, com_features as (
    select
        md5(
            concat_ws(
                '|',
                cast(ano as varchar),
                codigo_orgao,
                pacote
            )
        ) as sk_despesa_orgao
        , ano
        , codigo_orgao
        , nome_orgao
        , codigo_orgao_superior
        , nome_orgao_superior
        , pacote
        , ano % 4 = 3 as fl_ano_pre_eleitoral
        , ano % 4 = 1 as fl_ano_pos_eleitoral
        , ano % 4 in (0, 2) as fl_ano_eleitoral
        , case
            when ano % 4 = 2 then 'Geral'
            when ano % 4 = 0 then 'Municipal'
            else 'Não Eleitoral'
        end as tipo_eleicao
        , case
            when ano between 2003 and 2006 then 'Lula 1'
            when ano between 2007 and 2010 then 'Lula 2'
            when ano between 2011 and 2014 then 'Dilma 1'
            when ano = 2015                then 'Dilma 2'
            when ano = 2016                then 'Transicao'
            when ano between 2017 and 2018 then 'Temer'
            when ano between 2019 and 2022 then 'Bolsonaro'
            when ano >= 2023               then 'Lula 3'
        end as governo
        , valor_empenhado
        , valor_liquidado
        , valor_pago
        , valor_pago_lag_1
        , valor_pago_lag_2
        , valor_pago - valor_pago_lag_1 as variacao_yoy_abs
        , case
            when valor_pago_lag_1 > 0
            then round(
                ((valor_pago - valor_pago_lag_1) / valor_pago_lag_1) * 100
            , 2)
        end as variacao_yoy_pct
        , rolling_mean_3
    from com_lags
)

select *
from com_features