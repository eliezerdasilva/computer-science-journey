# figuras.py
"""
Implementação das figuras geométricas
"""

import numpy as np
from typing import Callable

from monte_carlo import MonteCarloArea
from config import DEFAULT_N_PONTOS, DEFAULT_SEED


class Circulo(MonteCarloArea):
    """Círculo de raio R"""
    
    def __init__(self, raio: float = 1.0, n_pontos: int = DEFAULT_N_PONTOS, seed: int = DEFAULT_SEED):
        super().__init__(n_pontos, seed)
        self.raio = raio
        
    def area_retangulo_delimitador(self) -> float:
        return (2 * self.raio) ** 2
        
    def gerar_pontos(self):
        x = self._rng.uniform(-self.raio, self.raio, self.n_pontos)
        y = self._rng.uniform(-self.raio, self.raio, self.n_pontos)
        return x, y
        
    def esta_dentro(self, x, y):
        return x**2 + y**2 <= self.raio**2
        
    def area_teorica(self) -> float:
        return np.pi * self.raio**2
        
    def __str__(self):
        return f"Círculo (raio={self.raio})"


class Elipse(MonteCarloArea):
    """Elipse com semi-eixos a e b"""
    
    def __init__(self, a: float = 2.0, b: float = 1.0, n_pontos: int = DEFAULT_N_PONTOS, seed: int = DEFAULT_SEED):
        super().__init__(n_pontos, seed)
        self.a = a  # semi-eixo x
        self.b = b  # semi-eixo y
        
    def area_retangulo_delimitador(self) -> float:
        return (2 * self.a) * (2 * self.b)
        
    def gerar_pontos(self):
        x = self._rng.uniform(-self.a, self.a, self.n_pontos)
        y = self._rng.uniform(-self.b, self.b, self.n_pontos)
        return x, y
        
    def esta_dentro(self, x, y):
        return (x**2 / self.a**2) + (y**2 / self.b**2) <= 1
        
    def area_teorica(self) -> float:
        return np.pi * self.a * self.b
        
    def __str__(self):
        return f"Elipse (a={self.a}, b={self.b})"


class Retangulo(MonteCarloArea):
    """Retângulo de largura W e altura H"""
    
    def __init__(self, largura: float = 2.0, altura: float = 1.0, n_pontos: int = DEFAULT_N_PONTOS, seed: int = DEFAULT_SEED):
        super().__init__(n_pontos, seed)
        self.largura = largura
        self.altura = altura
        
    def area_retangulo_delimitador(self) -> float:
        # O próprio retângulo é o delimitador
        return self.largura * self.altura
        
    def gerar_pontos(self):
        x = self._rng.uniform(0, self.largura, self.n_pontos)
        y = self._rng.uniform(0, self.altura, self.n_pontos)
        return x, y
        
    def esta_dentro(self, x, y):
        # Todos os pontos estão dentro do retângulo
        return np.ones(self.n_pontos, dtype=bool)
        
    def area_teorica(self) -> float:
        return self.largura * self.altura
        
    def __str__(self):
        return f"Retângulo ({self.largura} x {self.altura})"


class Quadrado(MonteCarloArea):
    """Quadrado de lado L"""
    
    def __init__(self, lado: float = 2.0, n_pontos: int = DEFAULT_N_PONTOS, seed: int = DEFAULT_SEED):
        super().__init__(n_pontos, seed)
        self.lado = lado
        
    def area_retangulo_delimitador(self) -> float:
        return self.lado * self.lado
        
    def gerar_pontos(self):
        x = self._rng.uniform(0, self.lado, self.n_pontos)
        y = self._rng.uniform(0, self.lado, self.n_pontos)
        return x, y
        
    def esta_dentro(self, x, y):
        return np.ones(self.n_pontos, dtype=bool)
        
    def area_teorica(self) -> float:
        return self.lado**2
        
    def __str__(self):
        return f"Quadrado (lado={self.lado})"


class Triangulo(MonteCarloArea):
    """Triângulo retângulo com base B e altura H"""
    
    def __init__(self, base: float = 2.0, altura: float = 2.0, n_pontos: int = DEFAULT_N_PONTOS, seed: int = DEFAULT_SEED):
        super().__init__(n_pontos, seed)
        self.base = base
        self.altura = altura
        
    def area_retangulo_delimitador(self) -> float:
        # Retângulo que contém o triângulo
        return self.base * self.altura
        
    def gerar_pontos(self):
        x = self._rng.uniform(0, self.base, self.n_pontos)
        y = self._rng.uniform(0, self.altura, self.n_pontos)
        return x, y
        
    def esta_dentro(self, x, y):
        # Pontos abaixo da reta y = (altura/base) * x
        return y <= (self.altura / self.base) * x
        
    def area_teorica(self) -> float:
        return (self.base * self.altura) / 2
        
    def __str__(self):
        return f"Triângulo (base={self.base}, altura={self.altura})"


class FuncaoQualquer(MonteCarloArea):
    """Área sob uma função f(x) no intervalo [a, b]"""
    
    def __init__(self, func: Callable, a: float, b: float, n_pontos: int = DEFAULT_N_PONTOS, seed: int = DEFAULT_SEED):
        super().__init__(n_pontos, seed)
        self.func = func
        self.a = a
        self.b = b
        self.y_max = self._estimar_y_max()
        
    def _estimar_y_max(self, n_amostras: int = 10000) -> float:
        x_amostra = np.linspace(self.a, self.b, n_amostras)
        y_amostra = self.func(x_amostra)
        return float(np.max(y_amostra)) * 1.05
        
    def area_retangulo_delimitador(self) -> float:
        return (self.b - self.a) * self.y_max
        
    def gerar_pontos(self):
        x = self._rng.uniform(self.a, self.b, self.n_pontos)
        y = self._rng.uniform(0, self.y_max, self.n_pontos)
        return x, y
        
    def esta_dentro(self, x, y):
        return y <= self.func(x)
        
    def area_teorica(self) -> float:
        # Estimativa com Monte Carlo de alta precisão
        n_alta = min(self.n_pontos * 5, 5_000_000)
        rng_temp = np.random.default_rng(42)
        
        x_alta = rng_temp.uniform(self.a, self.b, n_alta)
        y_alta = rng_temp.uniform(0, self.y_max, n_alta)
        dentro_alta = y_alta <= self.func(x_alta)
        
        area_ret = (self.b - self.a) * self.y_max
        return (np.sum(dentro_alta) / n_alta) * area_ret
        
    def __str__(self):
        return f"Função f(x) em [{self.a}, {self.b}]"