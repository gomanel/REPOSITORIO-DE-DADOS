# -*- coding: utf-8 -*-
"""
Parte 1 — Visualização Gráfica com Matplotlib (VERSÃO ORIGINAL)
- Gráfico de linha: variação de temperatura ao longo de uma semana
- Gráfico de dispersão: relação entre duas variáveis (horas de estudo x nota)

Como executar no seu PC:
  1) Instale as dependências (uma vez): 
     pip install matplotlib numpy pandas
  2) Rode este arquivo:
     python part1_matplotlib.py
  3) Resultados:
     - Mostra 2 gráficos na tela (se houver interface gráfica).
     - Também salva as imagens: grafico_temperatura.png e grafico_estudo_vs_nota.png
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Garante que o script também funcione em ambiente sem display (salvando as imagens)
try:
    matplotlib.use("Agg")
except Exception:
    pass

# ------- Gráfico de linha: temperatura por dia -------
dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
temperaturas_c = np.array([22.0, 23.5, 21.0, 24.2, 25.3, 26.1, 24.8])

plt.figure(figsize=(8, 4))
plt.plot(dias, temperaturas_c, marker="o")
plt.title("Variação de Temperatura em uma Semana (°C)")
plt.xlabel("Dia da Semana")
plt.ylabel("Temperatura (°C)")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_temperatura.png", dpi=120)
try:
    plt.show()
except Exception:
    pass
plt.close()

# ------- Gráfico de dispersão: horas de estudo x nota -------
horas_estudo = np.array([1, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7])
notas = np.array([55, 60, 62, 65, 67, 74, 78, 80, 86, 92])

plt.figure(figsize=(8, 4))
plt.scatter(horas_estudo, notas)
plt.title("Relação entre Horas de Estudo e Nota")
plt.xlabel("Horas de Estudo")
plt.ylabel("Nota (0–100)")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_estudo_vs_nota.png", dpi=120)
try:
    plt.show()
except Exception:
    pass
plt.close()