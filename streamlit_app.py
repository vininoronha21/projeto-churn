"""
Arquivo de entrada para o Streamlit Cloud.

Este arquivo existe apenas para redirecionar para src/app.py
O Streamlit Cloud requer um arquivo na raiz do projeto.
"""

import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import app
