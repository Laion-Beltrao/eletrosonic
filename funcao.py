import pandas as pd
import openpyxl
import glob
import os
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import numpy as np

def prever_frota_eletrica(df, uf, municipio, meses_futuros=6):
    """
    Prevê a frota de veículos elétricos para um município usando regressão linear.
    
    Parâmetros:
        df             : DataFrame consolidado (df_combustivel com colunas normalizadas)
        uf             : Estado (ex: 'MINAS GERAIS')
        municipio      : Cidade (ex: 'BELO HORIZONTE')
        meses_futuros  : Quantos meses à frente projetar (padrão: 6)
    """

    # combustíveis considerados elétricos/híbridos -------------------------------------
    combustiveis_eletricos = [
        'ELETRICO/FONTE EXTERNA',
        'GASOLINA/ALCOOL/ELETRICO',
        'GASOLINA/ELETRICO', 
        'HIBRIDO PLUG-IN',
        'DIESEL/ELETRICO', 
        'ELETRICO/FONTE INTERNA', 
        'HIBRIDO',
        'ELETRICO',
        'ETANOL/ELETRICO',
        'HIBRIDO/GAS NATURAL VEICULAR'
    ]

    # normalizar inputs do usuário -------------------------------------
    uf = uf.strip().upper()
    municipio = municipio.strip().upper()

    # filtrar o DataFrame -------------------------------------
    df_filtrado = df[
        (df['uf'] == uf) &
        (df['municipio'] == municipio) &
        (df['combustivel'].isin(combustiveis_eletricos))
    ]

    # validar se encontrou dados -------------------------------------
    if df_filtrado.empty:
        print(f"\n Nenhum dado elétrico encontrado para '{municipio}' - '{uf}'.")
        print("   Verifique se o nome está correto. Municípios disponíveis nesse estado:")
        disponiveis = df[df['uf'] == uf]['municipio'].unique()
        if len(disponiveis) == 0:
            print(f"Nenhum registro encontrado para o estado '{uf}'.")
        else:
            print(f"{sorted(disponiveis)}")
        return None

    # agrupar por mês -------------------------------------
    df_modelo = df_filtrado.groupby('mes')['qtd_veiculos'].sum().reset_index()

    # dividir os dados em características (a matriz X) e a variável objetivo(y)
    X = df_modelo[['mes']].values
    y = df_modelo['qtd_veiculos'].values

    # treinar modelo -------------------------------------
    modelo = LinearRegression()
    modelo.fit(X, y)

    # métricas -------------------------------------
    y_pred_hist = modelo.predict(X)
    ss_res = np.sum((y - y_pred_hist) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2  = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    mae = np.mean(np.abs(y - y_pred_hist))

    # projeção -------------------------------------
    ultimo_mes   = int(df_modelo['mes'].max())
    meses_proj   = np.arange(ultimo_mes + 1, ultimo_mes + meses_futuros + 1).reshape(-1, 1)
    valores_proj = modelo.predict(meses_proj).astype(int)
    valores_proj = np.maximum(valores_proj, 0)   # sem valores negativos

    # imprimir resultados -------------------------------------
    print(f"\n{'='*50}")
    print(f"  {municipio} — {uf}")
    print(f"{'='*50}")
    print(f"  Crescimento mensal estimado : +{modelo.coef_[0]:,.1f} veículos/mês")
    print(f"  R²                          : {r2:.4f}")
    print(f"  MAE                         : {mae:,.1f} veículos")
    print(f"\n  Projeção — próximos {meses_futuros} meses:")

    nomes_meses = ['JAN','FEV','MAR','ABR','MAI','JUN',
                   'JUL','AGO','SET','OUT','NOV','DEZ']
    for mes_num, qtd in zip(meses_proj.flatten(), valores_proj): # transformar em array
        label = nomes_meses[(mes_num - 1) % 12]
        print(f"     Mês {mes_num:>2} ({label}): {qtd:>6,} veículos")
    print(f"{'='*52}\n")

    # gráfico
    todos_meses = list(X.flatten()) + list(meses_proj.flatten())
    todos_pred  = list(y_pred_hist) + list(valores_proj)
    labels_x    = [nomes_meses[(m - 1) % 12] for m in todos_meses]

    plt.figure(figsize=(12, 5))
    plt.plot(X.flatten(), y, marker='o', label='Histórico real', color='steelblue')
    plt.plot(todos_meses, todos_pred, linestyle='--', marker='s',
             markersize=4, label='Regressão + Projeção', color='tomato', alpha=0.8)
    plt.axvline(ultimo_mes + 0.5, color='gray', linestyle=':', alpha=0.6, label='Início da projeção')
    plt.title(f'Frota Elétrica — {municipio} ({uf})')
    plt.xlabel('Mês')
    plt.ylabel('Qtd. Veículos Elétricos')
    plt.xticks(ticks=todos_meses, labels=labels_x, rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return {
        'municipio'  : municipio,
        'uf'         : uf,
        'modelo'     : modelo,
        'r2'         : r2,
        'mae'        : mae,
        'projecao'   : dict(zip(meses_proj.flatten().tolist(), valores_proj.tolist()))
    }

""""
-> zip() - A função zip() pega duas listas e as combina, emparelhando o primeiro elemento 
com o segundo, e assim por diante.

-> flatten() - Transforma uma estrutura de dados (como um array NumPy multidimensional) em 
um único array unidimensional (uma linha). Isso é útil se meses_proj for uma matriz, 
garantindo que ela se torne uma lista linear.

"""