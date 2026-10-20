# Adaline + Regra LMS — Explicação

## 1. A Ideia Central

O **Adaline (ADAptive LINear Element)** é um modelo de rede neural utilizado para classificação linear. Seu aprendizado utiliza a **regra LMS (Least Mean Squares)**, também conhecida como regra de Widrow-Hoff.

O objetivo é ajustar os pesos e o viés de uma função linear para minimizar o erro quadrático entre os valores reais e as saídas contínuas produzidas pelo modelo.

A função linear é:

**u = w · x + b**

Onde:

- `x`: vetor de características da amostra.
- `w`: vetor de pesos aprendidos.
- `b`: viés (*bias*).
- `u`: saída contínua do modelo.

A classificação final é obtida aplicando a função sinal:

**y_predito = sign(u)**

O Adaline calcula primeiro uma saída contínua e somente depois a transforma em uma classe.

## 2. A Função Linear

O método utiliza uma combinação linear das características de entrada:

**u = w₁x₁ + w₂x₂ + ... + wₙxₙ + b**

Onde:

- `n`: quantidade de características.
- `xᵢ`: valor da característica i.
- `wᵢ`: peso associado à característica i.
- `b`: viés.

No código, essa operação é implementada pelo método `_saida_continua`:

```python
def _saida_continua(self, X):
    return X @ self.w + self.b
```

O operador `@` realiza a multiplicação matricial. Para uma única amostra, equivale ao produto escalar entre os atributos e os pesos.

O método `_predicao` aplica a função sinal:

```python
def _predicao(self, X):
    return np.sign(self._saida_continua(X))
```

Assim, o modelo retorna classes representadas por `-1` e `+1`, de acordo com o sinal da saída.

## 3. A Regra LMS

A regra LMS ajusta os pesos e o viés para reduzir o erro entre a saída contínua e o valor esperado.

### 3.1. Cálculo do erro

Para cada amostra, o modelo calcula:

**erro = y - u**

Substituindo a função linear:

**erro = y - (w · x + b)**

Onde:

- `y`: valor real da amostra.
- `u`: saída contínua calculada pelo modelo.
- `erro`: diferença entre o valor esperado e a saída calculada.

Por exemplo, se o valor real for `y = 1` e a saída contínua for `u = 0,4`, então:

**erro = 1 - 0,4 = 0,6**

O erro indica a diferença entre a saída produzida e o valor desejado.

### 3.2. Atualização dos pesos

Os pesos são atualizados conforme:

**w_novo = w_atual + taxa_aprendizado × erro × x**

Onde a taxa de aprendizado corresponde ao parâmetro `lr`.

Para cada peso individual:

**wᵢ = wᵢ + lr × erro × xᵢ**

O viés é atualizado por:

**b = b + lr × erro**

No código:

```python
erro = yi - u

self.w += self.lr * erro * xi
self.b += self.lr * erro
```

Essas atualizações são realizadas após o cálculo de cada amostra, caracterizando o aprendizado online.

### 3.3. Relação com o gradiente descendente

O Adaline utiliza uma função de erro quadrático para ajustar seus parâmetros.

Para uma amostra, o erro quadrático é definido por:

**E = 0,5 × (y - u)²**

Como `u = w · x + b`, as derivadas da função de erro são:

- Derivada em relação aos pesos: `-erro × x`
- Derivada em relação ao viés: `-erro`

O gradiente descendente atualiza os parâmetros na direção oposta ao gradiente. Com isso, obtemos as atualizações da regra LMS:

**w = w + lr × erro × x**

**b = b + lr × erro**

O fator `0,5` na função de erro simplifica as derivadas, cancelando o fator `2` que apareceria ao derivar o erro quadrático sem esse fator.

## 4. Erro Quadrático Médio (MSE)

Durante o treinamento, o modelo registra o erro quadrático médio de cada época.

A fórmula é:

**MSE = soma dos erros quadráticos / quantidade de amostras**

Ou, em notação matemática textual:

**MSE = [(y₁ - u₁)² + (y₂ - u₂)² + ... + (yₙ - uₙ)²] / n**

Onde:

