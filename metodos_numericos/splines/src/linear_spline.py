from .spline_base import SplineBase
import numpy as np

class LinearSpline(SplineBase):
    """
    Spline linear (grau 1).
    Fórmula: sᵢ(x) = yᵢ + (yᵢ₊₁ - yᵢ)/hᵢ * (x - xᵢ) [citation:6][citation:7]
    """
    
    def __init__(self, x: np.ndarray, y: np.ndarray):
        super().__init__(x, y)
        # Pré-calcular inclinações de cada segmento
        self.m = np.diff(y) / self.h
    
    def evaluate(self, x_val: float) -> float:
        if x_val < self.x[0] or x_val > self.x[-1]:
            return np.nan
        
        i = self._locate_interval(x_val)
        return self.y[i] + self.m[i] * (x_val - self.x[i])
    
    def evaluate_batch(self, x_vals: np.ndarray) -> np.ndarray:
        """Avalia o spline em múltiplos pontos de forma vetorizada."""
        return np.array([self.evaluate(x) for x in x_vals])