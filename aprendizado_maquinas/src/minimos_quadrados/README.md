# Mínimos Quadrados - Explicação

## 1. A Ideia Central
O objetivo do método dos Mínimos Quadrados é encontrar os coeficientes (pesos) de uma equação que façam a reta (ou hiperplano) passar o mais perto possível de todos os pontos observados.

Isso é feito minimizando a **soma dos erros quadráticos** (a diferença entre o valor previsto e o valor real, elevada ao quadrado).

*   **Fórmula Matemática (Equação Normal):** X^T X w = X^T y

---

Significados:

| Nesse Código | Significado |
| :--- | :--- |
| `X_aug` | Matriz de dados (Design Matrix). Tem uma coluna de `1s` (para o bias) e colunas com as features. |
| `@` (ou `np.dot`) | Produto interno (multiplicação de matrizes). |
| `A = X_aug.T @ X_aug` | Matriz de correlação das features (tamanho 2x2). |
| `b = X_aug.T @ y` | Vetor de correlação com o alvo (tamanho 2x1). |
| `w` | O resultado final: `[bias, coeficiente_angular]`. |
| `w = np.linalg.solve(A, b)` | Resolve a Equação Normal para achar o vetor `w`. |

---

## 2. O Passo a Passo do Código

```python
# 1. Adiciona a coluna de 1s (Cria a matriz X)
X_aug = np.c_[np.ones(X.shape[0]), X] 

# 2. Monta a Matriz A (M = X^T * X) e o Vetor b (X^T * y)
A = X_aug.T @ X_aug  # Matriz de correlação
b = X_aug.T @ y      # Correlação com o alvo

# 3. Resolve a Equação Normal (X^T * X * w = X^T * y)
w = np.linalg.solve(A, b)
# w[0] = bias (intercepto)
# w[1] = coeficiente (inclinação)
```

---

## 3. Como os Dados são Gerados 

A função `gerar_dados_linear` cria um cenário onde sabemos exatamente qual é a resposta correta.

```python
rng = np.random.RandomState(seed)
X = rng.uniform(-3, 3, n)
y = 2 * X + 1 + rng.normal(0, ruido, n)
```

*   **A Semente (`seed`):** Garante que o "aleatório" seja sempre o mesmo. Se rodar o código 100 vezes, o gráfico será idêntico.
*   **Os Dados de Entrada (`X`):** Gerados com distribuição uniforme entre -3 e 3. Representam as variáveis independentes.
*   **A Verdade (O Sinal):** `2 * X + 1`. É a regra exata do mundo simulado. O algoritmo deve tentar descobrir que o coeficiente é `2` e o bias é `1`.
*   **O Caos (O Ruído):** `rng.normal(0, ruido, n)`. Simula o mundo real (erros de medição). A média `0` significa que os erros para cima e para baixo se cancelam. O `ruido` (desvio padrão) espalha os pontos ao redor da reta.

---

## 4. Fluxo Completo de Execução

1.  **Geração:** `gerar_dados_linear` cria os arrays X e y (sinal + ruído).
2.  **Preparação:** `X.reshape(-1, 1)` garante que X seja uma matriz 2D.
3.  **Augmentação:** `X_aug` adiciona a coluna de 1s (para o bias não sumir).
4.  **Cálculo:** O código monta `A` e `b` e resolve `w = solve(A, b)`.
5.  **Resultado:** Os coeficientes encontrados (ex: `bias≈1.0`, `coef≈2.0`) serão próximos da verdade, mas não exatos, devido ao ruído.
6.  **Visualização:** O `matplotlib` desenha os pontos em azul e a reta prevista em vermelho cortando a nuvem de pontos.

---
