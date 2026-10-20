# MLP + Backpropagation — Explicação

## 1. A Ideia Central



A implementação utiliza três etapas principais:

1. **Propagação direta (Forward Propagation):** calcula a saída da rede a partir dos dados de entrada.
2. **Cálculo do erro:** compara a saída produzida com o valor esperado.
3. **Retropropagação (Backpropagation):** calcula os gradientes do erro em relação aos pesos e vieses, permitindo atualizar os parâmetros.

O processo é repetido durante várias épocas para reduzir o erro da rede.

## 2. Estrutura da Rede Neural

A implementação possui uma camada de entrada, uma camada oculta e uma camada de saída.

<AsyncImage query="multilayer perceptron neural network architecture two input neurons one hidden layer four neurons one output neuron labeled input hidden output weights biases educational diagram" aspectRatio="5:4" width="100%" />

### Camada de entrada

Recebe as características dos dados. Neste exemplo, cada amostra possui duas características:

- `x0`: primeira característica.
- `x1`: segunda característica.

A entrada não realiza uma transformação de aprendizado por si só. Ela fornece os valores que serão processados pelos neurônios da camada oculta.

### Camada oculta

A camada oculta realiza combinações ponderadas das entradas e aplica a função de ativação `tanh`.

O número de neurônios é definido pelo parâmetro `n_oculta`.

No exemplo, a rede utiliza oito neurônios ocultos.

### Camada de saída

Recebe as ativações da camada oculta e produz uma saída linear.

A classificação final é obtida aplicando a função sinal à saída:

- Se a saída for positiva, a previsão será `+1`.
- Se a saída for negativa, a previsão será `-1`.

## 3. Parâmetros e Variáveis

A classe `MLP` utiliza os seguintes parâmetros:

| Parâmetro | Significado |
|---|---|
| `n_oculta` | Quantidade de neurônios na camada oculta. |
| `lr` | Taxa de aprendizado, que controla a intensidade das atualizações. |
| `n_epocas` | Número de épocas de treinamento. |
| `seed` | Semente para reproduzir a inicialização aleatória. |
| `W1` | Matriz de pesos entre a entrada e a camada oculta. |
| `b1` | Vetor de vieses da camada oculta. |
| `W2` | Matriz de pesos entre a camada oculta e a saída. |
| `b2` | Viés da camada de saída. |
| `historico_erro` | Lista que armazena o MSE de cada época. |

Para duas características de entrada e oito neurônios ocultos, as dimensões são:

- `W1`: `(2, 8)`.
- `b1`: `(8,)`.
- `W2`: `(8, 1)`.
- `b2`: `(1,)`.

Essas dimensões permitem conectar cada característica de entrada a todos os neurônios ocultos e cada neurônio oculto à saída.

## 4. Propagação Direta (Forward Propagation)

A propagação direta calcula a saída da rede utilizando os pesos e vieses atuais.

### 4.1. Entrada para a camada oculta

Primeiro, a rede calcula uma combinação linear entre as entradas e os pesos:

**Z1 = X @ W1 + b1**

Onde:

- `X`: matriz de amostras de entrada.
- `W1`: pesos entre a entrada e a camada oculta.
- `b1`: vieses da camada oculta.
- `Z1`: valores antes da ativação.

No código:

```python
Z1 = X @ self.W1 + self.b1
```

A operação `X @ W1` realiza a multiplicação matricial. O viés é somado ao resultado para cada neurônio oculto.

### 4.2. Função de ativação tanh

Depois da combinação linear, a rede aplica a função `tanh`:

**A1 = tanh(Z1)**

A função é definida por:

**tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))**

Seu resultado fica entre `-1` e `+1`.

No código:

```python
A1 = np.tanh(Z1)
```

A função de ativação introduz não linearidade na rede. Sem essa transformação não linear, a composição das camadas continuaria equivalente a uma única transformação linear.

### 4.3. Camada oculta para a saída

As ativações da camada oculta são combinadas linearmente:

**Z2 = A1 @ W2 + b2**

No código:

```python
Z2 = A1 @ self.W2 + self.b2
```

A variável `Z2` representa a saída contínua da rede.

Neste modelo, não há uma função de ativação adicional na saída. A função sinal é aplicada somente durante a classificação.

### 4.4. Método `_forward`

O método reúne as operações anteriores:

