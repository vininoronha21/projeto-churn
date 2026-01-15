# 📊 Dashboard Análise de Churn - Previsão de Cancelamento de Clientes | (PT-BR)

---

> Dashboard interativo desenvolvido em Python e hospedado em Streamlit Cloud para análise e previsão de Churn, permitindo identificar padrões de cancelamento e reduzir a perda de clientes.

🔗 **[Acesse o dashboard online](https://dashboard-churn.streamlit.app)**

---

## 🎯 Sobre o projeto

Este projeto nasceu da necessidade das empresas compreenderem, de forma clara e objetiva, as causas do cancelamento de seus serviços. O dashboard desenvolvido permite:

- Visualizar a taxa de churn em tempo real
- Identificar os principais fatores que levam ao cancelamento
- Analisar a receita perdida
- Gerar insights automáticos para tomada de decisão

---

## 📸 Preview do Dashboard

<img src="assets/screenshots/tela_inicio.png" width="900" alt="Dashboard">

> *Visão geral do dashboard com KPIs principais.*

---

## ✨ Funcionalidades

### 📈 KPIs Principais

> Visualização total dos clientes, cancelamentos, taxa de churn e receita perdida

<img src="assets/screenshots/analise_visual.png" width="700" alt="Dashboard">

### 🎲 Dados Brutos

> Visualização opcional da base de dados completa

<img src="assets/screenshots/dados_brutos.png" width="700" alt="Dashboard">

### 💭 Insights Automáticos

> Insights que identificam padrões críticos e sugerem ações

<img src="assets/screenshots/insights.png" width="700" alt="Dashboard">

### 📊 Visualizações Interativas

- **Análise de Atraso de Pagamento**: Box Plot comparando dias de atraso entre clientes ativos e cancelados
- **Contatos com Call Center**: Histograma mostrando relação entre ligações ao suporte e cancelamento
- **Taxa por Tipo de Contrato**: Gráfico de barras identificando contratos com maior cancelamento

<img src="assets/screenshots/analise_tipo_contrato.png" width="700" alt="Dashboard">

### 🔼 Evolução Temporal

> Linha do tempo mostrando tendências de cancelamento ao longo dos meses com uma possível meta

<img src="assets/screenshots/evolucao.png" width="700" alt="Dashboard">

### 🎛️ Controles e Filtros

- **Filtro de Datas**: Seleção de período personalizado (data inicial e final)
- **Filtro por Contrato**: Análise focada em tipos específicos de contrato (Mensal, Trimestral, Anual)
- **Validação Inteligente**: Sistema que previne seleção de datas inválidas

<img src="assets/screenshots/filtro.png" width="700" alt="Dashboard">

---

## 🛠️ Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3.11-orange?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52.1-red?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.3.3-green?logo=plotly&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.5.0-3F4F75?logo=pandas&logoColor=white)
![Numpy](https://img.shields.io/badge/Numpy-2.3.5-blue?logo=numpy&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-7.3.3-black?logo=pytest&logoColor=white)

---

## 📂 Estrutura do Projeto

```
projeto-churn/
├── .devcontainer/           # Docker
│   └── devcontainer.json    # Ambiente de desenvolvimento
│
├── .streamlit/              # Configurações do Streamlit
│   └── config.toml          # Tema e configurações do servidor
│
├──assets/                   # Pasta com recursos estáticos 
│  └── screenshots/          # Screenshots do projeto
│
├── data/                    # Dados do projeto
│   └── cancelamentos.csv    # Base de dados de clientes (gerada)
│
├── src/                     # Código fonte principal
│   ├── __init__.py          # Inicializador do pacote
│   └── gerador_base.py      # Script para gerar dados fictícios
│
├── tests/                   # Testes automatizados
│   ├── __init__.py  
│   ├── test_calculos.py     # Testes de funções de cálculo
│   └── test_validacoes.py   # Testes de validação de dados
│
├── .gitignore               # Arquivos ignorados pelo Git
├── LICENSE                  # Licença
├── README_EN.md             # English Doc
├── README.md                # Documentação
├── requirements.txt         # Dependências do projeto
└── streamlit_app.py         # Raíz do projeto
```

---

## 💻 Melhorias Futuras

- [ ] Implementar modelo de Machine Learning para previsão de churn
- [ ] Criar sistema de alertas automáticos
- [ ] Adicionar exportação de relatórios em PDF
- [ ] Autenticação de usuários
- [ ] Integração com banco de dados (PostgreSQL)

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a passo

#### 1. Clone o repositório

```bash
git clone https://github.com/vininoronha21/projeto-churn.git
cd projeto-churn
```

#### 2. Crie um ambiente virtual (recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Windows:
venv\Scripts\activate

# Ativar no Linux/Mac:
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Rode o gerador para criar o CSV

```bash
python gerador_base.py
```

Você vai ver uma mensagem tipo:

```
✅ Base gerada com sucesso!
📁 Salvo em: {caminho_saida}
📊 Total de clientes: {XXXX}
📅 Período dos dados: {XXXX-XX-XX} até {XXXX-XX-XX}
```

Este comando criará o arquivo `data/cancelamentos.csv` com 1000 clientes fictícios.

#### 5. Execute o dashboard

```bash
streamlit run streamlit_app.py
```

---

## 🧪 Executar Testes

```bash
# Rodar todos os testes
pytest

# Rodar com detalhes (verbose)
pytest -v

# Rodar com cobertura de código
pytest --cov=src tests/

# Rodar testes específicos
pytest tests/test_calculos.py -v
```

**Exemplo de saída:**

```
================================ test session starts =================================
collected 15 items

tests/test_calculos.py ..........                                              [ 66%]
tests/test_validacoes.py .....                                                 [100%]

================================ 15 passed in 0.23s ==================================
```

---

## 📚 Referências

### Documentação Oficial

- [Streamlit](https://docs.streamlit.io/)
- [Pandas](https://pandas.pydata.org/docs/)
- [Plotly](https://plotly.com/python/)
- [Pytest](https://docs.pytest.org/)

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

Desenvolvido por **Vinícius Forte**

- 🐙 GitHub: [vininoronha21](https://github.com/vininoronha21)
- 💼 LinkedIn: [Vinícius Noronha](https://linkedin.com/in/viniciusnoronha)
- 📧 Email: contatovininoronha@gmail.com
