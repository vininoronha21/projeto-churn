import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

## CONSTANTES - Valores fixos para simplificação
CANCELADOS = 1
ATIVO = 0

## Colunas que o CSV deve ter (baseado no gerador_base.py)
COLUNAS_NECESSARIAS = [
    'id_cliente',
    'data_cadastro',
    'idade',
    'genero',
    'tempo_cliente',
    'frequencia_uso',
    'contatos_callcenter',
    'dias_atraso',
    'assinatura',
    'duracao_contrato',
    'total_gasto',
    'cancelado'
]

## Configurações Iniciais
st.set_page_config(
    page_title="Dashboard de Churn | Vinícius Forte",  # Título da aba
    page_icon="💡",  # Emoji que aparece na aba
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/vininoronha21/projeto-churn',
        'Report a bug': 'https://github.com/vininoronha21/projeto-churn/issues',
        'About': '''
        
        Este projeto foi desenvolvido como parte dos meus estudos em:
        - Análise e Desenvolvimento Web com Python
        - Manipulação de dados com Pandas
        - Visualização com Plotly
        - Criação de dashboards interativos
        
        📧 Email: contatovininoronha@gmail.com\n
        💼 [LinkedIn](https://linkedin.com/in/viniciusnoronha)\n  
        🐙 [GitHub](https://github.com/vininoronha21)\n
    
        Desenvolvido por **Vinícius Forte**
        '''
    }
)


## Detectar se é mobile
is_mobile = st.session_state.get('mobile', False)

if st.sidebar.checkbox("Modo Mobile"):
    is_mobile = True
    st.session_state.mobile = True

## Adaptar layout para mobile
if is_mobile:
    st.columns(1)
else:
    st.columns(4)


## Funções Auxiliares
@st.cache_data
def carregar_dados():
    """
    Carrega os dados de cancelamento do CSV

    Returns:
      pd.DataFrame: DataFrame com dados de clientes, ou None se houver erro
    """
    BASE_DIR = Path(__file__).resolve().parents[1]
    caminho_csv = BASE_DIR / "data" / "cancelamentos.csv"

    if not caminho_csv.exists():
        return None

    return pd.read_csv(caminho_csv)


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
    
    clientes_cancelados = df[df['cancelado'] == CANCELADOS].shape[0]
    taxa_churn = (clientes_cancelados / total_clientes) * 100
    receita_perdida = df[df['cancelado'] == CANCELADOS]['total_gasto'].sum()

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
    media_atraso_cancelados = df[df['cancelado'] == CANCELADOS]['dias_atraso'].mean()
    media_atraso_ativos = df[df['cancelado'] == ATIVO]['dias_atraso'].mean()

    # Análise por contrato
    churn_contrato = df.groupby("duracao_contrato")[["cancelado"]].mean().reset_index()
    churn_contrato['cancelado'] = churn_contrato['cancelado'] * 100
    pior_contrato = churn_contrato.loc[churn_contrato['cancelado'].idxmax(), 'duracao_contrato']

    return {
        'media_atraso_cancelados': media_atraso_cancelados,
        'media_atraso_ativos': media_atraso_ativos,
        'pior_contrato': pior_contrato,
        'churn_contrato': churn_contrato
    }


def converter_coluna_data(df):
    """
    Converte a coluna 'data_cadastro' para o tipo de datetime do pandas

    Por que é importante?
    - Pandas precisa saber que é uma data para ser filtrada
    - Sem conversão, a coluna é tratada como texto

    Args:
      df: DataFrame com coluna 'data_cadastro' como string

    Returns:
      pd.DataFrame: DataFrame com coluna convertida para datetime
    """
    df = df.copy()
    if 'data_cadastro' in df.columns:
        df['data_cadastro'] = pd.to_datetime(df['data_cadastro'], errors='coerce') # erros='coerce' transforma datas inválidas em NaT (Not a Time)   
    return df


## Validação de dados
df = carregar_dados()

# Verifica se o arquivo existe
if df is None:
    st.error("❌ ERRO: Arquivo data/cancelamentos.csv não encontrado.")
    st.info("💡 Verifique se o arquivo está versionado no GitHub.")
    st.stop()

# Converter coluna de data
df = converter_coluna_data(df)

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

## X. Filtros
st.subheader("🔍 Filtros de Análise")

# Criar colunas para organizar os filtros lado a lado
col_filtro1, col_filtro2, col_filtro3 = st.columns(3)

with col_filtro1:
    data_minima = df['data_cadastro'].min().date()
    data_maxima = df['data_cadastro'].max().date()

    data_inicial = st.date_input(
        "📅 Data Inicial",
        value=data_minima,
        min_value=data_minima,
        max_value=data_maxima,
        help="Selecione a data inicial para filtrar os dados"
    )

with col_filtro2:
    data_final = st.date_input(
        "📅 Data Final",
        value=data_maxima,
        min_value=data_minima,
        max_value=data_maxima,
        help="Selecione a data final para filtrar os dados"
    )

with col_filtro3:
    # Filtro adicional: tipo de contratro
    # Obtém todos os tipos únicos de contrato
    tipos_contrato = ['Todos'] + sorted(df['duracao_contrato'].unique().tolist())

    filtro_contrato = st.selectbox(
        "📋 Tipo de Contrato",
        options=tipos_contrato,
        help="Filtre por tipo de contrato específico"
    )

if data_inicial > data_final:
    st.error("⚠️ Erro: A data inicial não pode ser posterior à data final!")
    st.stop()

## I. Aplicar filtros no DataFrame

# Converter data_inicial e data_final para datetime
data_inicial_dt = pd.to_datetime(data_inicial)
data_final_dt = pd.to_datetime(data_final)