```python
def _forward(self, X):
    Z1 = X @ self.W1 + self.b1
    A1 = np.tanh(Z1)
    Z2 = A1 @ self.W2 + self.b2
    return Z1, A1, Z2
```

Ele retorna três valores:

- `Z1`: valores da camada oculta antes da ativação.
- `A1`: ativações da camada oculta.
- `Z2`: saída linear da rede.

Esses resultados são necessários tanto para calcular as previsões quanto para executar o Backpropagation.

## 5. Função de Erro (MSE)

O treinamento utiliza o erro quadrático médio (*Mean Squared Error*).

Primeiro, calcula-se a diferença entre os valores esperados e as saídas da rede:

**erro = y - Z2**

Depois, calcula-se a média dos erros elevados ao quadrado:

**MSE = soma dos erros quadráticos / quantidade de amostras**

De forma expandida:

**MSE = [(y1 - Z2_1)² + (y2 - Z2_2)² + ... + (yn - Z2_n)²] / n**

Onde:

- `y`: valores reais.
- `Z2`: saídas contínuas produzidas pela rede.
- `n`: quantidade de amostras.
- `MSE`: erro quadrático médio.

No código:

```python
erro = y_col - Z2
mse = np.mean(erro ** 2)
self.historico_erro.append(mse)
```

O MSE é armazenado em cada época para permitir acompanhar a evolução do treinamento.

**Importante:** a função de erro é calculada usando a saída contínua `Z2`, não a classe discreta obtida pela função sinal.

## 6. Backpropagation — Retropropagação do Erro

O **Backpropagation** calcula como cada peso e viés contribui para o erro da rede.

Ele utiliza a regra da cadeia para propagar os gradientes da saída em direção à camada oculta.

O algoritmo segue esta sequência:

1. Calcular o gradiente da saída.
2. Calcular os gradientes dos pesos e do viés da saída.
3. Propagar o gradiente para a camada oculta.
4. Aplicar a derivada da função `tanh`.
5. Calcular os gradientes dos pesos e vieses da camada oculta.
6. Atualizar todos os parâmetros utilizando gradiente descendente.

### 6.1. Gradiente da saída

A função de erro é o MSE:

**MSE = soma dos erros quadráticos / n**

Como o erro é definido como `y - Z2`, a derivada do MSE em relação à saída é:

**dZ2 = -2 × erro / n**

No código:

```python
dZ2 = -2.0 * erro / n
```

O sinal negativo aparece porque o erro foi definido como `y - Z2`, enquanto a derivada é calculada em relação à saída `Z2`.

O fator `1/n` considera a média dos erros entre todas as amostras.

### 6.2. Gradientes da camada de saída

A matriz de pesos `W2` conecta os neurônios ocultos à saída.

Seu gradiente é:

**dW2 = A1.T @ dZ2**

O gradiente do viés é:

**db2 = soma de dZ2 ao longo das amostras**

No código:

```python
dW2 = A1.T @ dZ2
db2 = np.sum(dZ2, axis=0)
```

A transposição de `A1` permite combinar as ativações de cada neurônio oculto com os gradientes correspondentes da saída.

Como o treinamento utiliza todas as amostras de uma vez em cada época, os gradientes são acumulados para o conjunto completo.

### 6.3. Propagação do gradiente para a camada oculta

A rede precisa calcular como as ativações ocultas contribuíram para o erro da saída.

O gradiente em relação às ativações é:

**dA1 = dZ2 @ W2.T**

No código:

```python
dA1 = dZ2 @ self.W2.T
```

Esse cálculo utiliza os pesos `W2` para propagar a influência do erro da saída até cada neurônio oculto.

Entretanto, `A1` é o resultado da função `tanh`. Por isso, ainda é necessário considerar a derivada dessa função.

### 6.4. Derivada da tanh

A derivada da função `tanh`, expressa em função de sua própria saída, é:

**tanh'(z) = 1 - tanh(z)²**

Como `A1 = tanh(Z1)`, podemos escrever:

**dZ1 = dA1 × (1 - A1²)**

No código:

```python
dZ1 = dA1 * (1 - A1 ** 2)
```

A multiplicação é realizada elemento a elemento.

Essa etapa é essencial porque o gradiente precisa considerar tanto a influência dos neurônios ocultos na saída quanto a derivada da função de ativação.

### 6.5. Gradientes da camada oculta

