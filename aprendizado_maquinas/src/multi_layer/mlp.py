"""
Multi Layer Perceptron (MLP) — rede com camada oculta e backpropagation.
Referência: Hagan, Neural Network Design, cap. sobre Backpropagation.

Ideia central: sem camada oculta, só conseguimos fronteiras lineares.
Com uma camada oculta + ativação não-linear (sigmoide/tanh), podemos
aproximar qualquer função (teorema da aproximação universal).

Backpropagation = regra da cadeia para calcular o gradiente do erro
em relação a TODOS os pesos da rede, camada por camada, de trás pra frente.

Implementação didática: 1 camada oculta, ativação tanh na oculta,
saída linear (para classificação binária com rótulos ±1, usamos sign na predição).
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils import gerar_dados_classificacao, plot_hiperplano

class MLP:
    def __init__(self, n_oculta=5, lr=0.01, n_epocas=500, seed=42):
        self.n_oculta = n_oculta
        self.lr = lr
        self.n_epocas = n_epocas
        self.seed = seed
        self.W1 = None  # pesos entrada → oculta  (d, n_oculta)
        self.b1 = None  # bias da oculta          (n_oculta,)
        self.W2 = None  # pesos oculta → saída     (n_oculta, 1)
        self.b2 = None  # bias da saída            (1,)
        self.historico_erro = []
    
    def _forward(self, X):
        """
        Propagação direta.
        Z1 = X @ W1 + b1     (pré-ativação da oculta)
        A1 = tanh(Z1)        (ativação não-linear)
        Z2 = A1 @ W2 + b2    (saída linear, para classificação usamos sign)
        """
        Z1 = X @ self.W1 + self.b1
        A1 = np.tanh(Z1)
        Z2 = A1 @ self.W2 + self.b2
        return Z1, A1, Z2
    
    def _predicao(self, X):
        """Classificação: sign da saída linear."""
        _, _, Z2 = self._forward(X)
        return np.sign(Z2).ravel()
    
    def treinar(self, X, y):
        """
        Treinamento com backpropagation (batch completo por época).
        
        Passos por época:
        1. Forward: calcula saídas.
        2. Calcula erro (y - Z2).
        3. Backward: gradiente do erro em relação a cada peso.
           - dZ2 = -2 * (y - Z2) / n        (derivada do MSE)
           - dW2 = A1.T @ dZ2;  db2 = soma(dZ2)
           - dA1 = dZ2 @ W2.T
           - dZ1 = dA1 * (1 - A1²)         (derivada da tanh)
           - dW1 = X.T @ dZ1;  db1 = soma(dZ1)
        4. Atualiza pesos: w -= lr * gradiente
        """
        rng = np.random.RandomState(self.seed)
        n, d = X.shape
        y_col = y.reshape(-1, 1)
        
        # Inicialização Xavier (ajuda na convergência)
        self.W1 = rng.normal(0, np.sqrt(2.0/d), (d, self.n_oculta))
        self.b1 = np.zeros(self.n_oculta)
        self.W2 = rng.normal(0, np.sqrt(2.0/self.n_oculta), (self.n_oculta, 1))
        self.b2 = np.zeros(1)
        
        for epoca in range(self.n_epocas):
            # --- Forward ---
            Z1, A1, Z2 = self._forward(X)
            
            # --- Erro ---
            erro = y_col - Z2
            mse = np.mean(erro ** 2)
            self.historico_erro.append(mse)
            
            # --- Backward (regra da cadeia) ---
            # Gradiente da saída (derivada de MSE em relação a Z2)
            dZ2 = -2.0 * erro / n
            # Gradientes da camada de saída
            dW2 = A1.T @ dZ2
            db2 = np.sum(dZ2, axis=0)
            # Gradiente da camada oculta
            dA1 = dZ2 @ self.W2.T
            dZ1 = dA1 * (1 - A1 ** 2)  # derivada da tanh: 1 - tanh²
            dW1 = X.T @ dZ1
            db1 = np.sum(dZ1, axis=0)
            
            # --- Atualização (gradiente descendente) ---
            self.W1 -= self.lr * dW1
            self.b1 -= self.lr * db1
            self.W2 -= self.lr * dW2
            self.b2 -= self.lr * db2
        
        return self

def demo():
    # Dados NÃO linearmente separáveis: duas "luas" ou círculos concêntricos
    from sklearn.datasets import make_moons
    X, y_bin = make_moons(n_samples=300, noise=0.15, random_state=42)
    y = 2 * y_bin - 1  # converter para {-1, +1}
    # Normalizar (MLP é sensível à escala)
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    
    mlp = MLP(n_oculta=8, lr=0.05, n_epocas=800, seed=42)
    mlp.treinar(X, y)
    acuracia = np.mean(mlp._predicao(X) == y)
    print(f"MLP (1 oculta, 8 neurônios) — Acurácia: {acuracia:.2%}")
    
    # Visualização da fronteira não-linear
    import matplotlib.pyplot as plt
    xx, yy = np.meshgrid(np.linspace(X[:,0].min()-0.5, X[:,0].max()+0.5, 200),
                         np.linspace(X[:,1].min()-0.5, X[:,1].max()+0.5, 200))
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = mlp._predicao(grid).reshape(xx.shape)
    
    plt.figure(figsize=(7, 5))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
    plt.scatter(X[y==1, 0], X[y==1, 1], c='blue', edgecolors='k', label='+1')
    plt.scatter(X[y==-1, 0], X[y==-1, 1], c='red', edgecolors='k', label='-1')
    plt.title('MLP: fronteira de decisão não-linear (make_moons)')
    plt.legend(); plt.grid(True); plt.show()

if __name__ == "__main__":
    demo()