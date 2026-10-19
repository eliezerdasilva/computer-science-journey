"""
Adaline (ADAptive LINear Element) + Regra LMS (Least Mean Squares).
Referência: Hagan, Neural Network Design, cap. sobre Adaline.

Diferença crucial do Perceptron:
- Perceptron usa a SAÍDA DISCRETA (após sign) para corrigir.
- Adaline usa a SAÍDA CONTÍNUA (w·x + b) antes do sign.
  Ou seja, o erro é (y_real - saida_continua), que mede
  "o quão longe" estamos da fronteira ideal, não apenas se acertamos.

Isso torna o aprendizado mais suave e estável — a regra LMS (Widrow-Hoff)
minimiza o erro quadrático médio por gradiente descendente.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import gerar_dados_classificacao, plot_hiperplano

class Adaline:
    def __init__(self, lr=0.01, n_epocas=100, tol=1e-4, seed=42):
        self.lr = lr
        self.n_epocas = n_epocas
        self.tol = tol
        self.seed = seed
        self.w = None
        self.b = None
        self.historico_erro = []
    
    def _saida_continua(self, X):
        """Ativação linear: u = w·x + b (sem sign)."""
        return X @ self.w + self.b
    
    def _predicao(self, X):
        """Classificação final: sign(u)."""
        return np.sign(self._saida_continua(X))
    
    def treinar(self, X, y):
        """
        Loop LMS (online).
        Para cada amostra:
        - u = w·x + b (saída linear)
        - erro = y_real - u (erro contínuo)
        - w += lr * erro * x;  b += lr * erro
        O erro quadrático médio é registrado por época para monitorar.
        """
        rng = np.random.RandomState(self.seed)
        n, d = X.shape
        self.w = rng.normal(0, 0.1, d)
        self.b = 0.0
        self.historico_erro = []
        
        for epoca in range(self.n_epocas):
            indices = rng.permutation(n)
            erro_total = 0.0
            for i in indices:
                xi = X[i]
                yi = y[i]
                u = xi @ self.w + self.b          # saída contínua
                erro = yi - u                      # erro LMS
                self.w += self.lr * erro * xi
                self.b += self.lr * erro
                erro_total += erro ** 2
            mse = erro_total / n
            self.historico_erro.append(mse)
            # Critério de parada: melhora insuficiente
            if epoca > 5 and abs(self.historico_erro[-2] - mse) < self.tol:
                print(f"Convergiu (estável) na época {epoca + 1}, MSE={mse:.6f}")
                break
        
        return self

def demo():
    X, y = gerar_dados_classificacao(n=200, seed=5)
    ada = Adaline(lr=0.01, n_epocas=200, seed=5)
    ada.treinar(X, y)
    acuracia = np.mean(ada._predicao(X) == y)
    print(f"Acurácia no treino: {acuracia:.2%}")
    
    # Plot da convergência do MSE
    import matplotlib.pyplot as plt
    plt.figure(figsize=(7, 4))
    plt.plot(ada.historico_erro, 'b-', linewidth=2)
    plt.xlabel('Época'); plt.ylabel('MSE')
    plt.title('Adaline/LMS: convergência do erro quadrático médio')
    plt.grid(True); plt.show()
    
    plot_hiperplano(X, y, ada.w, ada.b, "Adaline: fronteira aprendida")

if __name__ == "__main__":
    demo()