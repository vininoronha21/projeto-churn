import streamlit as st
import pandas as pd
import plotly.express as px

## CONSTANTES - Valores fixos para simplificação
CANCELADOS = 1
ATIVO = 0

## Colunas que o CSV deve ter (baseado no gerador_base.py)
COLUNAS_NECESSARIAS = [
    'id',
    'age',
    'gender',
    'customer_time',
    'frequency_use',
    'contacts_callcenter',
    'days_late',
    'signature',
    'contract_duration',
    'total_spent',
    'canceled'
]

## Configurações Iniciais
st.set_page_config(page_title="Dashboard de Churn", layout="wide")