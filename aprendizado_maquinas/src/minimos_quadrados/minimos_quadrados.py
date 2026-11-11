"""
Mínimos Quadrados (Least Squares)
Referência: Hagan, Neural Network Design, capítulo sobre Linear Filters.

Ideia central: encontrar w que minimize ||Xw - y||².
Solução analítica: w = (XᵀX)⁻¹ Xᵀ y (equação normal).
Não há treinamento iterativo — os coeficientes são calculados diretamente.

Dataset utilizado: Auto MPG (UCI Machine Learning Repository)
- X = horsepower  (potência do motor)
- y = mpg         (milhas por galão)
Relação esperada: LINEAR NEGATIVA — carros mais potentes consomem mais.
"""

# Bibliotecas para cálculos numéricos, manipulação do CSV e gráficos.
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


URL_AUTO_MPG = "https://raw.githubusercontent.com/plotly/datasets/master/auto-mpg.csv"

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_LOCAL   = os.path.join(_SCRIPT_DIR, "auto-mpg.csv")


def carregar_auto_mpg(caminho_local=CSV_LOCAL, url=URL_AUTO_MPG):
    """
    Retorna:
        X : np.ndarray (n,)  → horsepower
        y : np.ndarray (n,)  → mpg
    """
    if os.path.exists(caminho_local):
        df = pd.read_csv(caminho_local)
    else:
        df = pd.read_csv(url)
        df.to_csv(caminho_local, index=False)

    # Coerção numérica robusta (o UCI original usa '?' em horsepower).
    df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
    df['mpg']        = pd.to_numeric(df['mpg'],        errors='coerce')

    # Remove linhas com valores ausentes em qualquer uma das duas colunas.
    df = df.dropna(subset=['horsepower', 'mpg'])

    X = df['horsepower'].to_numpy(dtype=float)
    y = df['mpg'].to_numpy(dtype=float)
    return X, y


def minimos_quadrados_normal(X, y):
    """
    Calcula os coeficientes da regressão linear pela equação normal.

    X: matriz (n, d) com as características das amostras.
    y: vetor (n,) com os valores desejados.

    Retorna um vetor em que w[0] é o viés e w[1:] são os coeficientes.
    """

    # Adiciona uma coluna de 1s para incluir o viés no cálculo.
    X_aug = np.c_[np.ones(X.shape[0]), X]

    # Componentes da equação normal: A = XᵀX,  b = Xᵀy.
    A = X_aug.T @ X_aug
    b = X_aug.T @ y

    # Resolve A·w = b sem calcular a inversa explicitamente.
    w = np.linalg.solve(A, b)
    return w


def demo():
    """Ajusta uma reta aos dados reais do Auto MPG via mínimos quadrados."""

    # 1. Carrega os dados reais (398 amostras após limpeza).
    X, y = carregar_auto_mpg()

    # 2. Formata X como matriz (n, 1) — esperado pela função.
    X_2d = X.reshape(-1, 1)

    # 3. Calcula os coeficientes ótimos pela equação normal.
    w = minimos_quadrados_normal(X_2d, y)

    # 4. Métricas de qualidade do ajuste.
    y_pred = w[0] + w[1] * X
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2     = 1.0 - ss_res / ss_tot

    # 5. Saída no terminal.
    print("=== Mínimos Quadrados — Auto MPG ===")
    print(f"n amostras          : {len(y)}")
    print(f"bias (intercepto)   : {w[0]:.4f}")
    print(f"coef (horsepower)   : {w[1]:.4f}")
    print(f"R²                  : {r2:.4f}")
    print(f"Interpretação       : a cada +1 hp, o consumo cai ~{-w[1]:.4f} mpg")
    print(f"Modelo ajustado     : mpg ≈ {w[0]:.2f} + ({w[1]:.4f}) * horsepower")

    # 6. Gráfico.
    plt.figure(figsize=(9, 5))
    plt.scatter(X, y, s=14, alpha=0.6, label=f'Dados reais (n={len(y)})')

    x_line = np.linspace(X.min(), X.max(), 200)
    y_line = w[0] + w[1] * x_line
    plt.plot(x_line, y_line, 'r-', linewidth=2, label='Ajuste LS')

    plt.xlabel('Horsepower (potência)')
    plt.ylabel('MPG (milhas por galão)')
    plt.title('Mínimos Quadrados — Auto MPG (dados reais da UCI)')
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.show()


# Executa somente quando o arquivo é executado diretamente.
if __name__ == "__main__":
    demo()
