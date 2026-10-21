"""
Mínimos Quadrados (Least Squares)
Referência: Hagan, Neural Network Design, capítulo sobre Linear Filters.

Ideia central: encontrar w que minimize ||Xw - y||².
Solução analítica: w = (XᵀX)⁻¹ Xᵀ y (equação normal).
Não há treinamento iterativo — os coeficientes são calculados diretamente.
"""

# Bibliotecas para cálculos numéricos, manipulação de caminhos e gráficos.
import numpy as np
import sys, os

# Adiciona o diretório pai ao caminho de busca para importar o módulo utils.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a função que gera dados sintéticos para regressão linear.
from utils import gerar_dados_linear
import matplotlib.pyplot as plt


def minimos_quadrados_normal(X, y):
    """
    Calcula os coeficientes da regressão linear pela equação normal.

    X: matriz com as características das amostras.
    y: vetor com os valores desejados.

    Retorna um vetor em que w[0] é o viés e w[1:] são os coeficientes.
    """

    # Adiciona uma coluna de 1s para incluir o viés no cálculo.
    # Assim, o modelo pode ser escrito como uma única multiplicação matricial.
    X_aug = np.c_[np.ones(X.shape[0]), X]

    # Calcula os componentes da equação normal:
    # A representa XᵀX e b representa Xᵀy.
    A = X_aug.T @ X_aug
    b = X_aug.T @ y

    # Resolve o sistema linear A·w = b.
    # solve() evita calcular explicitamente a inversa da matriz A.
    w = np.linalg.solve(A, b)

    # Retorna os coeficientes: viés na primeira posição e pesos nas demais.
    return w


def demo():
    """Demonstra o ajuste de uma reta utilizando mínimos quadrados."""

    # Gera 80 amostras com ruído para simular dados de regressão linear.
    X, y = gerar_dados_linear(n=80, ruido=1.2)

    # Converte X para uma matriz bidimensional com formato (n_amostras, 1).
    X_2d = X.reshape(-1, 1)

    # Calcula diretamente os coeficientes que minimizam a soma dos erros
    # quadráticos entre os valores observados e os valores previstos.
    w = minimos_quadrados_normal(X_2d, y)

    # Exibe os coeficientes estimados e os valores utilizados na geração dos dados.
    print("=== Mínimos Quadrados ===")
    print(f"Coeficientes encontrados: bias={w[0]:.4f}, coef={w[1]:.4f}")
    print("Valor esperado (dados gerados): bias=1.0, coef=2.0")

    # Cria o gráfico e exibe os dados observados como pontos.
    plt.figure(figsize=(7, 5))
    plt.scatter(X, y, alpha=0.6, label='Dados observados')

    # Gera valores de x para desenhar a reta ajustada.
    x_line = np.linspace(X.min(), X.max(), 100)

    # Calcula as previsões utilizando a equação da reta: y = bias + coef*x.
    y_line = w[0] + w[1] * x_line

    # Desenha a reta estimada e configura os elementos do gráfico.
    plt.plot(x_line, y_line, 'r-', linewidth=2, label='Ajuste LS')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Mínimos Quadrados: ajuste de reta')
    plt.legend()
    plt.grid(True)
    plt.show()


# Executa a demonstração somente quando o arquivo é executado diretamente.
if __name__ == "__main__":
    demo()
