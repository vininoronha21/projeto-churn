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
