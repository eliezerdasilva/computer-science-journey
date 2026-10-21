"""
Adaline (ADAptive LINear Element) + Regra LMS (Least Mean Squares).
Referência: Hagan, Neural Network Design, capítulo sobre Adaline.

Diferença crucial do Perceptron:
- Perceptron utiliza a saída discreta (após sign) para corrigir os pesos.
- Adaline utiliza a saída contínua (w·x + b) antes do sign.
- O erro é calculado por: erro = y_real - saída_contínua.

A regra LMS (Widrow-Hoff) ajusta os pesos por gradiente descendente,
buscando minimizar o erro quadrático médio (MSE).
"""

# Bibliotecas para operações matemáticas e manipulação de caminhos.
import numpy as np
import sys, os

# Adiciona o diretório pai ao caminho de busca para importar o módulo utils.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Funções auxiliares para gerar os dados e visualizar a fronteira de decisão.
from utils import gerar_dados_classificacao, plot_hiperplano

class Adaline:
    def __init__(self, lr=0.01, n_epocas=100, tol=1e-4, seed=42):
        # Hiperparâmetros do treinamento.
        self.lr = lr                  # Taxa de aprendizado: controla o tamanho das atualizações.
        self.n_epocas = n_epocas      # Número máximo de passagens pelos dados.
        self.tol = tol                # Variação mínima do MSE para o critério de parada.
        self.seed = seed              # Semente para reproduzir os resultados.

        # Parâmetros que serão ajustados durante o treinamento.
        self.w = None                 # Vetor de pesos, um para cada característica.
        self.b = None                 # Viés, que desloca a fronteira de decisão.
        self.historico_erro = []      # Armazena o MSE de cada época.

    def _saida_continua(self, X):
        """Calcula a saída linear do modelo: u = w·x + b."""
        # O operador @ realiza o produto entre a matriz de entradas e os pesos.
        # O viés é somado à saída de cada amostra.
        return X @ self.w + self.b

    def _predicao(self, X):
        """Converte a saída contínua em classes discretas."""
        # A função sinal retorna +1 para valores positivos e -1 para negativos.
        # Se a saída for exatamente zero, np.sign retorna zero.
        return np.sign(self._saida_continua(X))

    def treinar(self, X, y):
        """
        Treina o modelo utilizando a regra LMS online.
        Os pesos são atualizados após o processamento de cada amostra.
        """
        # Cria um gerador aleatório reproduzível.
        rng = np.random.RandomState(self.seed)

        # Obtém o número de amostras (n) e de características (d).
        n, d = X.shape

        # Inicializa os pesos com valores aleatórios pequenos e o viés com zero.
        self.w = rng.normal(0, 0.1, d)
        self.b = 0.0
        self.historico_erro = []

        # Cada época corresponde a uma passagem por todas as amostras.
        for epoca in range(self.n_epocas):
            indices = rng.permutation(n)  # Embaralha as amostras a cada época.
            erro_total = 0.0               # Acumula os erros quadráticos da época.

            for i in indices:
                xi = X[i]  # Características da amostra atual.
                yi = y[i]  # Classe desejada da amostra atual.

                # Calcula a saída contínua e o erro em relação ao valor desejado.
                u = xi @ self.w + self.b
                erro = yi - u

                # Regra LMS: ajusta os pesos e o viés na direção de redução do erro.
                # A atualização utiliza a saída contínua, sem aplicar np.sign().
                self.w += self.lr * erro * xi
                self.b += self.lr * erro

                # Soma o erro ao quadrado para calcular o MSE ao final da época.
                erro_total += erro ** 2

            # MSE = soma dos erros quadráticos dividida pelo número de amostras.
            mse = erro_total / n
            self.historico_erro.append(mse)

            # Interrompe o treinamento se a variação do MSE entre épocas
            # consecutivas for menor que a tolerância definida.
            if epoca > 5 and abs(self.historico_erro[-2] - mse) < self.tol:
                print(f"Convergiu (estável) na época {epoca + 1}, MSE={mse:.6f}")
                break

        # Retorna o modelo treinado.
        return self

def demo():
    # Gera 200 amostras para o problema de classificação.
    X, y = gerar_dados_classificacao(n=200, seed=5)

    # Cria o modelo e define seus parâmetros de treinamento.
    ada = Adaline(lr=0.01, n_epocas=200, seed=5)

    # Ajusta os pesos e o viés utilizando os dados gerados.
    ada.treinar(X, y)

    # Calcula a acurácia nos próprios dados de treinamento.
    # A média dos valores booleanos representa a proporção de acertos.
    acuracia = np.mean(ada._predicao(X) == y)
    print(f"Acurácia no treino: {acuracia:.2%}")

    # Plota o histórico do MSE para acompanhar a evolução do erro.
    import matplotlib.pyplot as plt

    plt.figure(figsize=(7, 4))
    plt.plot(ada.historico_erro, 'b-', linewidth=2)
    plt.xlabel('Época')
    plt.ylabel('MSE')
    plt.title('Adaline/LMS: convergência do erro quadrático médio')
    plt.grid(True)
    plt.show()

    # Exibe os dados e a fronteira de decisão aprendida.
    # Em duas dimensões, essa fronteira é uma reta definida por:
    # w1*x1 + w2*x2 + b = 0.
    plot_hiperplano(X, y, ada.w, ada.b, "Adaline: fronteira aprendida")

# Executa a demonstração somente quando o arquivo é executado diretamente,
# evitando que ela seja iniciada automaticamente ao importar este módulo.
if __name__ == "__main__":
    demo()