Depois de calcular `dZ1`, a rede calcula os gradientes dos pesos da primeira camada:

**dW1 = X.T @ dZ1**

O gradiente dos vieses é:

**db1 = soma de dZ1 ao longo das amostras**

No código:

```python
dW1 = X.T @ dZ1
db1 = np.sum(dZ1, axis=0)
```

Agora, o algoritmo conhece os gradientes necessários para atualizar os parâmetros das duas camadas.

## 7. Atualização dos Pesos

Após calcular todos os gradientes, o modelo aplica o gradiente descendente.

A regra geral é:

**parâmetro_novo = parâmetro_atual - taxa_aprendizado × gradiente**

No código:

```python
self.W1 -= self.lr * dW1
self.b1 -= self.lr * db1
self.W2 -= self.lr * dW2
self.b2 -= self.lr * db2
```

O sinal de subtração é utilizado porque o gradiente aponta na direção de maior crescimento da função de erro. Para minimizá-la, os parâmetros são atualizados na direção oposta.

A taxa de aprendizado (`lr`) controla o tamanho de cada atualização:

- Uma taxa muito pequena pode tornar o treinamento lento.
- Uma taxa muito grande pode provocar oscilações ou dificultar a convergência.
- Uma taxa adequada favorece a redução do erro durante o treinamento.

## 8. Inicialização dos Pesos

O código inicializa os pesos utilizando uma distribuição normal:

```python
self.W1 = rng.normal(0, np.sqrt(2.0/d), (d, self.n_oculta))
self.b1 = np.zeros(self.n_oculta)

self.W2 = rng.normal(0, np.sqrt(2.0/self.n_oculta),
                     (self.n_oculta, 1))
self.b2 = np.zeros(1)
```

Os vieses começam em zero e os pesos recebem valores aleatórios.

A inicialização utiliza escalas relacionadas à quantidade de conexões de entrada de cada camada.

O comentário do código identifica essa estratégia como inicialização Xavier. Entretanto, as escalas utilizadas são baseadas em `sqrt(2 / quantidade_de_entradas)`, fórmula associada à inicialização de He. A inicialização Xavier normal clássica utiliza um desvio padrão relacionado tanto à quantidade de entradas quanto à quantidade de saídas.

Essa distinção importa porque a inicialização pode influenciar a estabilidade dos gradientes e o comportamento inicial do treinamento.

## 9. Treinamento 

Em cada época:

1. A rede processa todas as amostras.
2. Calcula o MSE do conjunto.
3. Calcula os gradientes considerando todas as amostras.
4. Atualiza os parâmetros uma única vez.

O ciclo principal é:

```python
for epoca in range(self.n_epocas):
    Z1, A1, Z2 = self._forward(X)

    erro = y_col - Z2
    mse = np.mean(erro ** 2)
    self.historico_erro.append(mse)

    dZ2 = -2.0 * erro / n
    dW2 = A1.T @ dZ2
    db2 = np.sum(dZ2, axis=0)

    dA1 = dZ2 @ self.W2.T
    dZ1 = dA1 * (1 - A1 ** 2)

    dW1 = X.T @ dZ1
    db1 = np.sum(dZ1, axis=0)

    self.W1 -= self.lr * dW1
    self.b1 -= self.lr * db1
    self.W2 -= self.lr * dW2
    self.b2 -= self.lr * db2
```

Os pesos permanecem fixos durante a propagação direta e o cálculo dos gradientes de uma época. A atualização ocorre somente depois que todos os gradientes foram calculados.

## 10. Classificação das Amostras

O método `_predicao` executa a propagação direta e aplica a função sinal:

```python
def _predicao(self, X):
    _, _, Z2 = self._forward(X)
    return np.sign(Z2).ravel()
```

A expressão `np.sign(Z2)` converte a saída contínua em valores discretos.

O método `ravel()` transforma o resultado em um vetor unidimensional, facilitando a comparação com os rótulos reais.

A regra de classificação é:

- `Z2 > 0`: classe `+1`.
- `Z2 < 0`: classe `-1`.
- `Z2 = 0`: resultado `0`, que não pertence às duas classes esperadas.

## 11. Geração dos Dados: make_moons

O experimento utiliza a função `make_moons`, do scikit-learn:

```python
from sklearn.datasets import make_moons

X, y_bin = make_moons(
    n_samples=300,
    noise=0.15,
    random_state=42
)

y = 2 * y_bin - 1
```

