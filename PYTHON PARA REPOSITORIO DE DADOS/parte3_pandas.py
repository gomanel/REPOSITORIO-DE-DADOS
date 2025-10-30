# -*- coding: utf-8 -*-
"""
Parte 3 — Princípios de Manipulação e Análise de Dados em Pandas (VERSÃO ORIGINAL)
- Carrega um dataset simples (vendas) em um DataFrame
- Exibe head, info e estatísticas descritivas
- Filtra registros por um critério (receita >= 200) e ordena

Como executar no seu PC:
  1) (Se necessário) pip install pandas
  2) Garanta que o arquivo 'vendas_exemplo.csv' esteja na mesma pasta (gerado aqui na primeira execução)
  3) python part3_pandas.py
"""
import io
import pandas as pd
from pathlib import Path

# Cria um dataset simples se ainda não existir (vendas_exemplo.csv)
csv_path = Path("vendas_exemplo.csv")
if not csv_path.exists():
    df_seed = pd.DataFrame({
        "data": pd.to_datetime([
            "2025-10-20", "2025-10-20", "2025-10-21", "2025-10-21", "2025-10-22",
            "2025-10-22", "2025-10-23", "2025-10-23", "2025-10-24", "2025-10-24"
        ]),
        "produto": ["Camiseta", "Calça", "Camiseta", "Tênis", "Calça",
                    "Boné", "Camiseta", "Tênis", "Boné", "Calça"],
        "unidades": [3, 2, 4, 1, 5, 2, 6, 2, 4, 3],
        "preco_unit": [49.9, 129.9, 49.9, 299.0, 129.9, 39.9, 49.9, 299.0, 39.9, 129.9]
    })
    df_seed["receita"] = df_seed["unidades"] * df_seed["preco_unit"]
    df_seed.to_csv(csv_path, index=False)

# Carrega o CSV e realiza as operações pedidas
df = pd.read_csv(csv_path, parse_dates=["data"])

print("=== Pandas — head() ===")
print(df.head())

buf = io.StringIO()
df.info(buf=buf)
print("\n=== Pandas — info() ===")
print(buf.getvalue())

numericas = df.select_dtypes(include=["number"])
print("=== Pandas — describe() numérico ===")
print(numericas.describe())

filtro = df[df["receita"] >= 200].sort_values(by="receita", ascending=False)
print("\n=== Pandas — filtro (receita >= 200) ===")
print(filtro)