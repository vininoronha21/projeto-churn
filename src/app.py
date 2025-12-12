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


## Funções Auxiliares
@st.cache_data
def carregar_dados():
  """
  Carrega os dados de cancelamento do CSV

  Returns:
    pd.DataFrame: DataFrame com dados de clientes, ou None se houver erro
  """
  try:
    dados = pd.read_csv("data/cancelamentos.csv")
    return dados
  except FileNotFoundError:
    return None

def validar_dados(df):
  """
  Verifica se o DataFrame possui todas as colunas necessárias

  Args:
    df: DataFrame a ser validado
  
  Returns:
    tuple: (bool, list) - (é válido?, lista de colunas faltantes)
  """
  if df is None:
    return False, []
  
  colunas_faltantes = [col for col in COLUNAS_NECESSARIAS if col not in df.columns]

  if colunas_faltantes:
    return False, colunas_faltantes
  
  return True, []

def calcular_metricas(df):
  """
  Calcula as métricas principais do dashboard
  
  Args:
    df: DataFrame com os dados de clientes

  Returns:
    dict: Dicionário com as métricas calculadas
  """
  total_clientes = len(df)

  # Previne divisão por zero
  if total_clientes == 0:
    return {
        'total': 0,
        'cancelados': 0,
        'taxa_churn': 0,
        'receita_perdida': 0
    }
  
  clientes_cancelados = df[df['canceled'] == CANCELADOS].shape[0]
  taxa_churn = (clientes_cancelados / total_clientes) * 100
  receita_perdida = df[df['canceled'] == CANCELADOS]['total_spent'].sum()

  return {
      'total': total_clientes,
      'cancelados': clientes_cancelados,
      'taxa_churn': taxa_churn,
      'receita_perdida': receita_perdida
  }

def formatar_moeda(valor):
  """
  Formata valor em reais (R$)

  Args:
    valor: Valor numérico a ser formatado

  Returns:
    str: Valor formatado como moeda BRL 
  """
  
  valor_formatado = f"{valor:,.2f}" # Utilizando f-string para formatar com 2 casas decimais e separadores
  valor_formatado = valor_formatado.replace(',', '_').replace('.', ',').replace('_', '.') # Utilizando replace para converter ao padrao brasileiro (1.000,00)
  return f"R${valor_formatado}"

def calcular_insight(df):
  """
  Calcula insights automáticos sobre os dados

  Args:
    df: DataFrame com os dados de clientes

  Returns:
    dict: Dicionário com os insights calculados
  """
  
  # Médias de atraso
  media_atraso_cancelados = df[df['canceled'] == CANCELADOS]['days_late'].mean()
  media_atraso_ativos = df[df['canceled'] == ATIVO]['days_late'].mean()

  # Análise por contrato
  churn_contrato = df.groupby("contract_duration")[["canceled"]].mean().reset_index()
  churn_contrato['canceled'] = churn_contrato['canceled'] * 100
  pior_contrato = churn_contrato.loc[churn_contrato['canceled'].idxmax(), 'contract_duration']

  return {
    'media_atraso_cancelados': media_atraso_cancelados,
    'media_atraso_ativos': media_atraso_ativos,
    'pior_contrato': pior_contrato,
    'churn_contrato': churn_contrato
  }

## Validação de dados
df = carregar_dados()

# Verifica se o arquivo existe
if df is None:
  st.error("❌ ERRO: O arquivo 'cancelamentos.csv' não foi encontrado.")
  st.info("💡 Dica: Rode o script 'gerador_base.py' para gerar o arquivo.")
  st.stop()

# Verifica se as colunas necessárias existem
valido, colunas_faltantes = validar_dados(df)

if not valido:
  st.error(f"❌ ERRO: Colunas faltantes no CSV: {', '.join(colunas_faltantes)}")
  st.info("💡 Verifique se o arquivo CSV está no formato correto.")
  st.stop()

# Verifica se há dados
if len(df) == 0:
  st.warning("⚠️ Aviso: O arquivo CSV está vazio!")
  st.stop()
  
## Interface do Dashboard
st.title("📊 Análise de Cancelamento de Clientes")
st.markdown("Este dashboard foi desenvolvido para analisar motivos prováveis de cancelamentos e possíveis perda de clientes.")

## I. KPIs Principais
st.subheader("📈 Métricas Principais")

metricas = calcular_metricas(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Base Total", metricas['total'])
col2.metric("❌ Cancelamentos", metricas['cancelados'])
col3.metric("📊 Taxa de Churn", f"{metricas['taxa_churn']:.1f}%")
col4.metric("💰 Receita Perdida", formatar_moeda(metricas['receita_perdida']))

st.divider()

## II. Dados Brutos
st.subheader("🔍 Quem fica vs Quem sai")

if st.checkbox("Mostrar dados brutos"):
  st.dataframe(df.head(10)) # Mostra 10 primeiras linhas

## III. Gráficos de Análise
st.subheader("📊 Análises Visuais")

graph1, graph2 = st.columns(2)

# Gráfico 1: Atraso no Pagamento vs Cancelamento
with graph1:
    fig_dias = px.box(
      df,
      x='canceled',
      y='days_late',
      color='canceled',
      title="Dias de Atraso no Pagamento",
      labels={
        'canceled': "Cancelou? (0=Não, 1=Sim)",
        'days_late': "Dias de atraso"  
      },
      color_discrete_map={ATIVO: "#2ca02c", CANCELADOS: "#d62728"}
    )
    fig_dias.update_layout(showlegend=False)
    st.plotly_chart(fig_dias, use_container_width=True)

with graph2:
    fig_call = px.histogram(
      df, 
      x="contacts_callcenter", 
      color="canceled",
      title="Número de Ligações ao Suporte",
      barmode="group",
      labels={"contacts_callcenter": "Nº de Ligações"},
      color_discrete_map={ATIVO: "#2ca02c", CANCELADOS: "#d62728"}
      )
    st.plotly_chart(fig_call, use_container_width=True)
  
st.divider()  

## IV. Calcular insights para Análise de Contrato
st.subheader("Análise por Tipo de Contrato")

insights = calcular_insight(df)

fig_contrato = px.bar(
  insights['churn_contrato'],
  x='contract_duration',
  y='canceled',
  title="Taxa de Cancelamento por Duração de Contrato",
  labels={
    'canceled': "Taxa de Cancelamento (%)",
    'contract_duration': "Tipo de Contrato"
  },
  color='canceled',
  color_continuous_scale="Reds"
)
st.plotly_chart(fig_contrato, use_container_width=True)

## V. Insights Automáticos
st.divider()
st.subheader("Insights Automáticos")

col1, col2 = st.columns(2)

with col1:
  st.info("Sobre atrasos de pagamento")
  st.write(f"Média de atraso de quem cancela: {insights['media_atraso_cancelados']:.1f} dias")
  st.write(f"Média de atraso de quem fica: {insights['media_atraso_ativos']:.1f} dias")

  # Alerta se a diferença for significativa
  if insights['media_atraso_cancelados'] > insights['media_atraso_ativos'] * 2:
    st.error("CRÍTICO: Clientes que cancelam atrasam o dobro do tempo!")

with col2:
  st.info("Sobre contratos")
  st.write(f"O tipo de contrato com maior rejeição é: {insights['pior_contrato']}")
  st.warning(f"🚨 SUGESTÃO: Criar incentivos para migrar clientes do {insights['pior_contrato']} para outros planos")

## VI. Rodapé
st.divider()
st.caption("Dashboard feito por Vinícius Forte com Streamlit 🚀")