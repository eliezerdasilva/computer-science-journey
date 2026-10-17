"""
Mínimos Quadrados (Least Squares)
Referência: Hagan, Neural Network Design, cap. sobre Linear Filters.

Ideia central: encontrar w que minimize ||Xw - y||².
Solução analítica: w = (XᵀX)⁻¹ Xᵀ y  (equação normal).
Não há iteratividade — é uma solução fechada.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils import gerar_dados_linear
import matplotlib.pyplot as plt

def minimos_quadrados_normal(X, y):
    """
    Resolve via equação normal: w = (XᵀX)⁻¹ Xᵀ y.
    X deve incluir coluna de 1s para o bias.
    
    Passos:
    1. Adiciona coluna de 1s → [1, x1, x2, ...]
    2. Calcula XᵀX (matriz de correlação)
    3. Calcula Xᵀy (vetor de correlação com alvo)
    4. Resolve o sistema linear (mais estável que inverter)
    """
    X_aug = np.c_[np.ones(X.shape[0]), X]  # coluna de bias
    # np.linalg.solve é numericamente mais estável que inv(X.T @ X) @ X.T @ y
    A = X_aug.T @ X_aug
    b = X_aug.T @ y
    w = np.linalg.solve(A, b)
    return w  # w[0] = bias, w[1:] = coeficientes

def demo():
    """Demonstração: ajuste de reta em dados sintéticos."""
    X, y = gerar_dados_linear(n=80, ruido=1.2)
    
    # Adiciona dimensão para o formato esperado (n, 1)
    X_2d = X.reshape(-1, 1)
    w = minimos_quadrados_normal(X_2d, y)
    
    print("=== Mínimos Quadrados ===")
    print(f"Coeficientes encontrados: bias={w[0]:.4f}, coef={w[1]:.4f}")
    print(f"Valor esperado (dados gerados): bias=1.0, coef=2.0")
    
    # Visualização
    plt.figure(figsize=(7, 5))
    plt.scatter(X, y, alpha=0.6, label='Dados observados')
    x_line = np.linspace(X.min(), X.max(), 100)
    y_line = w[0] + w[1] * x_line
    plt.plot(x_line, y_line, 'r-', linewidth=2, label='Ajuste LS')
    plt.xlabel('x'); plt.ylabel('y')
    plt.title('Mínimos Quadrados: ajuste de reta')
    plt.legend(); plt.grid(True)
    plt.show()

if __name__ == "__main__":
    demo()