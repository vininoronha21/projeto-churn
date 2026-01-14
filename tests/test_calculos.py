"""
Testes para função de cálculo do dashboard.

Este arquivo testa se os cálculos matemáticos estão corretos.
Cada função test_* é um teste independente.
"""

import pytest
import pandas as pd
import sys
import os

# Adiciona o diretório 'src' ao path para importar o app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Agora é possível importar as funções do app.py
from streamlit_app import calcular_metricas, formatar_moeda, calcular_insight, CANCELADOS, ATIVO


class TestCalcularMetricas:
  """
  Agrupa todos os testes da função calcular_metricas.

  Usarei classes pela organização, assim fica fácil saber que esses testes são relacionados à mesma função.
  """

  def test_calculo_com_dados_normais(self):
    """
    Testa se os cálculos básicos estão corretos com dados simples.

    PADRÃO AAA (Arrange, Act, Assert):
    - Arrange: Preparar os dados
    - Act: Executar a função
    - Assert: Verificar se o resultado está correto
    """
    # Arrange = Criar dados de teste
    # 4 Clientes: 2 cancelaram (50%), gastaram R$100 cada
    dados_teste = pd.DataFrame({
      'id_cliente': [1, 2, 3, 4],
      'cancelado': [1, 1, 0, 0],
      'total_gasto': [100, 100, 50, 50]
    })

    # Act: Chama a função que queremos testar
    resultado = calcular_metricas(dados_teste)

    # Assert: Verifica se os resultados estão corretos
    assert resultado['total'] == 4, "Deveria ter 4 clientes no total"
    assert resultado['cancelados'] == 2, "Deveria ter 2 cancelados"
    assert resultado['taxa_churn'] == 50.0, "Taxa de churn deveria ser 50%"
    assert resultado['receita_perdida'] == 200, "Receita perdida deveria ser R$200"

  def test_dataframe_vazio(self):
    """
    Testa o comportamento com df vazio.

    Por que é importante? O código pode receber dados vazios, como o CSV pode estar corrompido ou vazio. Precisa-se resolver.
    """

    dados_vazios = pd.DataFrame(columns=['cancelado', 'total_gasto'])

    resultado = calcular_metricas(dados_vazios)

    # Com 0 clientes = tudo deveria ser 0
    assert resultado['total'] == 0
    assert resultado['cancelados'] == 0
    assert resultado['taxa_churn'] == 0
    assert resultado['receita_perdida'] == 0
    
  def test_todos_clientes_cancelaram(self):
    """
    Testa cenário extremo: 100% cancelaram.
    """

    dados_teste = pd.DataFrame({
      'cancelado': [1, 1, 1],
      'total_gasto': [100, 200, 300]
    })

    resultado = calcular_metricas(dados_teste)

    assert resultado['taxa_churn'] == 100.0, "Deveria ser 100% de churn"
    assert resultado['receita_perdida'] == 600, "Perdeu toda a receita"

  def test_nenhum_cliente_cancelou(self):
    """
    Testa o cenário ideal: 0% de cancelamento.
    """

    dados_teste = pd.DataFrame({
      'cancelado': [0, 0, 0],
      'total_gasto': [100, 200, 300]
    })

    resultado = calcular_metricas(dados_teste)

    assert resultado['taxa_churn'] == 0.0, "Deveria ser 0% de churn"
    assert resultado['receita_perdida'] == 0, "Não perdeu receita"


class TestFormatarMoeda:
  """
  Testes para a função de formatação de moeda.
  """

  def test_formatar_valor_simples(self):
    """
    Testa formatação de valores simples.
    """
    assert formatar_moeda(100) == "R$100,00"
    assert formatar_moeda(1000) == "R$1.000,00"
    assert formatar_moeda(1000000) == "R$1.000.000,00"
  
  def test_formatar_valor_com_centavos(self):
    """
    Testa se os centavos estão formatados corretamente.
    """
    assert formatar_moeda(123.45) == "R$123,45"
    assert formatar_moeda(1234.56) == "R$1.234,56"
  
  def test_formatar_zero(self):
    """
    Testa formatação do valor zero.
    """
    assert formatar_moeda(0) == "R$0,00"
  
  def test_formatar_valor_negativo(self):
    """
    Testa formatação de valores negativos (caso aconteça uma devolução).
    """
    resultado = formatar_moeda(-100)
    assert "100" in resultado and "-" in resultado



  class TestCalcularInsight:
    """
    Testes para a função que calcula insights automáticos.
    """

    def test_calculo_medias_atraso(self):
      """
      Testa se as médias de atraso estao sendo calculadas corretamente.
      """

      dados_teste = pd.DataFrame({
        'cancelado': [CANCELADOS, CANCELADOS, ATIVO, ATIVO],
        'dias_atraso': [30, 40, 5, 15],
        'duracao_contrato': ['Mensal', 'Mensal', 'Anual', 'Anual']
      })

      insights = calcular_insight(dados_teste)

      assert insights['media_atraso_cancelados'] == 35.0
      assert insights['media_atraso_ativos'] == 10.0

    def test_identificacao_pior_contrato(self):
      """
      Testa se identifica corretamente qual tipo de contrato tem mais churn
      """

      dados_teste = pd.DataFrame({
        'cancelado': [1, 1, 0, 0],
        'dias_atraso': [10, 20, 5, 5],
        'duracao_contrato': ['Mensal', 'Mensal', 'Anual', 'Anual']
      })

      insights = calcular_insight(dados_teste)

      assert insights['pior_contrato'] == 'Mensal'
      

class TestConverterColunaData:
  """
  Testes para a função de conversão de datas.
  """

  def test_conversao_data_valida(self):
    """
    Testa se converte strings de data corretamente.
    """

    df_teste = pd.DataFrame({
      'data_cadastro': ['2024-01-01', '2024-06-20', '2025-12-30']
    })

    from streamlit_app import converter_coluna_data
    df_convertido = converter_coluna_data(df_teste)

    # Verifica se a coluna é do tipo datetime
    assert pd.api.types.is_datetime64_any_dtype(df_convertido['data_cadastro'])
    assert df_convertido['data_cadastro'].notna().all()

  def test_conversaodata_invalida(self):
    """
    Testa comportamento com datas inválidas.
    """

    df_teste = pd.DataFrame({
      'data_cadastro': ['2024-01-01' 'data_invalida', '2025-99-99']
    })

    from streamlit_app import converter_coluna_data
    df_convertido = converter_coluna_data(df_teste)

    # Primeira linha deve ser válida
    assert pd.notna(df_convertido.loc[0, 'data_cadastro'])
    # Linhas 2 e 3 devem ser NaT (Not a Time)
    assert pd.isna(df_convertido.loc[1, 'data_cadastro'])
    assert pd.isna(df_convertido.loc[2, 'data_cadastro'])
