"""
Gerador de base de dados para análise de churn.

Este script cria um CSV com dados fictícios de clientes,
INCLUINDO datas de cadastro para permitir análises temporais.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
