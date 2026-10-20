
# Self-Organizing Map (SOM) - Explicação

## 1. A Ideia Central

O objetivo do **Mapa Auto-Organizável de Kohonen (SOM)** é organizar dados semelhantes em regiões próximas de uma grade de neurônios. Cada neurônio possui um vetor de pesos que representa uma região do espaço de entrada.

O SOM utiliza **aprendizado não supervisionado**, ou seja, não precisa das classes corretas para aprender a organização dos dados. Durante o treinamento, os neurônios competem para identificar aquele cujo vetor de pesos é mais próximo da amostra. O vencedor e seus vizinhos são ajustados em direção a essa amostra.

Isso permite preservar a **topologia dos dados**, fazendo com que amostras semelhantes tendam a ativar neurônios próximos na grade.

* **Objetivo:** encontrar o neurônio vencedor (BMU) e atualizar seus pesos e os pesos dos vizinhos em direção à amostra de entrada.

---

Significados:

| Nesse Código | Significado |
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
| `BMU` | Best Matching Unit: neurônio cujo vetor de pesos está mais próximo da amostra apresentada. |
| `distancias` | Distâncias euclidianas ao quadrado entre a amostra e os vetores de pesos dos neurônios. |
| `mapear(X)` | Retorna o índice do neurônio vencedor para cada amostra. |

---

## 2. O Passo a Passo do Código

A inicialização cria os pesos dos neurônios aleatoriamente:

    rng = np.random.RandomState(seed)
    self.W = rng.rand(grid_rows * grid_cols, n_features)

Cada neurônio recebe um vetor de pesos com a mesma quantidade de características da amostra de entrada.

### Passo 1: Encontrar o neurônio vencedor

O método `_encontrar_bmu(x)` calcula a distância entre a amostra e todos os neurônios.

    distancias = np.sum((self.W - x) ** 2, axis=1)
    return np.argmin(distancias)

A fórmula utilizada é:

\[
d_i^2 = \sum_{j=1}^{n}(w_{ij}-x_j)^2
\]

Onde:

* \(d_i^2\) é a distância ao quadrado entre a amostra e o neurônio.
* \(w_{ij}\) é o peso do neurônio \(i\) na característica \(j\).
* \(x_j\) é o valor da característica \(j\) da amostra.

O neurônio vencedor é aquele que apresenta a menor distância:

\[
BMU = \arg\min_i d_i^2
\]

A raiz quadrada não é necessária porque ela não altera qual neurônio possui a menor distância.

### Passo 2: Calcular a vizinhança

Depois de encontrar o vencedor, o SOM calcula a distância entre ele e os demais neurônios na grade.

    dist_grid = np.sum(
        (self.coords - self.coords[bmu_idx]) ** 2,
        axis=1
    )

Essa distância é diferente da distância entre os pesos e a amostra. Aqui, são utilizadas as coordenadas dos neurônios na grade.

### Passo 3: Calcular a influência

O código utiliza uma função gaussiana para determinar a influência do vencedor sobre os outros neurônios.

    h = np.exp(-dist_grid / (2 * sigma ** 2))

A fórmula é:

\[
h_i = \exp\left(-\frac{d_i^2}{2\sigma^2}\right)
\]

Onde:

* \(h_i\) é a influência da vizinhança sobre o neurônio \(i\).
* \(d_i^2\) é a distância ao quadrado entre o neurônio e o vencedor na grade.
* \(\sigma\) é o raio da vizinhança.

Quanto mais próximo o neurônio estiver do vencedor, maior será sua influência. O vencedor possui distância zero e, portanto, influência igual a 1.

### Passo 4: Atualizar os pesos

A regra de atualização é:

\[
w_i^{novo}=w_i^{antigo}+\eta h_i(x-w_i^{antigo})
\]

Onde:

* \(w_i\) é o vetor de pesos do neurônio.
* \(x\) é a amostra de entrada.
* \(\eta\) é a taxa de aprendizado.
* \(h_i\) é a influência da vizinhança.

No código:

    self.W += lr * h[:, None] * (x - self.W)

O trecho `h[:, None]` transforma o vetor de influências em uma matriz coluna, permitindo que o NumPy aplique a influência de cada neurônio às suas características.

O resultado é que os pesos do vencedor e dos vizinhos se aproximam da amostra apresentada.

---

## 3. Como os Dados são Gerados

A função `gerar_dados_classificacao` cria duas classes de dados sintéticos, cada uma concentrada em uma região diferente do espaço.

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

