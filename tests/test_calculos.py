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
from app import calcular_metricas, formatar_moeda, calcular_insight, CANCELADOS, ATIVO


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
    