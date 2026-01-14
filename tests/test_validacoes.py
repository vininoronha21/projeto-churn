"""
Testes para funções de validação de dados.

Essas funções garantem que os dados estão no formato correto antes de processar o dashboard.
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from streamlit_app import validar_dados, COLUNAS_NECESSARIAS


class TestValidarDados:
  """
  Teste para a função validar_dados
  """

  def test_dataframe_valido(self):
    """
    Testa df com todas as colunas necessárias.
    """

    # Arrange: Criar df com TODAS colunas necessárias
    df_valido = pd.DataFrame(columns=COLUNAS_NECESSARIAS)

    # Act: Executa a ação
    valido, faltantes = validar_dados(df_valido)

    # Assert: Verifica o resultado
    assert valido == True, "Deveria ser válido"
    assert len(faltantes) == 0, "Não deveria ter colunas faltantes"

  def test_dataframe_com_colunas_faltantes(self):
      """
      Testa df sem algumas colunas obrigatórias.
      """
        
      df_incompleto = pd.DataFrame(columns=['id_cliente', 'cancelado'])
        
        
      valido, faltantes = validar_dados(df_incompleto)
        
        
      assert valido == False, "Não deveria ser válido"
      assert len(faltantes) > 0, "Deveria identificar colunas faltantes"
      assert 'idade' in faltantes
      assert 'genero' in faltantes
    
  def test_dataframe_none(self):
      """
      Testa comportamento quando recebe None (arquivo não encontrado).
      """
        
      valido, faltantes = validar_dados(None)
        
        
      assert valido == False
      assert faltantes == []  # Retorna lista vazia quando é None
    
  def test_dataframe_com_colunas_extras(self):
      """
      Testa df com colunas extras (além das necessárias).
      Isso NÃO é um problema - deveria ser válido!
      """
        
      colunas = COLUNAS_NECESSARIAS + ['coluna_extra_qualquer']
      df_com_extras = pd.DataFrame(columns=colunas)
        
        
      valido, faltantes = validar_dados(df_com_extras)
        
        
      assert valido == True, "Colunas extras não deveriam invalidar"
      assert len(faltantes) == 0
