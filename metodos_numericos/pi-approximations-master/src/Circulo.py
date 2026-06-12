
import numpy as np
import time
from functools import cached_property
from dataclasses import dataclass
from typing import Callable, Tuple, List
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle

class Circulo():
    
    
    def __init__(self, raio: float = 1.0, n_pontos: int = 100000, seed: int = None):
        super().__init__(n_pontos, seed)
        self.raio = raio
        
    def area_retangulo_delimitador(self) -> float:
        # Quadrado que circunscreve o círculo: lado = 2R
        return (2 * self.raio) ** 2
        
    def gerar_pontos(self) -> Tuple[np.ndarray, np.ndarray]:
        x = self._rng.uniform(-self.raio, self.raio, self.n_pontos)
        y = self._rng.uniform(-self.raio, self.raio, self.n_pontos)
        return x, y
        
    def esta_dentro(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        # Equação do círculo: x² + y² ≤ R²
        return x**2 + y**2 <= self.raio**2
        
    def area_teorica(self) -> float:
        return np.pi * self.raio**2
        
    def _plot_figura(self, ax):
        circle = Circle((0, 0), self.raio, fill=False, color='black', linewidth=2)
        ax.add_patch(circle)
