# Self-Organizing Map (SOM) — Explicação

## 1. A Ideia Central

O objetivo do **Mapa Auto-Organizável de Kohonen (SOM)** é organizar dados semelhantes em regiões próximas de uma grade de neurônios. Cada neurônio possui um vetor de pesos que representa uma região do espaço de entrada.

O SOM utiliza **aprendizado não supervisionado**, ou seja, não precisa das classes corretas para aprender a organização dos dados. Durante o treinamento, os neurônios competem para identificar aquele cujo vetor de pesos é mais próximo da amostra. O vencedor e seus vizinhos são ajustados em direção a essa amostra.

Isso permite preservar a **topologia dos dados**, fazendo com que amostras semelhantes tendam a ativar neurônios próximos na grade.

- **Objetivo:** encontrar o neurônio vencedor (BMU) e atualizar seus pesos e os pesos dos vizinhos em direção à amostra de entrada.

### Significados

| Nesse código | Significado |
| :--- | :--- |
| `SOM` | Classe que implementa o Mapa Auto-Organizável de Kohonen. |
| `grid_rows` e `grid_cols` | Quantidade de linhas e colunas da grade de neurônios. |
| `n_features` | Número de características de cada amostra de entrada. |
| `W` | Matriz de pesos dos neurônios. Cada linha representa um neurônio e cada coluna, uma característica. |
| `coords` | Coordenadas fixas dos neurônios na grade, utilizadas para calcular as distâncias entre eles. |
| `lr_inicial` | Taxa de aprendizado inicial, que controla a intensidade das atualizações dos pesos. |
| `sigma_inicial` | Raio inicial da vizinhança, que controla quantos neurônios são influenciados pelo vencedor. |
| `n_iter` | Número de iterações de treinamento. |
| `seed` | Semente que permite reproduzir a inicialização e a sequência de amostras aleatórias. |
| `BMU` | *Best Matching Unit*: neurônio cujo vetor de pesos está mais próximo da amostra apresentada. |
| `distancias` | Distâncias euclidianas ao quadrado entre a amostra e os vetores de pesos dos neurônios. |
| `mapear(X)` | Retorna o índice do neurônio vencedor para cada amostra. |

---

## 2. O Passo a Passo do Código

A inicialização cria os pesos dos neurônios aleatoriamente:

```python
rng = np.random.RandomState(seed)
self.W = rng.rand(grid_rows * grid_cols, n_features)
```

Cada neurônio recebe um vetor de pesos com a mesma quantidade de características da amostra de entrada.

### Passo 1: Encontrar o neurônio vencedor

O método `_encontrar_bmu(x)` calcula a distância entre a amostra e todos os neurônios.

```python
distancias = np.sum((self.W - x) ** 2, axis=1)
return np.argmin(distancias)
```

A distância ao quadrado entre a amostra e cada neurônio é calculada assim:

**dᵢ² = (wᵢ₁ − x₁)² + (wᵢ₂ − x₂)² + ... + (wᵢₙ − xₙ)²**

Onde:

- **dᵢ²:** distância ao quadrado entre a amostra e o neurônio i.
- **wᵢⱼ:** peso do neurônio i na característica j.
- **xⱼ:** valor da característica j da amostra.
- **n:** número de características da amostra.

O neurônio vencedor é aquele que apresenta a menor distância:

**BMU = índice do neurônio com a menor distância dᵢ²**

A raiz quadrada não é necessária porque ela não altera qual neurônio possui a menor distância.

### Passo 2: Calcular a vizinhança

Depois de encontrar o vencedor, o SOM calcula a distância entre ele e os demais neurônios na grade.

```python
dist_grid = np.sum(
    (self.coords - self.coords[bmu_idx]) ** 2,
    axis=1
)
```

Essa distância é diferente da distância entre os pesos e a amostra. Aqui, são utilizadas as coordenadas dos neurônios na grade.

