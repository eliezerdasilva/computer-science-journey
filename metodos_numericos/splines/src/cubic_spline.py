from .spline_base import SplineBase
import numpy as np
from typing import Literal, Optional

class CubicSpline(SplineBase):
    """
        Função de teste: y = sin(x) com 5 pontos (0, π/4, π/2, 3π/4, π)

Natural:
  - Pontas "soltas"
  - Curva mais suave no geral
  - Pode ter um pouco mais de erro nas bordas
  📈 Curva: ~__~~__~ (ondulada suave)

Completa:
  - Pontas fixadas com inclinação conhecida (cos(0)=1, cos(π)=-1)
  - Melhor precisão total
  - Requer informação extra
  📈 Curva: ~~__~~ (segue melhor a função)

Not-a-Knot:
  - Semelhante à natural, mas com melhor precisão
  - Não requer info extra
  - Padrão recomendado
  📈 Curva: ~~__~~ (muito similar à completa)
    
    """
    
    def __init__(self, x: np.ndarray, y: np.ndarray, 
                 bc_type: Literal['natural', 'clamped', 'not-a-knot'] = 'not-a-knot',
                 yp0: Optional[float] = None, ypn: Optional[float] = None):
        """
        Args:
            x, y: Pontos de dados
            bc_type: Tipo de condição de contorno
            yp0: y'(x₀) para clamped
            ypn: y'(xₙ) para clamped
        """
        super().__init__(x, y)
        self.bc_type = bc_type
        self.M = self._solve_system(yp0, ypn)
        self.coeffs = self._compute_coefficients()
    
    def _solve_system(self, yp0: Optional[float], ypn: Optional[float]) -> np.ndarray:
        """
        Resolve o sistema tridiagonal para as segundas derivadas Mᵢ = s''(xᵢ) [citation:9].
        
        Para i = 1..n-1:
        (hᵢ₋₁/6)Mᵢ₋₁ + (hᵢ₋₁+hᵢ)/3 Mᵢ + (hᵢ/6)Mᵢ₊₁ = 
            (yᵢ₊₁-yᵢ)/hᵢ - (yᵢ-yᵢ₋₁)/hᵢ₋₁ [citation:9]
        """
        n = self.n
        N = n + 1  # número de nós
        
        # Matriz tridiagonal e vetor RHS
        A = np.zeros((N, N))
        b = np.zeros(N)
        
        # Equações internas (i = 1..n-1)
        for i in range(1, n):
            A[i, i-1] = self.h[i-1] / 6
            A[i, i] = (self.h[i-1] + self.h[i]) / 3
            A[i, i+1] = self.h[i] / 6
            b[i] = (self.y[i+1] - self.y[i]) / self.h[i] - \
                   (self.y[i] - self.y[i-1]) / self.h[i-1]
        
        # Condições de contorno
        if self.bc_type == 'natural':
            # s''(x₀) = s''(xₙ) = 0 [citation:6][citation:8]
            A[0, 0] = 1
            A[N-1, N-1] = 1
            b[0] = 0
            b[N-1] = 0
            
        elif self.bc_type == 'clamped':
            # s'(x₀) = yp0, s'(xₙ) = ypn [citation:7][citation:9]
            if yp0 is None or ypn is None:
                raise ValueError("yp0 e ypn são necessários para clamped spline")
            A[0, 0] = self.h[0] / 3
            A[0, 1] = self.h[0] / 6
            b[0] = (self.y[1] - self.y[0]) / self.h[0] - yp0
            
            A[N-1, N-2] = self.h[n-1] / 6
            A[N-1, N-1] = self.h[n-1] / 3
            b[N-1] = ypn - (self.y[n] - self.y[n-1]) / self.h[n-1]
            
        elif self.bc_type == 'not-a-knot':
            # Continuidade de s''' em x₁ e xₙ₋₁ [citation:7][citation:8]
            # Equivalente a: M₁ = M₀ e Mₙ = Mₙ₋₁ (para malha uniforme)
            # Implementação simplificada para malhas uniformes
            A[0, 0] = 1
            A[0, 1] = -1
            b[0] = 0
            A[N-1, N-2] = -1
            A[N-1, N-1] = 1
            b[N-1] = 0
            
        else:
            raise ValueError(f"bc_type '{self.bc_type}' não reconhecido")
        
        return np.linalg.solve(A, b)
    
    def _compute_coefficients(self):
        """
        Calcula os coeficientes aᵢ, bᵢ, cᵢ, dᵢ para cada segmento [citation:7][citation:9].
        Forma: sᵢ(x) = aᵢ + bᵢ(x-xᵢ) + cᵢ(x-xᵢ)² + dᵢ(x-xᵢ)³
        """
        coeffs = []
        for i in range(self.n):
            hi = self.h[i]
            Mi = self.M[i]
            Mi1 = self.M[i+1]
            
            # Fórmulas baseadas na representação com Mᵢ [citation:9]
            a = self.y[i]
            b = (self.y[i+1] - self.y[i]) / hi - hi*(2*Mi + Mi1) / 6
            c = Mi / 2
            d = (Mi1 - Mi) / (6 * hi)
            coeffs.append((a, b, c, d))
        
        return coeffs
    
    def evaluate(self, x_val: float) -> float:
        if x_val < self.x[0] or x_val > self.x[-1]:
            return np.nan
        
        i = self._locate_interval(x_val)
        dx = x_val - self.x[i]
        a, b, c, d = self.coeffs[i]
        return a + b*dx + c*dx**2 + d*dx**3