# Filtro por data
df_filtrado = df[
    (df['data_cadastro'] >= data_inicial_dt) & 
    (df['data_cadastro'] <= data_final_dt)
].copy()  # .copy() cria uma cópia para evitar warnings do pandas

# Filtro por tipo de contrato
if filtro_contrato != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['duracao_contrato'] == filtro_contrato]

# Mostrar informações sobre os filtros aplicados
total_original = len(df)
total_filtrado = len(df_filtrado)
percentual = (total_filtrado / total_original * 100) if total_original > 0 else 0

st.info(f"📊 Mostrando **{total_filtrado:,}** de **{total_original:,}** clientes ({percentual:.1f}%)")

# Se não houver dados após filtrar, mostrar aviso
if len(df_filtrado) == 0:
    st.warning("⚠️ Nenhum cliente encontrado com os filtros selecionados. Tente ajustar os filtros.")
    st.stop()

## II. KPIs Principais
st.subheader("📈 Métricas Principais")

metricas = calcular_metricas(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Base Total", metricas['total'])
col2.metric("❌ Cancelamentos", metricas['cancelados'])
col3.metric("📊 Taxa de Churn", f"{metricas['taxa_churn']:.1f}%")
col4.metric("💰 Receita Perdida", formatar_moeda(metricas['receita_perdida']))

st.divider()

## III. Dados Brutos
st.subheader("🔍 Quem fica vs Quem sai")

if st.checkbox("Mostrar dados brutos"):
    st.dataframe(df_filtrado.head(10)) # Mostra 10 primeiras linhas

## IV. Gráficos de Análise
st.subheader("📊 Análises Visuais")

graph1, graph2 = st.columns(2)

# Gráfico 1: Atraso no Pagamento vs Cancelamento
with graph1:
    fig_dias = px.box(
        df_filtrado,
        x='cancelado',
        y='dias_atraso',
        color='cancelado',
        title="Dias de Atraso no Pagamento",
        labels={
            'cancelado': "Cancelou? (0=Não, 1=Sim)",
            'dias_atraso': "Dias de atraso"  
        },
        color_discrete_map={ATIVO: "#2ca02c", CANCELADOS: "#d62728"}
    )
    fig_dias.update_layout(showlegend=False)
    st.plotly_chart(fig_dias, use_container_width=True)

with graph2:
    fig_call = px.histogram(
        df_filtrado, 
        x="contatos_callcenter", 
        color="cancelado",
        title="Número de Ligações ao Suporte",
        barmode="group",
        labels={"contatos_callcenter": "Nº de Ligações"},
        color_discrete_map={ATIVO: "#2ca02c", CANCELADOS: "#d62728"}
    )
    st.plotly_chart(fig_call, use_container_width=True)
  
st.divider()  

## V. Calcular insights para Análise de Contrato
st.subheader("Análise por Tipo de Contrato")

insights = calcular_insight(df_filtrado)

fig_contrato = px.bar(
    insights['churn_contrato'],
    x='duracao_contrato',
    y='cancelado',
    title="Taxa de Cancelamento por Duração de Contrato",
    labels={
        'cancelado': "Taxa de Cancelamento (%)",
        'duracao_contrato': "Tipo de Contrato"
    },
    color='cancelado',
    color_continuous_scale="Reds"
)

fig_contrato.update_traces(hovertemplate='Tipo: %{x}<br>Taxa de Churn: %{y:.1f}%<extra></extra>')
st.plotly_chart(fig_contrato, use_container_width=True)

## VI. Evolução temporal de cancelmanentos
st.divider()
st.subheader("📈 Evolução de Cancelamentos no Tempo")

# Agrupar dados por mês
# 'M' = agrupar p/ mês (Month)
# 'ME' = fim do mês (Month End)
df_temporal = df_filtrado.copy()
df_temporal['mes'] = df_temporal['data_cadastro'].dt.to_period('M')

cancelamentos_por_mes = df_temporal.groupby('mes').agg({
    'cancelado': ['sum', 'count'] # sum = total cancelados, count = total clientes
}).reset_index()

# Renomear colunas para facilitar
cancelamentos_por_mes.columns = ['mes', 'cancelados', 'total_clientes']

# Cálculo da taxa churn mensal
cancelamentos_por_mes['taxa_churn'] = (
    cancelamentos_por_mes['cancelados'] /
    cancelamentos_por_mes['total_clientes'] * 100
)

# Converter Period para string
cancelamentos_por_mes['mes'] = cancelamentos_por_mes['mes'].astype(str)

# Criar gráfico de linha
fig_temporal = px.line(
    cancelamentos_por_mes,
    x='mes',
    y='taxa_churn',
    title="Taxa de Churn Mensal (%)",
    labels={
        'mes': 'Mês/Ano',
        'taxa_churn': 'Taxa de Churn (%)'
    },
    markers=True
)

# Personalizar gráfico
fig_temporal.update_traces(
    line_color='#d62728',  # Vermelho
    line_width=3,
    hovertemplate='<b>%{x}</b><br>Taxa de Churn: %{y:.1f}%<extra></extra>'
)

fig_temporal.add_hline(
    y=25,
    line_dash="dash",
    line_color="green",
    annotation_text="Meta: 25%",
    annotation_position="right"
)

st.plotly_chart(fig_temporal, use_container_width=True)

# Mostrar tabela com os dados
with st.expander("📊 Ver dados detalhados por mês"):
    st.dataframe(
        cancelamentos_por_mes.style.format({
            'taxa_churn': '{:.1f}%',
            'cancelados': '{:.0f}',
            'total_clientes': '{:.0f}'
        }),
        use_container_width=True
    )

## VII. Insights Automáticos
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

## VIII. Rodapé
st.divider()
st.caption("Dashboard feito por Vinícius Forte com Streamlit 🚀")