- `n`: quantidade de amostras.
- `yᵢ`: valor real da amostra i.
- `uᵢ`: saída contínua da amostra i.
- `MSE`: média dos erros quadráticos.

No código:

```python
erro_total += erro ** 2

mse = erro_total / n
self.historico_erro.append(mse)
```

O MSE permite acompanhar o comportamento do treinamento. Quando diminui, indica que as saídas contínuas estão, em média, mais próximas dos valores desejados nas amostras avaliadas.

**Importante:** o código calcula o MSE utilizando os erros observados durante as atualizações de cada amostra. Como os pesos mudam ao longo da época, esse valor não corresponde exatamente ao erro calculado com um único conjunto fixo de pesos ao final dela.

## 5. Estrutura da Classe `Adaline`

### 5.1. Inicialização

O construtor recebe os parâmetros:

```python
def __init__(self, lr=0.01, n_epocas=100, tol=1e-4, seed=42):
```

| Parâmetro | Significado |
|---|---|
| `lr` | Taxa de aprendizado. Controla a intensidade das atualizações. |
| `n_epocas` | Número máximo de épocas de treinamento. |
| `tol` | Tolerância para identificar uma melhora muito pequena no MSE. |
| `seed` | Semente para reproduzir a inicialização e a ordem das amostras. |
| `w` | Vetor de pesos, inicializado durante o treinamento. |
| `b` | Viés, inicializado durante o treinamento. |
| `historico_erro` | Lista que armazena o MSE de cada época. |

### 5.2. Inicialização dos pesos

O código utiliza uma distribuição normal para inicializar os pesos:

```python
rng = np.random.RandomState(self.seed)
self.w = rng.normal(0, 0.1, d)
self.b = 0.0
```

Os pesos começam próximos de zero, com desvio padrão de `0,1`, enquanto o viés começa em zero.

A semente permite reproduzir os mesmos valores iniciais e a mesma sequência de embaralhamento, desde que os demais dados e parâmetros sejam iguais.

### 5.3. Embaralhamento das amostras

A cada época, as amostras são processadas em uma ordem aleatória:

```python
indices = rng.permutation(n)
```

Isso evita que o treinamento dependa sempre da ordem original dos dados.

O modelo percorre os índices embaralhados e atualiza seus parâmetros a cada amostra.

### 5.4. Critério de parada

O treinamento pode terminar antes de atingir o número máximo de épocas:

```python
if epoca > 5 and abs(self.historico_erro[-2] - mse) < self.tol:
    print(f"Convergiu (estável) na época {epoca + 1}, MSE={mse:.6f}")
    break
```

O algoritmo compara os MSEs de duas épocas consecutivas. Se a diferença absoluta for menor que `tol`, considera que houve pouca mudança e interrompe o treinamento.

A condição `epoca > 5` evita que esse critério seja aplicado nas primeiras épocas.

Essa condição indica **estabilidade do MSE entre duas épocas**, mas não garante que o erro seja mínimo ou que a classificação esteja perfeita.

## 6. Geração dos Dados de Classificação

A função `gerar_dados_classificacao` cria um conjunto sintético com duas classes.

### Classe negativa

Os pontos da classe `-1` são gerados em torno do centro `(-1,5; -1,5)`:

```python
X_neg = rng.normal(-1.5, 0.5, (n//2, 2))
y_neg = -np.ones(n//2)
```

### Classe positiva

Os pontos da classe `+1` são gerados em torno do centro `(1,5; 1,5)`:

```python
X_pos = rng.normal(1.5, 0.5, (n//2, 2))
y_pos = np.ones(n//2)
```

A função utiliza uma distribuição normal com desvio padrão de `0,5` para gerar os atributos de cada classe.

Depois, combina os pontos e seus rótulos:

```python
X = np.vstack([X_neg, X_pos])
y = np.concatenate([y_neg, y_pos])
```

Com `n=200`, são geradas 100 amostras de cada classe.

Os dados são construídos para que as classes fiquem concentradas em regiões diferentes do plano, favorecendo a separação por uma fronteira linear.

## 7. Execução do Treinamento

