import pandas as pd
import random

dados = []  # Estrutura para gerar 1000 clientes simulados

for i in range(1, 1001):
    id_cliente = i
    idade = random.randint(18, 70)
    genero = random.choice(["Masculino", "Feminino"])
    tempo_cliente = random.randint(1, 60)
    frequencia_uso = random.randint(1, 30)
    
    # Simulação: Contrato Mensal tem mais chance de ligar no call center e atrasar
    duracao_contrato = random.choice(["Mensal", "Anual", "Trimestral"])
    
    if duracao_contrato == "Mensal":
        contatos_callcenter = random.randint(0, 10) 
        dias_atraso = random.randint(0, 25)
    else:
        contatos_callcenter = random.randint(0, 3)
        dias_atraso = random.randint(0, 5)
    
    assinatura = random.choice(["Standard", "Premium", "Básico"])
    total_gasto = round(random.uniform(100, 999), 2)
    
    # Lógica do Cancelamento (Regra de Negócio Simulada)
    # Se ligou muito, atrasou muito ou é contrato mensal, chance alta de cancelar
    cancelado = 0 
    
    if contatos_callcenter > 4 or dias_atraso > 15:
        cancelado = 1
    
    if random.random() < 0.15:  # Fator aleatório 
        cancelado = 1 if cancelado == 0 else 0
    
    dados.append([
        id_cliente, idade, genero, tempo_cliente,
        frequencia_uso, contatos_callcenter,
        dias_atraso, assinatura, duracao_contrato,
        total_gasto, cancelado
    ])

# Criando o DataFrame
df = pd.DataFrame(dados, columns=[
    "id_cliente", "idade", "genero", "tempo_cliente",
    "frequencia_uso", "contatos_callcenter",
    "dias_atraso", "assinatura", "duracao_contrato",
    "total_gasto", "cancelado"
])

df.to_csv("cancelamentos.csv", index=False)
print(f"✅ Arquivo 'cancelamentos.csv' gerado com sucesso!")
print(f"📊 Total de registros: {len(df)}")
print(f"❌ Clientes cancelados: {df['cancelado'].sum()}")
print(f"📈 Taxa de churn: {(df['cancelado'].sum() / len(df) * 100):.1f}%")