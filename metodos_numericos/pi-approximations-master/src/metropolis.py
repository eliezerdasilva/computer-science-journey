import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# ============================================
# PASSO 1: Definir a função polinomial (grau 3)
# ============================================
def funcao_polinomial(x):
    """
    Função polinomial de grau 3 (cúbica).
    f(x) = -x^3 + 2x^2 + 5x + 10
    """
    return -x**3 + 2*x**2 + 5*x + 10

# ============================================
# PASSO 2: Definir a distribuição alvo (não normalizada)
# ============================================
def distribuicao_alvo(x):
    """
    Distribuição alvo baseada na função polinomial.
    Só é válida onde f(x) > 0.
    Usamos max(0, f(x)) para evitar valores negativos.
    """
    valor = funcao_polinomial(x)
    return max(0, valor)  # Probabilidade não pode ser negativa

# ============================================
# PASSO 3: Analisar a função (para referência)
# ============================================
print("=" * 60)
print("ANÁLISE DA FUNÇÃO POLINOMIAL")
print("=" * 60)

# Encontrar as raízes numericamente
x_vals = np.linspace(-3, 4, 1000)
y_vals = funcao_polinomial(x_vals)

# Encontrar onde a função é positiva
indices_positivos = y_vals > 0
x_positivos = x_vals[indices_positivos]

if len(x_positivos) > 0:
    x_min = x_vals[indices_positivos][0]
    x_max = x_vals[indices_positivos][-1]
    print(f"Domínio onde f(x) > 0: aproximadamente [{x_min:.2f}, {x_max:.2f}]")
else:
    print("A função é negativa em todo o domínio analisado.")
    x_min, x_max = -2, 4

# Calcular a integral (constante de normalização) - só para referência
integral, erro = quad(distribuicao_alvo, -10, 10)
print(f"Integral de f(x) no domínio: {integral:.4f}")
print(f"Isso seria a constante de normalização Z (mas não precisamos dela!)")

# ============================================
# PASSO 4: Definir parâmetros do algoritmo
# ============================================
num_iteracoes = 50000    # Número total de passos
burn_in = 5000           # Número de amostras iniciais a descartar
sigma_proposta = 0.3     # Tamanho do passo (ajustável)

# ============================================
# PASSO 5: Inicializar o algoritmo
# ============================================
# Escolher um ponto onde f(x) > 0
x_atual = 1.0  # Ponto inicial (dentro da região positiva)

# Listas para armazenar as amostras
amostras = []
valores_amostras = []  # Para guardar também os valores de f(x)

print("\n" + "=" * 60)
print("INICIANDO O METROPOLIS-HASTINGS")
print("=" * 60)

# ============================================
# PASSO 6: Loop principal do Metropolis-Hastings
# ============================================
for i in range(num_iteracoes):
    
    # ---------------------------------------------
    # 6.1: Gerar um palpite (proposta)
    # ---------------------------------------------
    # Usamos uma proposta Normal (Random Walk)
    x_novo = np.random.normal(loc=x_atual, scale=sigma_proposta)
    
    # ---------------------------------------------
    # 6.2: Calcular as probabilidades (não normalizadas)
    # ---------------------------------------------
    prob_atual = distribuicao_alvo(x_atual)
    prob_novo = distribuicao_alvo(x_novo)
    
    # ---------------------------------------------
    # 6.3: Calcular a razão de aceitação
    # ---------------------------------------------
    # Se prob_atual for zero (o que não deveria acontecer se escolhemos bem),
    # mas vamos tratar isso para robustez.
    if prob_atual == 0:
        # Se estamos num ponto inválido, sempre aceitamos o novo
        alpha = 1.0
    else:
        # Razão das probabilidades (não normalizadas)
        # Como a proposta é simétrica, a razão das propostas = 1
        alpha = prob_novo / prob_atual
    
    # ---------------------------------------------
    # 6.4: Decidir se aceita ou rejeita
    # ---------------------------------------------
    u = np.random.uniform(0, 1)
    
    if u <= alpha:
        # ACEITAR: ir para o novo ponto
        x_atual = x_novo
        
        # Garantir que não estamos em um ponto inválido (f(x) <= 0)
        # Se acontecer, o algoritmo naturalmente vai rejeitar passos futuros
        # até voltar para uma região válida
    
    # SEMPRE adicionar a amostra (mesmo se rejeitou, repetimos o ponto atual)
    amostras.append(x_atual)
    valores_amostras.append(distribuicao_alvo(x_atual))
    
    # ---------------------------------------------
    # 6.5: Mostrar progresso
    # ---------------------------------------------
    if (i + 1) % 10000 == 0:
        taxa_aceitacao = len(set(amostras)) / len(amostras) * 100
        print(f"Iteração {i+1}/{num_iteracoes}")
        print(f"  - Média das amostras até agora: {np.mean(amostras[-1000:]):.3f}")
        print(f"  - Taxa de aceitação (aprox): {taxa_aceitacao:.1f}%")
        print(f"  - Valor atual de f(x): {distribuicao_alvo(x_atual):.3f}")
        print()