A função `demo()` realiza o experimento:

```python
X, y = gerar_dados_classificacao(n=200, seed=5)

ada = Adaline(lr=0.01, n_epocas=200, seed=5)
ada.treinar(X, y)
```

O modelo recebe 200 amostras e utiliza:

- Taxa de aprendizado: `0,01`.
- Máximo de épocas: `200`.
- Semente: `5`.

Após o treinamento, a acurácia é calculada:

```python
acuracia = np.mean(ada._predicao(X) == y)
print(f"Acurácia no treino: {acuracia:.2%}")
```

A fórmula da acurácia é:

**Acurácia = número de previsões corretas / total de amostras**

O código compara as classes previstas com os rótulos reais e calcula a proporção de acertos.

Como essa avaliação utiliza os mesmos dados empregados no treinamento, ela mede a acurácia de treino, e não a capacidade de generalização para dados novos.

## 8. Visualização da Convergência

O histórico de erro é utilizado para visualizar a evolução do MSE:

```python
plt.plot(ada.historico_erro, 'b-', linewidth=2)
plt.xlabel('Época')
plt.ylabel('MSE')
plt.title('Adaline/LMS: convergência do erro quadrático médio')
plt.grid(True)
plt.show()
```

O gráfico apresenta:

- **Eixo X:** épocas de treinamento.
- **Eixo Y:** erro quadrático médio registrado em cada época.

Uma curva geralmente decrescente indica que o aprendizado está reduzindo o erro.

Oscilações podem ocorrer porque o modelo atualiza os pesos individualmente para cada amostra, em vez de calcular uma única atualização para todo o conjunto.

## 9. Visualização da Fronteira de Decisão

A função `plot_hiperplano` desenha os dados e a fronteira aprendida pelo modelo.

A fronteira é definida por:

**w₀x₀ + w₁x₁ + b = 0**

Isolando `x₁`:

**x₁ = -(w₀x₀ + b) / w₁**

No código:

```python
y_vals = -(w[0]*x_vals + b) / w[1]
plt.plot(x_vals, y_vals, 'k--', label='Fronteira')
```

Os pontos positivos são exibidos em azul e os negativos em vermelho. A reta tracejada representa os pontos em que a saída linear é zero.

- Se `u > 0`, a previsão é `+1`.
- Se `u < 0`, a previsão é `-1`.

Quando `u = 0`, `np.sign(0)` retorna zero, que não corresponde a nenhuma das duas classes esperadas. Além disso, a expressão da reta pressupõe que `w[1]` seja diferente de zero.

## 10. Fluxo Completo do Algoritmo

1. Gerar os dados de classificação.
2. Inicializar os pesos aleatoriamente e o viés em zero.
3. Embaralhar as amostras.
4. Para cada amostra:
   - Calcular a saída contínua: `u = w · x + b`.
   - Calcular o erro: `erro = y - u`.
   - Atualizar os pesos: `w = w + lr × erro × x`.
   - Atualizar o viés: `b = b + lr × erro`.
   - Acumular o erro quadrático.
5. Calcular e armazenar o MSE da época.
6. Verificar se o MSE ficou estável em relação à época anterior.
7. Repetir até a parada por estabilidade ou até atingir o limite de épocas.
8. Calcular a acurácia nos dados de treino.
9. Plotar o histórico de erro e a fronteira de decisão.

## 11. Características Importantes

- **Aprendizado supervisionado:** utiliza os rótulos reais para ajustar os parâmetros.
- **Modelo linear:** a fronteira de decisão é uma reta em duas dimensões ou um hiperplano em dimensões superiores.
- **Saída contínua:** o erro é calculado antes da aplicação da função sinal.
- **Regra LMS:** atualiza os pesos proporcionalmente ao erro contínuo.
- **Gradiente descendente online:** os parâmetros são atualizados após cada amostra.
- **MSE:** permite acompanhar o erro quadrático durante o treinamento.
- **Reprodutibilidade:** a semente controla a inicialização e o embaralhamento.
- **Limitação:** uma única fronteira linear não consegue separar perfeitamente todas as distribuições de dados.

