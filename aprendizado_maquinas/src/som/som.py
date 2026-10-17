"""
Self-Organizing Map (SOM) — Mapa Auto-Organizável de Kohonen.
Referência: Hagan, Neural Network Design, cap. sobre Competitive Networks.

Ideia central: uma grade de neurônios compete para "vencer" cada amostra.
O vencedor (BMU — Best Matching Unit) e seus vizinhos de grade são
puxados em direção à amostra. Com o tempo, o mapa se organiza
topologicamente: amostras similares ativam neurônios próximos.

Aprendizado NÃO supervisionado.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib.pyplot as plt

class SOM:
    def __init__(self, grid_rows=10, grid_cols=10, n_features=2,
                 lr_inicial=0.5, sigma_inicial=None, n_iter=500, seed=42):
        """
        Parâmetros:
        - grid_rows/cols: dimensões da grade de neurônios
        - n_features: dimensionalidade dos dados de entrada
        - lr_inicial: taxa de aprendizado inicial (decai exponencialmente)
        - sigma_inicial: raio de vizinhança inicial (decai exponencialmente)
        - n_iter: número de iterações de treino
        """
        self.rows = grid_rows
        self.cols = grid_cols
        self.n_features = n_features
        self.lr0 = lr_inicial
        self.sigma0 = sigma_inicial if sigma_inicial else max(grid_rows, grid_cols) / 2.0
        self.n_iter = n_iter
        self.seed = seed
        
        # Coordenadas fixas de cada neurônio na grade (para calcular vizinhança)
        r, c = np.meshgrid(np.arange(grid_rows), np.arange(grid_cols), indexing='ij')
        self.coords = np.stack([r.ravel(), c.ravel()], axis=1).astype(float)
        
        # Pesos: cada neurônio tem um vetor de mesmo tamanho que a entrada
        rng = np.random.RandomState(seed)
        self.W = rng.rand(grid_rows * grid_cols, n_features)
    
    def _encontrar_bmu(self, x):
        """
        BMU = neurônio cujo vetor de pesos está mais próximo de x.
        Distância euclidiana ao quadrado (sem raiz, mais rápido).
        """
        distancias = np.sum((self.W - x) ** 2, axis=1)
        return np.argmin(distancias)
    
    def treinar(self, X):
        """
        Loop principal de treinamento.
        Para cada amostra:
        1. Encontra o BMU.
        2. Calcula decaimento da taxa de aprendizado e do raio.
        3. Atualiza pesos do BMU e vizinhos com peso gaussiano.
        """
        rng = np.random.RandomState(self.seed)
        n_amostras = X.shape[0]
        
        # Constante de tempo para decaimento do raio
        tau = self.n_iter / np.log(self.sigma0) if self.sigma0 > 1 else 1
        
        for t in range(self.n_iter):
            # Escolhe uma amostra aleatória (aprendizado online)
            x = X[rng.randint(n_amostras)]
            
            # Decaimento exponencial de lr e sigma
            lr = self.lr0 * np.exp(-t / self.n_iter)
            sigma = self.sigma0 * np.exp(-t / tau)
            
            # Passo 1: competição — encontra o vencedor
            bmu_idx = self._encontrar_bmu(x)
            
            # Passo 2: cooperação — vizinhança gaussiana na grade
            # Distância de cada neurônio ao BMU (nas coordenadas da grade)
            dist_grid = np.sum((self.coords - self.coords[bmu_idx]) ** 2, axis=1)
            h = np.exp(-dist_grid / (2 * sigma ** 2))  # ativação de vizinhança
            
            # Passo 3: adaptação — move pesos em direção a x
            # h[:, None] transforma (n_neurônios,) em (n_neurônios, 1) para broadcast
            self.W += lr * h[:, None] * (x - self.W)
    
    def mapear(self, X):
        """Retorna o índice do BMU para cada amostra."""
        return np.array([self._encontrar_bmu(x) for x in X])

def demo():
    """Demonstração: SOM em dados 2D para visualizar organização topológica."""
    from utils import gerar_dados_classificacao
    
    X, y = gerar_dados_classificacao(n=400, seed=7)
    # Normaliza para [0,1] (SOM é sensível à escala)
    X_norm = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    
    som = SOM(grid_rows=10, grid_cols=10, n_features=2, n_iter=800, seed=7)
    som.treinar(X_norm)
    
    # Visualização: posição final dos pesos no espaço de entrada
    plt.figure(figsize=(8, 6))
    plt.scatter(X_norm[y==1, 0], X_norm[y==1, 1], c='blue', alpha=0.3, label='Classe +1')
    plt.scatter(X_norm[y==-1, 0], X_norm[y==-1, 1], c='red', alpha=0.3, label='Classe -1')
    # Desenha os neurônios como pontos pretos
    plt.scatter(som.W[:, 0], som.W[:, 1], c='black', s=40, marker='s', label='Neurônios')
    # Conecta vizinhos na grade para mostrar topologia
    for i in range(som.rows):
        for j in range(som.cols):
            idx = i * som.cols + j
            if j < som.cols - 1:
                viz = i * som.cols + (j + 1)
                plt.plot([som.W[idx,0], som.W[viz,0]], [som.W[idx,1], som.W[viz,1]], 'k-', alpha=0.2)
            if i < som.rows - 1:
                viz = (i + 1) * som.cols + j
                plt.plot([som.W[idx,0], som.W[viz,0]], [som.W[idx,1], som.W[viz,1]], 'k-', alpha=0.2)
    plt.title('SOM: grade de neurônios organizada sobre os dados')
    plt.legend(); plt.grid(True); plt.show()

if __name__ == "__main__":
    demo()