* **A Semente (`seed`):** garante que os dados aleatórios sejam reproduzíveis.
* **Os Dados de Entrada (`X`):** cada amostra possui duas características numéricas.
* **A Classe Negativa (`X_neg`):** os pontos são gerados com distribuição normal centrada em `(-1.5, -1.5)`, com desvio padrão `0.5`.
* **A Classe Positiva (`X_pos`):** os pontos são gerados com distribuição normal centrada em `(1.5, 1.5)`, também com desvio padrão `0.5`.
* **Os Rótulos (`y`):** identificam as classes com os valores `-1` e `+1`. São utilizados na visualização, mas não participam do treinamento do SOM.
* **A Normalização (`X_norm`):** transforma cada característica para o intervalo `[0, 1]`, evitando que diferenças de escala dominem o cálculo das distâncias.

A normalização é importante porque o SOM utiliza distâncias entre vetores para determinar o neurônio vencedor.

A normalização é realizada por:

\[
X_{norm}=\frac{X-X_{min}}{X_{max}-X_{min}}
\]

No código:

    X_norm = (X - X.min(axis=0)) / (
        X.max(axis=0) - X.min(axis=0)
    )

O parâmetro `axis=0` indica que o mínimo e o máximo são calculados separadamente para cada característica.

---

## 4. Como Funciona o Treinamento

O método `treinar(X)` executa o processo de aprendizagem do SOM.

### Escolha de uma amostra

Em cada iteração, uma amostra é escolhida aleatoriamente:

    x = X[rng.randint(n_amostras)]

Isso caracteriza um aprendizado online, pois os pesos são atualizados a cada amostra apresentada.

### Decaimento da taxa de aprendizado

A taxa de aprendizado diminui exponencialmente:

\[
lr(t)=lr_0\exp\left(-\frac{t}{n_{iter}}\right)
\]

Onde:

* \(lr(t)\) é a taxa de aprendizado atual.
* \(lr_0\) é a taxa de aprendizado inicial.
* \(t\) é a iteração atual.
* \(n_{iter}\) é o número total de iterações.

No código:

    lr = self.lr0 * np.exp(-t / self.n_iter)

No início, os pesos podem mudar bastante. Com o passar das iterações, as atualizações ficam menores.

### Decaimento do raio da vizinhança

O raio da vizinhança também diminui exponencialmente:

\[
\sigma(t)=\sigma_0\exp\left(-\frac{t}{\tau}\right)
\]

Onde:

* \(\sigma(t)\) é o raio atual da vizinhança.
* \(\sigma_0\) é o raio inicial.
* \(t\) é a iteração atual.
* \(\tau\) controla a velocidade do decaimento.

No código:

    sigma = self.sigma0 * np.exp(-t / tau)

A constante de tempo é calculada por:

    tau = self.n_iter / np.log(self.sigma0) if self.sigma0 > 1 else 1

No começo, uma região maior da grade é influenciada pelo vencedor. Mais tarde, a influência fica concentrada nos neurônios próximos.

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

* **Os Pontos Azuis:** representam as amostras da classe `+1`.
* **Os Pontos Vermelhos:** representam as amostras da classe `-1`.
* **Os Pontos Pretos:** representam os vetores de pesos dos neurônios após o treinamento.
* **As Linhas Pretas:** conectam neurônios vizinhos na grade, mostrando a organização topológica aprendida.

A grade contém:

\[
10\times10=100\text{ neurônios}
\]

Cada neurônio possui dois pesos porque os dados de entrada possuem duas características.

Os pesos dos neurônios são exibidos com:

    plt.scatter(
        som.W[:, 0],
        som.W[:, 1],
        c='black',
        s=40,
        marker='s',
        label='Neurônios'
    )

As conexões entre os neurônios são desenhadas horizontalmente e verticalmente. Elas permitem visualizar como a grade se adapta à distribuição dos dados.

---

## 6. A Função `mapear(X)`

Depois do treinamento, o SOM pode identificar qual neurônio representa melhor cada amostra.

    def mapear(self, X):
        """Retorna o índice do BMU para cada amostra."""
        return np.array([
            self._encontrar_bmu(x) for x in X
        ])

A função percorre todas as amostras e encontra o neurônio vencedor de cada uma.

O resultado é um array contendo os índices dos neurônios vencedores.

Por exemplo, se três amostras forem mapeadas para os neurônios `12`, `12` e `35`, as duas primeiras possuem o mesmo neurônio vencedor, enquanto a terceira é representada por outro neurônio.

Para obter as coordenadas dos neurônios vencedores:

    indices = som.mapear(X_norm)
    coordenadas = som.coords[indices]

**Importante:** o índice retornado por `mapear(X)` corresponde à posição do neurônio na matriz `W`. As coordenadas da grade são obtidas por meio de `som.coords`.

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


