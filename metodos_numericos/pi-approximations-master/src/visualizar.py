# visualizar.py
"""
Funções para visualização gráfica
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, Polygon

from config import COR_DENTRO, COR_FORA, MAX_PONTOS_PLOT, TAMANHO_FIGURA


def plotar_circulo(ax, raio, cor='black'):
    """Desenha um círculo no eixo"""
    circle = Circle((0, 0), raio, fill=False, color=cor, linewidth=2)
    ax.add_patch(circle)


def plotar_elipse(ax, a, b, cor='black'):
    """Desenha uma elipse no eixo"""
    ellipse = Ellipse((0, 0), 2*a, 2*b, fill=False, color=cor, linewidth=2)
    ax.add_patch(ellipse)


def plotar_retangulo(ax, largura, altura, cor='black', origem=(0, 0)):
    """Desenha um retângulo no eixo"""
    rect = Rectangle(origem, largura, altura, fill=False, color=cor, linewidth=2)
    ax.add_patch(rect)


def plotar_funcao(ax, func, a, b, y_max, cor='black'):
    """Desenha uma função no eixo"""
    x_plot = np.linspace(a, b, 1000)
    y_plot = func(x_plot)
    ax.plot(x_plot, y_plot, cor, linewidth=2)
    ax.fill_between(x_plot, 0, y_plot, alpha=0.3, color='gray')
    ax.axhline(y=y_max, color='gray', linestyle='--', alpha=0.5)


def plotar_figura(figura, mostrar=True, salvar=False, nome_arquivo="figura.png"):
    """
    Plota os pontos e o contorno da figura
    
    Parâmetros:
    -----------
    figura : objeto da classe figura (Circulo, Elipse, Retangulo, etc.)
    mostrar : bool - se True, mostra a janela
    salvar : bool - se True, salva em arquivo
    nome_arquivo : str - nome do arquivo para salvar
    """
    fig, ax = plt.subplots(figsize=TAMANHO_FIGURA)
    
    # Gerar pontos
    x, y = figura.gerar_pontos()
    dentro = figura.esta_dentro(x, y)
    
    # Amostrar para visualização (não mostrar todos os pontos)
    n_plot = min(figura.n_pontos, MAX_PONTOS_PLOT)
    indices = np.random.choice(figura.n_pontos, n_plot, replace=False)
    
    # Plotar pontos
    ax.scatter(x[indices][~dentro[indices]], y[indices][~dentro[indices]], 
              c=COR_FORA, s=5, alpha=0.5, label='Fora')
    ax.scatter(x[indices][dentro[indices]], y[indices][dentro[indices]], 
              c=COR_DENTRO, s=5, alpha=0.5, label='Dentro')
    
    # Plotar contorno da figura
    from figuras import Circulo, Elipse, Retangulo, Quadrado, Triangulo, FuncaoQualquer
    
    if isinstance(figura, Circulo):
        plotar_circulo(ax, figura.raio)
    elif isinstance(figura, Elipse):
        plotar_elipse(ax, figura.a, figura.b)
    elif isinstance(figura, (Retangulo, Quadrado)):
        plotar_retangulo(ax, figura.largura if hasattr(figura, 'largura') else figura.lado, 
                        figura.altura if hasattr(figura, 'altura') else figura.lado)
    elif isinstance(figura, FuncaoQualquer):
        plotar_funcao(ax, figura.func, figura.a, figura.b, figura.y_max)
    
    # Configurar gráfico
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    ax.set_title(f'{figura} - Monte Carlo\n{figura.n_pontos:,} pontos')
    ax.grid(True, alpha=0.3)
    
    if salvar:
        plt.savefig(nome_arquivo, dpi=150, bbox_inches='tight')
        print(f"✅ Gráfico salvo como: {nome_arquivo}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def comparar_figuras(lista_figuras, salvar=False):
    """
    Compara múltiplas figuras em subplots
    
    Parâmetros:
    -----------
    lista_figuras : list - lista de objetos de figuras
    salvar : bool - se True, salva a figura
    """
    n = len(lista_figuras)
    fig, axes = plt.subplots(1, n, figsize=(5*n, 5))
    
    if n == 1:
        axes = [axes]
    
    for i, (figura, ax) in enumerate(zip(lista_figuras, axes)):
        # Gerar pontos
        x, y = figura.gerar_pontos()
        dentro = figura.esta_dentro(x, y)
        
        # Amostrar
        n_plot = min(figura.n_pontos, MAX_PONTOS_PLOT)
        indices = np.random.choice(figura.n_pontos, n_plot, replace=False)
        
        # Plotar
        ax.scatter(x[indices][~dentro[indices]], y[indices][~dentro[indices]], 
                  c=COR_FORA, s=2, alpha=0.5)
        ax.scatter(x[indices][dentro[indices]], y[indices][dentro[indices]], 
                  c=COR_DENTRO, s=2, alpha=0.5)
        
        # Plotar contorno
        from figuras import Circulo, Elipse, Retangulo, Quadrado, Triangulo, FuncaoQualquer
        
        if isinstance(figura, Circulo):
            plotar_circulo(ax, figura.raio)
        elif isinstance(figura, Elipse):
            plotar_elipse(ax, figura.a, figura.b)
        elif isinstance(figura, (Retangulo, Quadrado)):
            plotar_retangulo(ax, figura.largura if hasattr(figura, 'largura') else figura.lado, 
                            figura.altura if hasattr(figura, 'altura') else figura.lado)
        
        ax.set_aspect('equal')
        ax.set_title(f'{figura}\n{figura.n_pontos:,} pontos')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig("comparacao_figuras.png", dpi=150, bbox_inches='tight')
        print("✅ Comparação salva como: comparacao_figuras.png")
    
    plt.show()