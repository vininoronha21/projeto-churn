"""
Arquivo de entrada para o Streamlit Cloud.

Este arquivo existe apenas para redirecionar para src/app.py
O Streamlit Cloud requer um arquivo na raiz do projeto.
"""

import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from src import app