Por exemplo, se o neurônio vencedor estiver na posição (2, 3) e outro neurônio estiver na posição (4, 3), a distância ao quadrado entre eles será:

**d² = (4 − 2)² + (3 − 3)² = 4**

Essa distância determina o quanto cada neurônio será influenciado pelo vencedor.

### Passo 3: Calcular a influência

O código utiliza uma função gaussiana para determinar a influência do vencedor sobre os outros neurônios.

```python
h = np.exp(-dist_grid / (2 * sigma ** 2))
```

A fórmula da influência é:

**hᵢ = exp(−dᵢ² / (2 × σ²))**

Onde:

- **hᵢ:** influência da vizinhança sobre o neurônio i.
- **dᵢ²:** distância ao quadrado entre o neurônio e o vencedor na grade.
- **σ:** raio da vizinhança.
- **exp:** função exponencial.

Quanto mais próximo o neurônio estiver do vencedor, maior será sua influência. O vencedor possui distância zero e, portanto, influência igual a 1.

Quando o raio da vizinhança diminui, a influência fica mais concentrada nos neurônios próximos do vencedor.

### Passo 4: Atualizar os pesos

A regra de atualização é:

**wᵢ(novo) = wᵢ(antigo) + η × hᵢ × (x − wᵢ(antigo))**

Onde:

- **wᵢ:** vetor de pesos do neurônio.
- **x:** amostra de entrada.
- **η:** taxa de aprendizado.
- **hᵢ:** influência da vizinhança.

No código:

```python
self.W += lr * h[:, None] * (x - self.W)
```

O trecho `h[:, None]` transforma o vetor de influências em uma matriz coluna, permitindo que o NumPy aplique a influência de cada neurônio às suas características.

O resultado é que os pesos do vencedor e dos vizinhos se aproximam da amostra apresentada. O vencedor recebe a maior atualização, enquanto os neurônios mais distantes recebem atualizações menores.

---

## 3. Como os Dados São Gerados

A função `gerar_dados_classificacao` cria duas classes de dados sintéticos, cada uma concentrada em uma região diferente do espaço.

```python
def gerar_dados_classificacao(n=200, seed=42):
    rng = np.random.RandomState(seed)

    # Classe -1: centrada em (-1.5, -1.5)
    X_neg = rng.normal(-1.5, 0.5, (n // 2, 2))
    y_neg = -np.ones(n // 2)

    # Classe +1: centrada em (1.5, 1.5)
    X_pos = rng.normal(1.5, 0.5, (n // 2, 2))
    y_pos = np.ones(n // 2)

    # Combina as duas classes
    X = np.vstack([X_neg, X_pos])
    y = np.concatenate([y_neg, y_pos])

    return X, y
```

- **A semente (`seed`):** garante que os dados aleatórios sejam reproduzíveis.
- **Os dados de entrada (`X`):** cada amostra possui duas características numéricas.
- **A classe negativa (`X_neg`):** os pontos são gerados com distribuição normal centrada em `(-1.5, -1.5)`, com desvio padrão `0.5`.
- **A classe positiva (`X_pos`):** os pontos são gerados com distribuição normal centrada em `(1.5, 1.5)`, também com desvio padrão `0.5`.
- **Os rótulos (`y`):** identificam as classes com os valores `-1` e `+1`. São utilizados na visualização, mas não participam do treinamento do SOM.
- **A normalização (`X_norm`):** transforma cada característica para o intervalo `[0, 1]`, evitando que diferenças de escala dominem o cálculo das distâncias.

A normalização é importante porque o SOM utiliza distâncias entre vetores para determinar o neurônio vencedor.

A fórmula da normalização Min-Max é:

**X_norm = (X − X_min) / (X_max − X_min)**

No código:

```python
X_norm = (X - X.min(axis=0)) / (
    X.max(axis=0) - X.min(axis=0)
)
```

O parâmetro `axis=0` indica que o mínimo e o máximo são calculados separadamente para cada característica.

