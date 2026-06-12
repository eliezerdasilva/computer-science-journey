# monte_carlo.py
"""
Classe base do método de Monte Carlo
"""

import numpy as np
import time
from dataclasses import dataclass

from config import DEFAULT_N_PONTOS, DEFAULT_SEED


@dataclass
class Resultado:
    """Armazena o resultado de uma simulação"""
    area_estimada: float
    area_teorica: float
    erro_absoluto: float
    erro_percentual: float
    pontos_dentro: int
    pontos_totais: int
    tempo_execucao: float
    
    def __str__(self):
        return f"""
╔══════════════════════════════════════════════════════════╗
║                    RESULTADO DA SIMULAÇÃO                ║
╠══════════════════════════════════════════════════════════╣
║ Pontos totais:     {self.pontos_totais:>12,}                          ║
║ Pontos dentro:     {self.pontos_dentro:>12,}                          ║
║ Área estimada:     {self.area_estimada:>12.6f}                        ║
║ Área teórica:      {self.area_teorica:>12.6f}                         ║
║ Erro absoluto:     {self.erro_absoluto:>12.6f}                        ║
║ Erro percentual:   {self.erro_percentual:>11.4f}%                     ║
║ Tempo de execução: {self.tempo_execucao:>12.4f} segundos              ║
╚══════════════════════════════════════════════════════════╝
"""


class MonteCarloArea:
    """
    Classe base para cálculo de áreas usando Monte Carlo.
    
    Para criar uma nova figura, herde desta classe e implemente:
    - area_retangulo_delimitador()
    - gerar_pontos()
    - esta_dentro()
    - area_teorica()
    """
    
    def __init__(self, n_pontos: int = DEFAULT_N_PONTOS, seed: int = DEFAULT_SEED):
        self.n_pontos = n_pontos
        self.seed = seed
        self._rng = np.random.default_rng(seed)
        
    def area_retangulo_delimitador(self) -> float:
        """Retorna área do retângulo que contém a figura"""
        raise NotImplementedError("Implemente na classe filha")
        
    def gerar_pontos(self):
        """Gera pontos aleatórios dentro do retângulo delimitador"""
        raise NotImplementedError("Implemente na classe filha")
    
    def esta_dentro(self, x, y):
        """Verifica quais pontos estão dentro da figura"""
        raise NotImplementedError("Implemente na classe filha")
    
    def area_teorica(self) -> float:
        """Retorna área teórica para comparação"""
        raise NotImplementedError("Implemente na classe filha")
    
    def calcular(self, verbose: bool = True) -> Resultado:
        """Executa a simulação Monte Carlo"""
        inicio = time.time()
        
        x, y = self.gerar_pontos()
        dentro = self.esta_dentro(x, y)
        pontos_dentro = np.sum(dentro)
        
        area_ret = self.area_retangulo_delimitador()
        area_estimada = (pontos_dentro / self.n_pontos) * area_ret
        
        tempo = time.time() - inicio
        
        resultado = Resultado(
            area_estimada=area_estimada,
            area_teorica=self.area_teorica(),
            erro_absoluto=abs(area_estimada - self.area_teorica()),
            erro_percentual=abs((area_estimada - self.area_teorica()) / self.area_teorica()) * 100,
            pontos_dentro=pontos_dentro,
            pontos_totais=self.n_pontos,
            tempo_execucao=tempo
        )
        
        if verbose:
            print(resultado)
            
        return resultado