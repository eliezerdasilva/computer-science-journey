"""
Perceptron — o classificador linear mais simples.
Referência: Hagan, Neural Network Design, cap. sobre Perceptron Learning Rule.

Ideia central: se uma amostra é classificada errado, ajusta os pesos
para corrigir. Se acerta, não mexe. Converge se os dados forem
linearmente separáveis.

Regra de aprendizado: w ← w + η * (y_real - y_pred) * x
Onde y_pred = sign(w·x + b). O erro é 0 ou ±2.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import gerar_dados_classificacao, plot_hiperplano

class Perceptron:
    def __init__(self, lr=0.1, n_epocas=100, seed=42):
        self.lr = lr
        self.n_epocas = n_epocas
        self.seed = seed
        self.w = None
        self.b = None
    
    def _predicao(self, X):
        """Saída: +1 ou -1 com base no sinal de w·x + b."""
        return np.sign(X @ self.w + self.b)
    
    def treinar(self, X, y):
        """
        Loop de treinamento.
        Para cada época, para cada amostra:
        - Calcula predição
        - Se errou: w += lr * (y_real - y_pred) * x
        - Se acertou: não atualiza (erro = 0)
        """
        rng = np.random.RandomState(self.seed)
        n, d = X.shape
        self.w = np.zeros(d)
        self.b = 0.0
        
        for epoca in range(self.n_epocas):
            erros = 0
            # Embaralha a ordem das amostras a cada época (boa prática)
            indices = rng.permutation(n)
            for i in indices:
                xi = X[i]
                yi = y[i]
                y_pred = np.sign(xi @ self.w + self.b)
                if y_pred != yi:
                    # Atualização do Perceptron
                    erro = yi - y_pred  # será ±2
                    self.w += self.lr * erro * xi
                    self.b += self.lr * erro
                    erros += 1
            # Critério de parada: época sem erros (convergiu)
            if erros == 0:
                print(f"Convergiu na época {epoca + 1}")
                break
        else:
            print(f"Não convergiu em {self.n_epocas} épocas ({erros} erros finais)")
        
        return self

def demo():
    X, y = gerar_dados_classificacao(n=200, seed=3)
    perc = Perceptron(lr=0.1, n_epocas=50, seed=3)
    perc.treinar(X, y)
    acuracia = np.mean(perc._predicao(X) == y)
    print(f"Acurácia no treino: {acuracia:.2%}")
    plot_hiperplano(X, y, perc.w, perc.b, "Perceptron: fronteira aprendida")

if __name__ == "__main__":
    demo()