Assim, cada característica é ajustada individualmente para o intervalo entre 0 e 1.

---

## 4. Como Funciona o Treinamento

O método `treinar(X)` executa o processo de aprendizagem do SOM.

### Escolha de uma amostra

Em cada iteração, uma amostra é escolhida aleatoriamente:

```python
x = X[rng.randint(n_amostras)]
```

Isso caracteriza um aprendizado online, pois os pesos são atualizados a cada amostra apresentada.

### Decaimento da taxa de aprendizado

A taxa de aprendizado diminui exponencialmente:

**lr(t) = lr₀ × exp(−t / n_iter)**

Onde:

- **lr(t):** taxa de aprendizado atual.
- **lr₀:** taxa de aprendizado inicial.
- **t:** iteração atual.
- **n_iter:** número total de iterações.

No código:

```python
lr = self.lr0 * np.exp(-t / self.n_iter)
```

No início, os pesos podem mudar bastante. Com o passar das iterações, as atualizações ficam menores.

Isso permite que o mapa se organize inicialmente de maneira mais ampla e, depois, passe por ajustes mais sutis.

### Decaimento do raio da vizinhança

O raio da vizinhança também diminui exponencialmente:

**σ(t) = σ₀ × exp(−t / τ)**

Onde:

- **σ(t):** raio atual da vizinhança.
- **σ₀:** raio inicial da vizinhança.
- **t:** iteração atual.
- **τ:** constante que controla a velocidade do decaimento.

No código:

```python
sigma = self.sigma0 * np.exp(-t / tau)
```

A constante de tempo é calculada por:

```python
tau = self.n_iter / np.log(self.sigma0) if self.sigma0 > 1 else 1
```

No começo, uma região maior da grade é influenciada pelo vencedor. Mais tarde, a influência fica concentrada nos neurônios próximos.

**Observação:** a expressão usada para calcular `tau` depende do valor inicial de `sigma0`. Quando `sigma0` é maior que 1, o código utiliza `n_iter / log(sigma0)`; caso contrário, utiliza 1.

### Resumo do treinamento

1. Seleciona uma amostra aleatória.
2. Encontra o neurônio vencedor.
3. Calcula a distância entre os neurônios na grade.
4. Calcula a influência gaussiana da vizinhança.
5. Atualiza os pesos de todos os neurônios.
6. Diminui a taxa de aprendizado e o raio da vizinhança.
7. Repete o processo até atingir o número de iterações definido.

---

## 5. O Passo a Passo da Visualização

A função `demo()` demonstra o funcionamento do SOM com 400 amostras e uma grade de `10 × 10` neurônios.

```python
X, y = gerar_dados_classificacao(n=400, seed=7)

X_norm = (X - X.min(axis=0)) / (
    X.max(axis=0) - X.min(axis=0)
)

som = SOM(
    grid_rows=10,
    grid_cols=10,
    n_features=2,
    n_iter=800,
    seed=7
)

som.treinar(X_norm)
```

Na visualização:

- **Os pontos azuis:** representam as amostras da classe `+1`.
- **Os pontos vermelhos:** representam as amostras da classe `-1`.
- **Os pontos pretos:** representam os vetores de pesos dos neurônios após o treinamento.
- **As linhas pretas:** conectam neurônios vizinhos na grade, mostrando a organização topológica aprendida.

A grade contém:

**10 × 10 = 100 neurônios**

Cada neurônio possui dois pesos porque os dados de entrada possuem duas características.

Os pesos dos neurônios são exibidos com:

```python
plt.scatter(
    som.W[:, 0],
    som.W[:, 1],
    c='black',
    s=40,
    marker='s',
    label='Neurônios'
)
```

As conexões entre os neurônios são desenhadas horizontalmente e verticalmente. Elas permitem visualizar como a grade se adapta à distribuição dos dados.

Como as amostras possuem duas características, cada vetor de pesos também possui duas componentes e pode ser representado no mesmo plano das amostras.

