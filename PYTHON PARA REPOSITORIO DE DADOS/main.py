# -*- coding: utf-8 -*-
"""
Atividade 4 — Execução Completa (Main)
======================================
1️ Parte 1 — Matplotlib → gráficos de linha e dispersão  
2️ Parte 2 — NumPy → cálculos de média, desvio padrão e soma  
3️ Parte 3 — Pandas → análise e filtragem de dados de vendas  

------------------------
   pip install matplotlib numpy pandas
------------------------
   python main.py
"""

import importlib
import time
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

def run_module(name: str):
    print(f"\n=== Executando {name} ===")
    time.sleep(0.8)
    try:
        mod = importlib.import_module(name)
        # força reload para garantir que rode novamente mesmo se já importado
        importlib.reload(mod)
    except Exception as e:
        print(f"[ERRO] Falha ao executar {name}: {e}")
    print(f"=== Conclusão de {name} ===\n")

def main():
    print("\n Iniciando execução completa da Atividade 4...\n")
    etapas = ["parte1_matplotlib", "parte2_numpy", "parte3_pandas"]

    for etapa in etapas:
        run_module(etapa)
        time.sleep(1)

    print("Etapas executadas!")

if __name__ == "__main__":
    main()
