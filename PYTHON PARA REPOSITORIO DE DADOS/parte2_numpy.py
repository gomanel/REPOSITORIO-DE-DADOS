# -*- coding: utf-8 -*-
"""
Parte 2 — Fundamentos de Estruturas de Dados e Funções em NumPy (VERSÃO ORIGINAL)
- Cria uma matriz 2D (4x3)
- Calcula média, desvio padrão e soma por eixo (colunas e linhas) e geral

Como executar no seu PC:
  1) (Se necessário) pip install numpy
  2) python part2_numpy.py
"""
import numpy as np

# Matriz 4x3 (linhas = "registros", colunas = "medidas")
matriz = np.array([
    [10, 15, 20],
    [ 7,  9, 12],
    [13, 18, 21],
    [ 5,  6,  8]
])

# Estatísticas por eixo e geral
print("=== NumPy — Estatísticas por COLUNA (axis=0) ===")
print("Média:", matriz.mean(axis=0))
print("Desvio padrão:", matriz.std(axis=0, ddof=0))
print("Soma:", matriz.sum(axis=0))

print("\n=== NumPy — Estatísticas por LINHA (axis=1) ===")
print("Média:", matriz.mean(axis=1))
print("Desvio padrão:", matriz.std(axis=1, ddof=0))
print("Soma:", matriz.sum(axis=1))

print("\n=== NumPy — Estatísticas GERAIS ===")
print("Média:", matriz.mean(), "| Desvio padrão:", matriz.std(ddof=0), "| Soma:", matriz.sum())