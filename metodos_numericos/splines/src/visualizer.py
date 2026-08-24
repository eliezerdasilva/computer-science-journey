import matplotlib.pyplot as plt
import numpy as np
from typing import List

class SplineVisualizer:
    """Classe para visualização de splines e comparação."""
    
    def __init__(self, figsize=(12, 8)):
        self.figsize = figsize
        self.figures = []
    
    def plot_spline_comparison(self, x_data, y_data, splines_dict, 
                                title="Comparação de Splines", n_points=500):
        """
        Plota diferentes splines sobre os dados originais.
        
        Args:
            splines_dict: {'nome': spline_object}
        """
        x_plot = np.linspace(min(x_data), max(x_data), n_points)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Gráfico principal
        ax1.scatter(x_data, y_data, color='black', s=50, zorder=5, label='Dados')
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(splines_dict)))
        for (name, spline), color in zip(splines_dict.items(), colors):
            y_plot = np.array([spline.evaluate(x) for x in x_plot])
            ax1.plot(x_plot, y_plot, color=color, linewidth=2, label=name)
        
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_title(title)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de erro (se houver função verdadeira)
        # ...
        
        self.figures.append(fig)
        plt.show()
        return fig
    
    def plot_derivatives(self, spline, x_data, title="Derivadas do Spline"):
        """Plota o spline e suas derivadas."""
        x_plot = np.linspace(min(x_data), max(x_data), 500)
        # ...