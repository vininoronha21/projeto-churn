## 🧪 Testes do Projeto

Este projeto utiliza **pytest** para execução de testes automatizados e **pytest-cov** para análise de cobertura de código.

## 📦 Instalação das dependências de teste

Antes de rodar os testes, instale as dependências:

```bash
pip install pytest pytest-cov
```

> Recomenda-se executar dentro de um **ambiente virtual **(.venv)** .

## ▶️ Como rodar os testes

🔹 Rodar todos os testes

```bash
pytest
```

🔹 Rodar testes com mais detalhes (verbose mode)

```bash
pytest -v
```

🔹 Rodar testes com cobertura de código (mostra a % do código testado)

```bash
pytest --cov=src tests/
```

🔹 Rodar apenas um arquivo de teste específico

```bash
pytest tests/test_calculos.py
```

🔹 Rodar apenas um teste específico
```bash
pytest tests/test_calculos.py::TestCalcularMetricas::test_calculo_com_dados_normais
```

## 📊 Exemplo de saída esperada
Ao rodar os testes, você verá algo como:
```bash
================================ test session starts =================================
collected 15 items

tests/test_calculos.py ..........                                              [ 66%]
tests/test_validacoes.py .....                                                 [100%]

================================ 15 passed in 0.23s ==================================
```

## 🤔 O que isso significa: 
- 15 testes coletados (cada . representa 1 teste que passou ✅ )
- Todos os testes passaram
- Execução rápida e sem erros
- Cobertura dividida entre testes de *cálculo* e *validações*

## ✅ Observações
- Os testes estão organizados na pasta *tests/*
- Os arquivos seguem o padrão test_*.py
- Os testes validam cálculos, regras de negócio e validações de entrada
