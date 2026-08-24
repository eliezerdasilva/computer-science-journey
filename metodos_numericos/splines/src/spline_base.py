import numpy as np
from typing import List, Tuple, Callable, Optional

class SplineBase:
    """Classe base para implementação de splines."""
    
    def __init__(self, x: np.ndarray, y: np.ndarray):
        """
        Inicializa o spline com os pontos de dados.
        
        Args:
            x: Array de coordenadas x (devem ser crescentes)
            y: Array de coordenadas y
        """
        if len(x) != len(y):
            raise ValueError("x e y devem ter o mesmo comprimento")
        if not np.all(np.diff(x) > 0):
            raise ValueError("x deve ser estritamente crescente")
        
        self.x = x.astype(float)
        self.y = y.astype(float)
        self.n = len(x) - 1  # número de intervalos
        self.h = np.diff(x)  # espaçamentos entre nós
        
    def _locate_interval(self, x_val: float) -> int:
        """Encontra o índice do intervalo que contém x_val [citation:2]."""
        if x_val < self.x[0] or x_val > self.x[-1]:
            raise ValueError(f"x={x_val} fora do domínio [{self.x[0]}, {self.x[-1]}]")
        return np.searchsorted(self.x, x_val) - 1
    
    def evaluate(self, x_val: float) -> float:
        """Avalia o spline em um ponto. Deve ser sobrescrito."""
        raise NotImplementedError