# Relatório: Implementação de Algoritmos Fundamentais de Aprendizado de Máquina

## 1. Objetivo
Implementar e compreender o princípio de funcionamento de cinco tópicos:
Mínimos Quadrados, Self-Organizing Map, Perceptron, Adaline/LMS e MLP.
Todas as implementações foram feitas em Python puro + NumPy, com
validação contra scikit-learn quando aplicável.

## 2. Metodologia
Cada algoritmo foi implementado do zero, com comentários explicando
cada passo. Os dados de demonstração são sintéticos e gerados
com sementes fixas para reprodutibilidade.

## 3. Resultados e Discussão

### 3.1 Mínimos Quadrados
Solução analítica direta. Converge em um passo. Serve como
"gabarito" para os métodos iterativos. A limitação é que só
funciona para modelos lineares nos parâmetros.

### 3.2 SOM
Aprendizado não supervisionado. Organiza topologicamente os dados.
A vizinhança gaussiana é o segredo: sem ela, seria só clustering
competitivo sem noção de ordem.

### 3.3 Perceptron
Primeiro classificador neural. Simples, mas limitado a fronteiras
lineares. A regra de aprendizado é "tudo ou nada" — não mede
o quão errado está.

### 3.4 Adaline/LMS
Evolução do Perceptron: usa erro contínuo e gradiente descendente.
A regra LMS minimiza o erro quadrático médio. É a ponte entre
o Perceptron e as redes modernas.

### 3.5 MLP
Com camada oculta + não-linearidade, resolve problemas não
separáveis linearmente. O backpropagation é a regra da cadeia
aplicada em rede. É a base de todo deep learning atual.

## 4. Comparação Geral

| Algoritmo | Supervisionado? | Fronteira | Convergência |
|-----------|----------------|-----------|--------------|
| Mínimos Quadrados | Sim | Linear | Direta (1 passo) |
| SOM | Não | — (clusterização) | Iterativa |
| Perceptron | Sim | Linear | Garantida se separável |
| Adaline/LMS | Sim | Linear | Aproximada (MSE) |
| MLP | Sim | Não-linear | Iterativa (backprop) |

## 5. Dificuldades e Aprendizados
- Entender por que o Perceptron falha em XOR.
- Visualizar a vizinhança no SOM.
- A regra da cadeia no backpropagation (o "vai e volta" dos gradientes).
- Importância da normalização dos dados.

## 6. Como Executar
```bash
bash setup.sh
source venv/bin/activate
python src/minimos_quadrados.py
python src/som.py
# etc.