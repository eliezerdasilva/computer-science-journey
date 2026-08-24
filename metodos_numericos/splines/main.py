import numpy as np
from src.linear_spline import LinearSpline
from src.cubic_spline import CubicSpline
from src.visualizer import SplineVisualizer

def demonstrar_runge():
    """Demonstração com a função de Runge - clássico exemplo de oscilação [citation:5][citation:8]."""
    print("="*60)
    print("DEMONSTRAÇÃO: Interpolação da Função de Runge")
    print("="*60)
    
    # Função de Runge: f(x) = 1/(1+25x²)
    def runge(x): return 1 / (1 + 25 * x**2)
    
    # Pontos igualmente espaçados
    x_data = np.linspace(-1, 1, 11)
    y_data = runge(x_data)
    
    print(f"Dados: {len(x_data)} pontos igualmente espaçados")
    
    # Criar splines
    splines = {
        'Linear': LinearSpline(x_data, y_data),
        'Cúbico Natural': CubicSpline(x_data, y_data, bc_type='natural'),
        'Cúbico Not-a-Knot': CubicSpline(x_data, y_data, bc_type='not-a-knot'),
    }
    
    # Visualizar
    viz = SplineVisualizer()
    viz.plot_spline_comparison(x_data, y_data, splines, 
                               title="Splines para Função de Runge")
    
    print("Observe como os splines evitam oscilações entre os pontos!")

def demonstrar_seno():
    """Demonstração com função seno - mostra suavidade dos splines cúbicos [citation:8]."""
    print("\n" + "="*60)
    print("DEMONSTRAÇÃO: Interpolação de sin(x)")
    print("="*60)
    
    x_data = np.linspace(0, np.pi, 5)  # apenas 5 pontos
    y_data = np.sin(x_data)
    
    splines = {
        'Linear': LinearSpline(x_data, y_data),
        'Cúbico Natural': CubicSpline(x_data, y_data, bc_type='natural'),
        'Cúbico Not-a-Knot': CubicSpline(x_data, y_data, bc_type='not-a-knot'),
    }
    
    viz = SplineVisualizer()
    viz.plot_spline_comparison(x_data, y_data, splines, 
                               title=f"Splines para sin(x) com {len(x_data)} pontos")

if __name__ == "__main__":
    demonstrar_runge()
    demonstrar_seno()