**Importante:** o SOM não utiliza os rótulos `y` para aprender as classes. As cores servem apenas para facilitar a interpretação visual da organização encontrada.

---

## 6. A Função `mapear(X)`

Depois do treinamento, o SOM pode identificar qual neurônio representa melhor cada amostra.

```python
def mapear(self, X):
    """Retorna o índice do BMU para cada amostra."""
    return np.array([
        self._encontrar_bmu(x) for x in X
    ])
```

A função percorre todas as amostras e encontra o neurônio vencedor de cada uma.

O resultado é um array contendo os índices dos neurônios vencedores.

Por exemplo, se três amostras forem mapeadas para os neurônios `12`, `12` e `35`, as duas primeiras possuem o mesmo neurônio vencedor, enquanto a terceira é representada por outro neurônio.

Para obter as coordenadas dos neurônios vencedores:

```python
indices = som.mapear(X_norm)
coordenadas = som.coords[indices]
```

**Importante:** o índice retornado por `mapear(X)` corresponde à posição do neurônio na matriz `W`. As coordenadas da grade são obtidas por meio de `som.coords`.

O índice identifica o neurônio na estrutura interna do SOM, enquanto as coordenadas indicam sua posição na grade.

---

## 7. Fluxo Completo de Execução

1. **Geração:** `gerar_dados_classificacao` cria as amostras das duas classes e seus rótulos.
2. **Normalização:** `X_norm` transforma as características para o intervalo `[0, 1]`.
3. **Inicialização:** `SOM(...)` cria a grade de neurônios e inicializa seus pesos aleatoriamente.
4. **Amostragem:** em cada iteração, o algoritmo seleciona uma amostra aleatória.
5. **Competição:** `_encontrar_bmu(x)` identifica o neurônio cujo vetor de pesos está mais próximo da amostra.
6. **Cooperação:** o algoritmo calcula a influência dos demais neurônios com base na distância até o vencedor na grade.
7. **Adaptação:** os pesos do vencedor e dos vizinhos são atualizados em direção à amostra.
8. **Decaimento:** a taxa de aprendizado e o raio da vizinhança diminuem ao longo das iterações.
9. **Mapeamento:** `mapear(X)` identifica o neurônio vencedor para cada amostra.
10. **Visualização:** o `matplotlib` exibe as amostras, os neurônios treinados e as conexões entre neurônios vizinhos.

---

## 8. Resumo das Fórmulas

| Etapa | Fórmula em texto simples | Finalidade |
| :--- | :--- | :--- |
| Distância até a amostra | `dᵢ² = Σⱼ (wᵢⱼ − xⱼ)²` | Medir a distância entre a amostra e cada neurônio. |
| Neurônio vencedor | `BMU = índice do menor dᵢ²` | Selecionar o neurônio mais próximo da amostra. |
| Influência da vizinhança | `hᵢ = exp(−dᵢ² / (2 × σ²))` | Determinar a intensidade da atualização de cada neurônio. |
| Atualização dos pesos | `wᵢ(novo) = wᵢ(antigo) + η × hᵢ × (x − wᵢ(antigo))` | Aproximar os pesos da amostra de entrada. |
| Normalização Min-Max | `X_norm = (X − X_min) / (X_max − X_min)` | Ajustar cada característica para o intervalo `[0, 1]`. |
| Taxa de aprendizado | `lr(t) = lr₀ × exp(−t / n_iter)` | Diminuir a intensidade das atualizações ao longo do treinamento. |
| Raio da vizinhança | `σ(t) = σ₀ × exp(−t / τ)` | Reduzir gradualmente a região de influência do vencedor. |

**Em síntese:** Em cada iteração, encontra o neurônio mais próximo da amostra, ajusta os pesos desse neurônio e dos seus vizinhos e reduz gradualmente a intensidade dessas atualizações. Ao final, dados semelhantes tendem a ser representados por regiões próximas da grade.
