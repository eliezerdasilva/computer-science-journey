"""
Multi Layer Perceptron (MLP) — rede com camada oculta e backpropagation.
Referência: Hagan, Neural Network Design, capítulo sobre Backpropagation.

Ideia central: sem camada oculta, só conseguimos fronteiras lineares.
Com uma camada oculta e ativação não linear (sigmoide/tanh), podemos
aproximar uma ampla classe de funções, conforme o teorema da aproximação universal.

Backpropagation utiliza a regra da cadeia para calcular os gradientes
do erro em relação aos pesos da rede, da saída para as camadas anteriores.

Implementação: uma camada oculta com ativação tanh e saída linear.
Na classificação binária com rótulos -1 e +1, usamos sign na predição.
"""

# Bibliotecas para operações numéricas e manipulação de caminhos.
import numpy as np
import sys, os

# Adiciona o diretório pai ao caminho de busca para importar o módulo utils.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Funções auxiliares para gerar dados de classificação e visualizar fronteiras.
from utils import gerar_dados_classificacao, plot_hiperplano


class MLP:
    def __init__(self, n_oculta=5, lr=0.01, n_epocas=500, seed=42):
        # Hiperparâmetros do modelo.
        self.n_oculta = n_oculta      # Número de neurônios na camada oculta.
        self.lr = lr                  # Taxa de aprendizado.
        self.n_epocas = n_epocas      # Número de épocas de treinamento.
        self.seed = seed              # Semente para reproduzir os resultados.

        # Parâmetros da rede, inicializados durante o treinamento.
        self.W1 = None  # Pesos da entrada para a camada oculta: (d, n_oculta).
        self.b1 = None  # Viés da camada oculta: (n_oculta,).
        self.W2 = None  # Pesos da camada oculta para a saída: (n_oculta, 1).
        self.b2 = None  # Viés da camada de saída: (1,).

        self.historico_erro = []  # Armazena o MSE de cada época.

    def _forward(self, X):
        """
        Propagação direta (forward propagation).
        Calcula a saída da rede a partir das entradas.
        """

        # Calcula a combinação linear das entradas na camada oculta.
        Z1 = X @ self.W1 + self.b1

        # Aplica tanh para introduzir não linearidade.
        A1 = np.tanh(Z1)

        # Calcula a saída linear a partir das ativações da camada oculta.
        Z2 = A1 @ self.W2 + self.b2

        # Retorna os valores intermediários necessários ao backpropagation.
        return Z1, A1, Z2

    def _predicao(self, X):
        """Converte a saída linear em classes -1 e +1."""

        # Aplica a função sinal à saída da rede.
        _, _, Z2 = self._forward(X)
        return np.sign(Z2).ravel()

    def treinar(self, X, y):
        """
        Treina a rede com backpropagation em lote (batch).

        Em cada época:
        1. Calcula as saídas da rede.
        2. Calcula o erro quadrático médio.
        3. Calcula os gradientes pela regra da cadeia.
        4. Atualiza todos os pesos e vieses.
        """

        # Inicializa o gerador aleatório e obtém as dimensões dos dados.
        rng = np.random.RandomState(self.seed)
        n, d = X.shape

        # Converte os rótulos para uma coluna, compatível com a saída da rede.
        y_col = y.reshape(-1, 1)

        # Inicialização dos pesos com valores aleatórios pequenos.
        # A escala considera o número de conexões de cada camada.
        self.W1 = rng.normal(0, np.sqrt(2.0/d), (d, self.n_oculta))
        self.b1 = np.zeros(self.n_oculta)
        self.W2 = rng.normal(0, np.sqrt(2.0/self.n_oculta), (self.n_oculta, 1))
        self.b2 = np.zeros(1)

        # Cada época utiliza todas as amostras antes de atualizar os parâmetros.
        self.historico_erro = []

        for epoca in range(self.n_epocas):

            # --- Forward: calcula a saída da rede ---
            Z1, A1, Z2 = self._forward(X)

            # --- Erro: diferença entre os valores desejados e previstos ---
            erro = y_col - Z2
            mse = np.mean(erro ** 2)
            self.historico_erro.append(mse)

            # --- Backward: calcula os gradientes pela regra da cadeia ---

            # Gradiente da função MSE em relação à saída linear Z2.
            dZ2 = -2.0 * erro / n

            # Gradientes dos pesos e do viés da camada de saída.
            dW2 = A1.T @ dZ2
            db2 = np.sum(dZ2, axis=0)

            # Propaga o gradiente para a camada oculta.
            dA1 = dZ2 @ self.W2.T

            # Derivada da tanh: 1 - tanh(Z1)².
            # Como A1 = tanh(Z1), podemos usar 1 - A1².
            dZ1 = dA1 * (1 - A1 ** 2)

            # Gradientes dos pesos e do viés da camada oculta.
            dW1 = X.T @ dZ1
            db1 = np.sum(dZ1, axis=0)

            # --- Atualização: gradiente descendente ---
            # Os parâmetros são ajustados na direção oposta ao gradiente.
            self.W1 -= self.lr * dW1
            self.b1 -= self.lr * db1
            self.W2 -= self.lr * dW2
            self.b2 -= self.lr * db2

        # Retorna a própria rede treinada.
        return self


def demo():
    # Gera dados não linearmente separáveis em formato de duas luas.
    from sklearn.datasets import make_moons
    X, y_bin = make_moons(n_samples=300, noise=0.15, random_state=42)

    # Converte os rótulos de {0, 1} para {-1, +1}.
    y = 2 * y_bin - 1

    # Padroniza as características para terem média zero e desvio-padrão um.
    # Isso ajuda a evitar diferenças excessivas de escala entre as entradas.
    X = (X - X.mean(axis=0)) / X.std(axis=0)

    # Cria e treina uma MLP com oito neurônios na camada oculta.
    mlp = MLP(n_oculta=8, lr=0.05, n_epocas=800, seed=42)
    mlp.treinar(X, y)

    # Calcula a acurácia nos dados de treinamento.
    acuracia = np.mean(mlp._predicao(X) == y)
    print(f"MLP (1 oculta, 8 neurônios) — Acurácia: {acuracia:.2%}")

    # Cria uma grade de pontos para visualizar a fronteira de decisão.
    import matplotlib.pyplot as plt

    xx, yy = np.meshgrid(
        np.linspace(X[:, 0].min()-0.5, X[:, 0].max()+0.5, 200),
        np.linspace(X[:, 1].min()-0.5, X[:, 1].max()+0.5, 200)
    )

    # Combina as coordenadas da grade e classifica cada ponto.
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = mlp._predicao(grid).reshape(xx.shape)

    # Exibe as regiões classificadas e as amostras de cada classe.
    plt.figure(figsize=(7, 5))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
    plt.scatter(X[y == 1, 0], X[y == 1, 1],
                c='blue', edgecolors='k', label='+1')
    plt.scatter(X[y == -1, 0], X[y == -1, 1],
                c='red', edgecolors='k', label='-1')

    plt.title('MLP: fronteira de decisão não-linear (make_moons)')
    plt.legend()
    plt.grid(True)
    plt.show()


# Executa a demonstração somente quando o arquivo é executado diretamente.
if __name__ == "__main__":
    demo()