Essa função gera duas classes organizadas em formato de luas entrelaçadas.

Os parâmetros são:

- `n_samples=300`: quantidade total de amostras.
- `noise=0.15`: intensidade do ruído adicionado aos pontos.
- `random_state=42`: semente para reproduzir os dados.

Originalmente, os rótulos são `0` e `1`. A expressão `2 * y_bin - 1` converte esses valores para `-1` e `+1`.

### Normalização dos dados

O código normaliza as características:

```python
X = (X - X.mean(axis=0)) / X.std(axis=0)
```

A operação subtrai a média de cada característica e divide pelo respectivo desvio padrão.

Assim, cada característica fica aproximadamente com média zero e desvio padrão um.

A normalização ajuda a evitar que diferenças de escala entre atributos prejudiquem o aprendizado.

## 12. Configuração do Experimento

A rede é criada e treinada com:

```python
mlp = MLP(
    n_oculta=8,
    lr=0.05,
    n_epocas=800,
    seed=42
)

mlp.treinar(X, y)
```

Os parâmetros utilizados são:

| Parâmetro | Valor | Significado |
|---|---:|---|
| `n_oculta` | 8 | Quantidade de neurônios ocultos. |
| `lr` | 0,05 | Taxa de aprendizado. |
| `n_epocas` | 800 | Número máximo de épocas. |
| `seed` | 42 | Semente da inicialização dos pesos. |

Depois do treinamento, a acurácia é calculada:

```python
acuracia = np.mean(mlp._predicao(X) == y)
print(f"MLP (1 oculta, 8 neurônios) — Acurácia: {acuracia:.2%}")
```

A acurácia corresponde à proporção de previsões corretas.


## 13. Visualização da Fronteira Não Linear

O experimento constrói uma grade de pontos para visualizar a região de decisão da rede.

```python
xx, yy = np.meshgrid(
    np.linspace(X[:,0].min()-0.5, X[:,0].max()+0.5, 200),
    np.linspace(X[:,1].min()-0.5, X[:,1].max()+0.5, 200)
)

grid = np.c_[xx.ravel(), yy.ravel()]
Z = mlp._predicao(grid).reshape(xx.shape)
```

A grade cobre a região ocupada pelas amostras. Cada ponto é enviado à rede para obter uma previsão.

As previsões são reorganizadas para formar uma matriz que pode ser desenhada com `contourf`.

```python
plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
plt.scatter(X[y==1, 0], X[y==1, 1],
            c='blue', edgecolors='k', label='+1')
plt.scatter(X[y==-1, 0], X[y==-1, 1],
            c='red', edgecolors='k', label='-1')

plt.title('MLP: fronteira de decisão não-linear (make_moons)')
plt.legend()
plt.grid(True)
plt.show()
```

O fundo colorido representa as regiões classificadas como positivas ou negativas. Os pontos representam as amostras reais.


## 14. Fluxo Completo do Algoritmo

1. Gerar as amostras com `make_moons`.
2. Converter os rótulos de `0` e `1` para `-1` e `+1`.
3. Normalizar as características.
4. Inicializar os pesos e vieses das duas camadas.
5. Executar a propagação direta.
6. Calcular o erro quadrático médio.
7. Calcular o gradiente da saída.
8. Propagar o gradiente para a camada oculta.
9. Aplicar a derivada da `tanh`.
10. Calcular os gradientes dos pesos e vieses da camada oculta.
11. Atualizar todos os parâmetros com gradiente descendente.
12. Repetir até atingir o número máximo de épocas.
13. Calcular a acurácia nos dados de treino.
14. Construir e visualizar a fronteira de decisão não linear.

## 15. Características Importantes

- **Rede multicamada:** possui uma camada oculta entre a entrada e a saída.
- **Ativação não linear:** utiliza `tanh` para aprender relações não lineares.
- **Backpropagation:** calcula os gradientes por meio da regra da cadeia.
- **Gradiente descendente:** atualiza os parâmetros na direção de redução do erro.
- **Treinamento em batch:** calcula os gradientes usando todas as amostras antes de atualizar os parâmetros.
- **MSE:** mede o erro quadrático entre a saída contínua e os rótulos.
- **Fronteira não linear:** consegue representar separações que uma única reta não consegue representar.
