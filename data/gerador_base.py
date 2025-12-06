import pandas as pd
import random


dados = [] # Estrutura para gerar 1000 clientes simulados
for i in range(1, 1001):
  id_user = i
  age = random.randint(18, 70)
  gender = random.choice(["Male", "Female"])
  customer_time = random.randint(1,60)
  frequency_use = random.randint(1, 30)

# Simulação: Contrato Mensal tem mais chance de ligar no call center e atrasar
  contract_duration = random.choice(["Monthly", "Annual", "Quarterly"])
  if contract_duration == "Monthly":
    contacts_callcenter = random.randint(0, 10) 
    days_late = random.randint(0, 25)
  else:
    contacts_callcenter = random.randint(0, 3)
    days_late = random.randint(0, 5)
  
  signature = random.choice(["Standard", "Premium", "Basic"])
  total_spent = round(random.uniform(100, 999), 2)

# Lógica do Cancelamento (Regra de Négocio Simulada)
# Se ligou muito, atrasou muito ou é contrato mensal, chance alta de cancelar
  canceled = 0 
  if contacts_callcenter > 4 or days_late > 15:
    canceled = 1

  if random.random() < 0.15: # Fator aleatório 
    canceled = 1 if canceled == 0 else 0
  
  dados.append([id_user, age, gender, customer_time,
                frequency_use, contacts_callcenter,
                days_late, signature, contract_duration,
                total_spent, canceled
                ])
  
# Criando o df(DataFrame)
df = pd.DataFrame(dados, columns=["id", "age", "gender", "customer_time",
                                  "frequency_use", "contacts_callcenter",
                                  "days_late", "signature", "contract_duration",
                                  "total_spent", "canceled"
                                  ])

df.to_csv("cancelamentos.csv", index=False)