# ============================================
# PASSO 7: Remover o Burn-in
# ============================================
amostras_finais = np.array(amostras[burn_in:])
valores_finais = np.array(valores_amostras[burn_in:])

print("=" * 60)
print("RESULTADOS FINAIS")
print("=" * 60)
print(f"Total de amostras: {len(amostras)}")
print(f"Burn-in removido: {burn_in}")
print(f"Amostras finais: {len(amostras_finais)}")
print(f"Média das amostras: {np.mean(amostras_finais):.4f}")
print(f"Desvio padrão das amostras: {np.std(amostras_finais):.4f}")
print(f"Valor médio de f(x) nas amostras: {np.mean(valores_finais):.4f}")

# ============================================
# PASSO 8: Visualizações
# ============================================
plt.figure(figsize=(15, 10))

# 8.1: Função polinomial e região amostrada
plt.subplot(2, 2, 1)
x_grid = np.linspace(x_min - 0.5, x_max + 0.5, 1000)
y_grid = funcao_polinomial(x_grid)

plt.plot(x_grid, y_grid, 'b-', linewidth=2, label='f(x)')
plt.fill_between(x_grid, 0, y_grid, where=(y_grid > 0), 
                  color='green', alpha=0.3, label='Região válida (f(x)>0)')
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.scatter(amostras_finais, [0]*len(amostras_finais), 
           color='red', s=1, alpha=0.3, label='Amostras')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Função Polinomial e Amostras')
plt.legend()
plt.grid(True, alpha=0.3)

# 8.2: Histograma das amostras (densidade)
plt.subplot(2, 2, 2)
plt.hist(amostras_finais, bins=60, density=True, alpha=0.7, 
         color='blue', label='Amostras do MH')

# Plotar a distribuição normalizada teórica (para comparação)
# f_normalizada(x) = f(x) / integral
if integral > 0:
    f_normalizada = funcao_polinomial(x_grid) / integral
    # Só plotar onde f(x) > 0
    mask = f_normalizada > 0
    plt.plot(x_grid[mask], f_normalizada[mask], 'r-', 
             linewidth=2, label='Distribuição teórica normalizada')

plt.xlabel('x')
plt.ylabel('Densidade')
plt.title('Histograma das Amostras vs Distribuição Teórica')
plt.legend()
plt.grid(True, alpha=0.3)

# 8.3: Trace plot (evolução temporal)
plt.subplot(2, 2, 3)
plt.plot(amostras_finais[:2000], alpha=0.7, linewidth=0.8)
plt.axhline(y=np.mean(amostras_finais), color='r', linestyle='--', 
            label=f'Média = {np.mean(amostras_finais):.3f}')
plt.xlabel('Iteração')
plt.ylabel('Valor de x')
plt.title('Trace Plot (primeiras 2000 amostras)')
plt.legend()
plt.grid(True, alpha=0.3)

# 8.4: Relação entre x e f(x) nas amostras
plt.subplot(2, 2, 4)
plt.scatter(amostras_finais[:1000], valores_finais[:1000], 
           alpha=0.5, s=10)
plt.plot(x_grid, funcao_polinomial(x_grid), 'r-', linewidth=2, label='f(x)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Amostras no Espaço (x, f(x))')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================
# PASSO 9: Análise Estatística Adicional
# ============================================
print("\n" + "=" * 60)
print("ANÁLISE ESTATÍSTICA")
print("=" * 60)

# Percentis
percentis = [1, 5, 25, 50, 75, 95, 99]
print("Percentis das amostras:")
for p in percentis:
    valor = np.percentile(amostras_finais, p)
    print(f"  {p}%: {valor:.4f}")

# Calcular o ponto de máximo da função (para referência)
derivada = lambda x: -3*x**2 + 4*x + 5  # Derivada de f(x)
# Encontrar raízes da derivada (pontos críticos)
raizes = np.roots([-3, 4, 5])  # Coeficientes da derivada
maximo_real = None
for r in raizes:
    if np.isreal(r) and x_min <= r <= x_max:
        r_real = np.real(r)
        if funcao_polinomial(r_real) > 0:
            if maximo_real is None or funcao_polinomial(r_real) > funcao_polinomial(maximo_real):
                maximo_real = r_real

if maximo_real is not None:
    print(f"\nPonto de máximo da função: x = {maximo_real:.4f}")
    print(f"Valor máximo de f(x): {funcao_polinomial(maximo_real):.4f}")
    print(f"Moda das amostras (pico): {np.percentile(amostras_finais, 99):.4f}")
else:
    print("\nNão foi possível encontrar o máximo da função no domínio.")

# ============================================
# PASSO 10: Função para salvar os resultados
# ============================================
def salvar_resultados(nome_arquivo="amostras_metropolis.csv"):
    """
    Salva as amostras em um arquivo CSV para análise posterior.
    """
    import pandas as pd
    df = pd.DataFrame({
        'x': amostras_finais,
        'f_x': valores_finais
    })
    df.to_csv(nome_arquivo, index=False)
    print(f"\nAmostras salvas em '{nome_arquivo}'")

# Descomente a linha abaixo se quiser salvar
# salvar_resultados()

print("\n" + "=" * 60)
print("FIM DO ALGORITMO")
print("=" * 60)