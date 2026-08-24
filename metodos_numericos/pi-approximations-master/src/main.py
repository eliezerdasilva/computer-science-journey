# main.py
"""
Programa principal para cálculo de áreas usando Monte Carlo
"""

import numpy as np

# Importar as classes e funções dos outros arquivos
from figuras import Circulo, Elipse, Retangulo, Quadrado, Triangulo, FuncaoQualquer
from visualizar import plotar_figura, comparar_figuras
from config import DEFAULT_N_PONTOS


# ============================================================
# EXEMPLO 1: Círculo
# ============================================================
def exemplo_circulo():
    print("\n" + "="*50)
    print("EXEMPLO 1: CÍRCULO")
    print("="*50)
    
    # Criar círculo de raio 1 com 1 milhão de pontos
    circulo = Circulo(raio=1.0, n_pontos=1_000_000)
    
    # Calcular área
    resultado = circulo.calcular()
    
    # Plotar (opcional - descomente para ver o gráfico)
    plotar_figura(circulo, mostrar=True, salvar=True, nome_arquivo="circulo.png")


# ============================================================
# EXEMPLO 2: Elipse
# ============================================================
def exemplo_elipse():
    print("\n" + "="*50)
    print("EXEMPLO 2: ELIPSE")
    print("="*50)
    
    # Criar elipse com a=3, b=1.5
    elipse = Elipse(a=3.0, b=1.5, n_pontos=1_000_000)
    resultado = elipse.calcular()
    
    # plotar_figura(elipse, mostrar=True, salvar=True, nome_arquivo="elipse.png")


# ============================================================
# EXEMPLO 3: Retângulo
# ============================================================
def exemplo_retangulo():
    print("\n" + "="*50)
    print("EXEMPLO 3: RETÂNGULO")
    print("="*50)
    
    # Criar retângulo 4x2
    retangulo = Retangulo(largura=4.0, altura=2.0, n_pontos=1_000_000)
    resultado = retangulo.calcular()
    
    # plotar_figura(retangulo, mostrar=True, salvar=True, nome_arquivo="retangulo.png")


# ============================================================
# EXEMPLO 4: Quadrado
# ============================================================
def exemplo_quadrado():
    print("\n" + "="*50)
    print("EXEMPLO 4: QUADRADO")
    print("="*50)
    
    # Criar quadrado de lado 3
    quadrado = Quadrado(lado=3.0, n_pontos=1_000_000)
    resultado = quadrado.calcular()
    
    # plotar_figura(quadrado, mostrar=True, salvar=True, nome_arquivo="quadrado.png")


# ============================================================
# EXEMPLO 5: Triângulo
# ============================================================
def exemplo_triangulo():
    print("\n" + "="*50)
    print("EXEMPLO 5: TRIÂNGULO")
    print("="*50)
    
    # Criar triângulo retângulo de base 3 e altura 4
    triangulo = Triangulo(base=3.0, altura=4.0, n_pontos=1_000_000)
    resultado = triangulo.calcular()
    
    # plotar_figura(triangulo, mostrar=True, salvar=True, nome_arquivo="triangulo.png")


# ============================================================
# EXEMPLO 6: Área sob uma função (curva)
# ============================================================
def exemplo_curva():
    print("\n" + "="*50)
    print("EXEMPLO 6: ÁREA SOB CURVA")
    print("="*50)
    
    # Definir uma função: f(x) = x² (parábola)
    def f_quadrado(x):
        return  x**2
    
    # Área sob x² de 0 a 2 = 8/3 ≈ 2.66667
    curva = FuncaoQualquer(f_quadrado, a=0, b=2, n_pontos=100_000_000)
    resultado = curva.calcular()
    
    plotar_figura(curva, mostrar=True, salvar=True, nome_arquivo="curva_quadrado.png")
    
    # Outra função: seno
    print("\n▶ Área sob f(x) = sen(x) de 0 a π (teórica = 2)")
    def f_seno(x):
        return np.sin(x)
    
    seno = FuncaoQualquer(f_seno, a=0, b=np.pi, n_pontos=500_000)
    seno.calcular()


# ============================================================
# EXEMPLO 7: Comparar várias figuras
# ============================================================
def exemplo_comparacao():
    print("\n" + "="*50)
    print("EXEMPLO 7: COMPARAÇÃO DE FIGURAS")
    print("="*50)
    
    # Criar figuras com menos pontos para visualização rápida
    circulo = Circulo(raio=1.0, n_pontos=50_000)
    elipse = Elipse(a=2.0, b=1.0, n_pontos=50_000)
    retangulo = Retangulo(largura=3.0, altura=2.0, n_pontos=50_000)
    quadrado = Quadrado(lado=2.0, n_pontos=50_000)
    
    # Comparar visualmente
    comparar_figuras([circulo, elipse, retangulo, quadrado], salvar=True)


# ============================================================
# EXEMPLO 8: Teste com diferentes quantidades de pontos
# ============================================================
def exemplo_convergencia():
    print("\n" + "="*50)
    print("EXEMPLO 8: TESTE DE CONVERGÊNCIA")
    print("="*50)
    print(f"{'Pontos':>12} | {'Área estimada':>14} | {'Erro %':>10}")
    print("-"*50)
    
    pontos_teste = [1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    
    for n in pontos_teste:
        circulo = Circulo(raio=1.0, n_pontos=n)
        res = circulo.calcular(verbose=False)
        print(f"{n:>12,} | {res.area_estimada:>14.6f} | {res.erro_percentual:>9.4f}%")


# ============================================================
# MAIN - Escolha qual exemplo executar
# ============================================================

if __name__ == "__main__":
    
    print("\n" + "█"*50)
    print("     CÁLCULO DE ÁREAS COM MONTE CARLO")
    print("█"*50)
    
    # Execute o exemplo que você quiser:
    
    #exemplo_circulo()      # ✅ Círculo
    # exemplo_elipse()       # Elipse
    # exemplo_retangulo()    # Retângulo
    # exemplo_quadrado()     # Quadrado
    # exemplo_triangulo()    # Triângulo
    exemplo_curva()        # Área sob curva
    # exemplo_comparacao()   # Comparar figuras
    # exemplo_convergencia() # Teste de convergência
    
    print("\n✅ Fim do programa!")