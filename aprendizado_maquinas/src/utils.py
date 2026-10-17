"""Funções utilitárias para geração de dados e visualização."""
import numpy as np
import matplotlib.pyplot as plt

def gerar_dados_linear(n=100, ruido=1.0, seed=42):
    """Gera dados sintéticos para regressão linear: y = 2x + 1 + ruído."""
    rng = np.random.RandomState(seed)
    X = rng.uniform(-3, 3, n)
    y = 2 * X + 1 + rng.normal(0, ruido, n)
    return X, y

def gerar_dados_classificacao(n=200, seed=42):
    """Gera duas classes linearmente separáveis com margem."""
    rng = np.random.RandomState(seed)
    # Classe -1: centrada em (-1.5, -1.5)
    X_neg = rng.normal(-1.5, 0.5, (n//2, 2))
    y_neg = -np.ones(n//2)
    # Classe +1: centrada em (1.5, 1.5)
    X_pos = rng.normal(1.5, 0.5, (n//2, 2))
    y_pos = np.ones(n//2)
    X = np.vstack([X_neg, X_pos])
    y = np.concatenate([y_neg, y_pos])
    return X, y

def plot_hiperplano(X, y, w, b, titulo="Fronteira de decisão"):
    """Plota pontos e a reta w·x + b = 0."""
    plt.figure(figsize=(6, 5))
    plt.scatter(X[y==1, 0], X[y==1, 1], c='blue', label='Classe +1', alpha=0.6)
    plt.scatter(X[y==-1, 0], X[y==-1, 1], c='red', label='Classe -1', alpha=0.6)
    # Reta: w0*x0 + w1*x1 + b = 0  =>  x1 = -(w0*x0 + b)/w1
    x_vals = np.array([X[:,0].min()-0.5, X[:,0].max()+0.5])
    y_vals = -(w[0]*x_vals + b) / w[1]
    plt.plot(x_vals, y_vals, 'k--', label='Fronteira')
    plt.xlabel('x0'); plt.ylabel('x1')
    plt.title(titulo); plt.legend(); plt.grid(True)
    plt.show()