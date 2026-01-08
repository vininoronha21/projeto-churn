"""
Gerador de base de dados para análise de churn.

Este script cria um CSV com dados fictícios de clientes,
INCLUINDO datas de cadastro para permitir análises temporais.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)


def gerar_data_cadastro(n_clientes, data_inicio='2024-01-01', data_fim='2025-12-31'):
    """
    Gera datas aleatórias de cadastro para os clientes.
    """
    # Converter str para objetos datetime
    inicio = pd.to_datetime(data_inicio)
    fim = pd.to_datetime(data_fim)

    # Calcular quantos dias existem entre as datas
    dias_diferenca = (fim - inicio).days

    # Gerar números aleatórios de dias
    dias_aleatorios = np.random.randint(0, dias_diferenca, size=n_clientes)

    # Somar os dias à data inicial
    datas = [inicio + timedelta(days=int(d)) for d in dias_aleatorios]

    # Converter para string no formato YYYY-MM-DD
    datas_formatadas = [d.strftime('%Y-%m-%d') for d in datas]

    return datas_formatadas


def gerar_base_churn(n_clientes=1000, caminho_saida='data/cancelamentos.csv'):
        """
        Gera base completa de dados com informações realistas.
        """

        print(f"🔄 Gerando base com {n_clientes} clientes...")

        # IDs únicos
        ids = range(1, n_clientes + 1)

        datas_cadastro = gerar_data_cadastro(n_clientes)

        # Dados demográficos
        idades = np.random.randint(20, 65, n_clientes)
        generos = np.random.choice(['M', 'F'], n_clientes)

        # Dados de uso
        tempo_cliente = np.random.randint(1, 60, n_clientes) # meses
        frequencia_uso = np.random.randint(0, 50, n_clientes) # acessos/mês

        # Dados de suporte
        contatos_callcenter = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8],
                                               n_clientes,
                                               p=[0.3, 0.25, 0.2, 0.1, 0.08, 0.04, 0.02, 0.005, 0.005])
        
        # Dados financeiros
        dias_atraso = np.random.choice([0, 5, 10, 15, 20, 30, 45, 60],
                                       n_clientes,
                                       p=[0.5, 0.15, 0.1, 0.1, 0.05, 0.05, 0.03, 0.02])
        
        assinaturas = np.random.choice(['Basico', 'Standard', 'Premium'],
                                       n_clientes,
                                       p=[0.5, 0.35, 0.15])
        
        contratos = np.random.choice(['Mensal', 'Trimestral', 'Anual'],
                                     n_clientes,
                                     p=[0.6, 0.25, 0.15])
        
        # Total gasto (correlacionado com tipo de assinatura)
        total_gasto = []
        for assinatura in assinaturas:
            if assinatura == 'Basico':
                gasto = np.random.uniform(100, 500)
            elif assinatura == 'Standard':
                gasto = np.random.uniform(500, 2000)
            else:
                gasto = np.random.uniform(2000, 10000)
            total_gasto.append(round(gasto, 2))

