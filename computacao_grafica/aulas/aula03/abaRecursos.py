"""
abaRecursos.py — Sidebar do editor 2D (versao com ferramentas de manipulacao)
==============================================================================
Secoes da sidebar:
  1) SELECIONAR + MANIPULACAO: selecionar, girar-esq, girar-dir, aumentar,
     diminuir, transladar
  2) PALETA DE CORES: 10 circulos
  3) CRIACAO: retangulo, circulo, triangulo, segmento, poligono

O modulo NAO conhece o editor. Expoe:
  - SIDEBAR_LARGURA
  - class Sidebar
      - desenhar(batch, shapes_list)
      - processar_clique(x, y) -> (tipo_evento, valor) ou None
      - cor_atual()
      - ferramenta_ativa
"""

import math

from pyglet import shapes


# ======================================================================
# BLOCO A — CONSTANTES DA SIDEBAR
# ======================================================================
SIDEBAR_LARGURA = 120

PALETA_CORES = [
    (230,  60,  60),
    (240, 140,  40),
    (240, 220,  60),
    (120, 220, 120),
    ( 60, 200, 200),
    ( 60, 150, 240),
    (140, 100, 220),
    (230, 100, 180),
    (120, 120, 120),
    ( 40,  40,  40),
]

COR_FUNDO_SIDEBAR = (245, 245, 245)
COR_BORDA_SIDEBAR = (200, 200, 200)
COR_BOTAO_ATIVO   = ( 60, 150, 240)
COR_BOTAO_INATIVO = (220, 220, 220)
COR_ICONE_ATIVO   = (255, 255, 255)
COR_ICONE_INATIVO = ( 60,  60,  60)


# ======================================================================
# BLOCO B — BOTOES
# ======================================================================
class BotaoCor:
    def __init__(self, cor_rgb, centro_x, centro_y, raio):
        self.cor_rgb = cor_rgb
        self.cx = centro_x
        self.cy = centro_y
        self.raio = raio

    def contem(self, x, y):
        return (x - self.cx) ** 2 + (y - self.cy) ** 2 <= self.raio ** 2


class BotaoFerramenta:
    def __init__(self, tipo, x, y, tamanho):
        self.tipo = tipo
        self.x = x
        self.y = y
        self.tamanho = tamanho

    def contem(self, x, y):
        return (self.x <= x <= self.x + self.tamanho and
                self.y <= y <= self.y + self.tamanho)

    def centro(self):
        return (self.x + self.tamanho / 2, self.y + self.tamanho / 2)


# ======================================================================
# BLOCO C — SIDEBAR
# ======================================================================
class Sidebar:
    def __init__(self, altura_janela):
        self.altura = altura_janela
        self.largura = SIDEBAR_LARGURA
        self.cor_idx = 0
        self.ferramenta_ativa = "selecionar"   # ou "girar_esq", "transladar"...
        self._montar_botoes()

    def _montar_botoes(self):
        margem = 12
        tam = 40
        passo = tam + 8

        # --- secao 1: manipulacao (grade 2 colunas) ---
        # tipos: selecionar, girar_esq, girar_dir, aumentar, diminuir, transladar
        self.ferramentas_manip = []
        tipos_manip = ["selecionar", "girar_esq", "girar_dir",
                       "aumentar", "diminuir", "transladar"]
        y_topo = self.altura - margem - tam
        for i, tipo in enumerate(tipos_manip):
            col = i % 2
            lin = i // 2
            x = margem + col * (tam + 4)
            y = y_topo - lin * passo
            self.ferramentas_manip.append(
                BotaoFerramenta(tipo, x=x, y=y, tamanho=tam))

        # y da proxima secao
        linhas_manip = (len(tipos_manip) + 1) // 2
        y_apos_manip = y_topo - linhas_manip * passo - 20

        # --- secao 2: paleta de cores (grade 2 colunas) ---
        self.botoes_cor = []
        raio = 16
        espaco = 44
        for i, cor in enumerate(PALETA_CORES):
            col = i % 2
            lin = i // 2
            cx = margem + raio + col * espaco
            cy = y_apos_manip - raio - lin * espaco
            self.botoes_cor.append(BotaoCor(cor, cx, cy, raio))

        # --- secao 3: ferramentas de criacao ---
        self.ferramentas_criar = []
        tipos_criar = ["retangulo", "circulo", "triangulo",
                       "segmento", "poligono"]
        y_paleta_base = y_apos_manip - raio - (len(self.botoes_cor) // 2) * espaco
        y_apos_paleta = y_paleta_base - 20
        for i, tipo in enumerate(tipos_criar):
            y = y_apos_paleta - tam - i * passo
            self.ferramentas_criar.append(
                BotaoFerramenta(tipo, x=margem, y=y, tamanho=tam))

    # ----------------------------------------------------------------
    def processar_clique(self, x, y):
        """Retorna:
             ("ferramenta", tipo)   -> clicou em selecionar/manip/criar
             ("cor", indice)        -> clicou numa cor
             None                   -> clique fora da sidebar
        """
        if x >= self.largura:
            return None

        # manipulacao
        for b in self.ferramentas_manip:
            if b.contem(x, y):
                self.ferramenta_ativa = b.tipo
                return ("ferramenta", b.tipo)

        # cores
        for i, b in enumerate(self.botoes_cor):
            if b.contem(x, y):
                self.cor_idx = i
                return ("cor", i)

        # criacao
        for b in self.ferramentas_criar:
            if b.contem(x, y):
                self.ferramenta_ativa = b.tipo
                return ("ferramenta", b.tipo)

        return None

    def cor_atual(self):
        return PALETA_CORES[self.cor_idx]

    def resetar_ferramenta(self):
        """Volta para 'selecionar' (usado apos finalizar uma criacao)."""
        self.ferramenta_ativa = "selecionar"

    # ----------------------------------------------------------------
    def desenhar(self, batch, shapes_list):
        L = self.largura
        A = self.altura

        shapes_list.append(shapes.Rectangle(0, 0, L, A,
                                            color=COR_FUNDO_SIDEBAR,
                                            batch=batch))
        shapes_list.append(shapes.Line(L, 0, L, A,
                                       thickness=1,
                                       color=COR_BORDA_SIDEBAR,
                                       batch=batch))

        for b in self.ferramentas_manip:
            self._desenhar_botao(b, batch, shapes_list)
        for i, b in enumerate(self.botoes_cor):
            shapes_list.append(shapes.Circle(b.cx, b.cy, b.raio,
                                             color=b.cor_rgb, batch=batch))
            if i == self.cor_idx:
                shapes_list.append(shapes.Circle(b.cx, b.cy, b.raio + 3,
                                                 color=(0, 0, 0), batch=batch))
                shapes_list.append(shapes.Circle(b.cx, b.cy, b.raio + 1,
                                                 color=b.cor_rgb, batch=batch))
        for b in self.ferramentas_criar:
            self._desenhar_botao(b, batch, shapes_list)

    def _desenhar_botao(self, botao, batch, shapes_list):
        ativo = (botao.tipo == self.ferramenta_ativa)
        cor_fundo = COR_BOTAO_ATIVO if ativo else COR_BOTAO_INATIVO
        cor_icone = COR_ICONE_ATIVO if ativo else COR_ICONE_INATIVO

        shapes_list.append(shapes.Rectangle(
            botao.x, botao.y, botao.tamanho, botao.tamanho,
            color=cor_fundo, batch=batch))

        cx, cy = botao.centro()
        t = botao.tipo
        if t == "selecionar":
            self._icone_selecionar(cx, cy, cor_icone, batch, shapes_list)
        elif t == "girar_esq":
            self._icone_girar(cx, cy, cor_icone, batch, shapes_list, -1)
        elif t == "girar_dir":
            self._icone_girar(cx, cy, cor_icone, batch, shapes_list, +1)
        elif t == "aumentar":
            self._icone_zoom(cx, cy, cor_icone, batch, shapes_list, +1)
        elif t == "diminuir":
            self._icone_zoom(cx, cy, cor_icone, batch, shapes_list, -1)
        elif t == "transladar":
            self._icone_transladar(cx, cy, cor_icone, batch, shapes_list)
        elif t == "retangulo":
            self._icone_retangulo(cx, cy, cor_icone, batch, shapes_list)
        elif t == "circulo":
            self._icone_circulo(cx, cy, cor_icone, batch, shapes_list)
        elif t == "triangulo":
            self._icone_triangulo(cx, cy, cor_icone, batch, shapes_list)
        elif t == "segmento":
            self._icone_segmento(cx, cy, cor_icone, batch, shapes_list)
        elif t == "poligono":
            self._icone_poligono(cx, cy, cor_icone, batch, shapes_list)

    # ---------- ICONES ----------
    def _icone_selecionar(self, cx, cy, cor, batch, lst):
        lst.append(shapes.Polygon(
            (cx - 8, cy + 10),
            (cx + 8, cy + 6),
            (cx + 2, cy - 2),
            color=cor, batch=batch))
        lst.append(shapes.Polygon(
            (cx + 2, cy - 2),
            (cx + 8, cy + 6),
            (cx + 6, cy - 10),
            color=cor, batch=batch))

    def _icone_girar(self, cx, cy, cor, batch, lst, sentido):
        """Arco com seta — seta para -1 (esq) ou +1 (dir)."""
        pontos = []
        for i in range(9):
            ang = math.radians(60 + i * 30 * sentido)
            pontos.append((cx + 9 * math.cos(ang), cy + 9 * math.sin(ang)))
        lst.append(shapes.Line(pontos[0][0], pontos[0][1],
                               pontos[4][0], pontos[4][1],
                               thickness=2, color=cor, batch=batch))
        # ponta da seta no final do arco
        px, py = pontos[-1]
        lst.append(shapes.Circle(px, py, 3, color=cor, batch=batch))

    def _icone_zoom(self, cx, cy, cor, batch, lst, sinal):
        """Lupa com + ou -."""
        lst.append(shapes.Circle(cx - 2, cy + 2, 7,
                                 color=cor, batch=batch))
        lst.append(shapes.Line(cx + 4, cy - 4, cx + 9, cy - 9,
                               thickness=2, color=cor, batch=batch))
        # sinal + ou -
        if sinal > 0:
            lst.append(shapes.Line(cx - 6, cy + 2, cx + 2, cy + 2,
                                   thickness=1, color=(255, 255, 255),
                                   batch=batch))
        lst.append(shapes.Line(cx - 2, cy - 2, cx - 2, cy + 6,
                               thickness=1, color=(255, 255, 255),
                               batch=batch))

    def _icone_transladar(self, cx, cy, cor, batch, lst):
        """Cruz com quatro setas."""
        lst.append(shapes.Line(cx - 10, cy, cx + 10, cy,
                               thickness=2, color=cor, batch=batch))
        lst.append(shapes.Line(cx, cy - 10, cx, cy + 10,
                               thickness=2, color=cor, batch=batch))
        # pontas (4 circulos pequenos)
        for (dx, dy) in [(-10, 0), (10, 0), (0, -10), (0, 10)]:
            lst.append(shapes.Circle(cx + dx, cy + dy, 2.5,
                                     color=cor, batch=batch))

    def _icone_retangulo(self, cx, cy, cor, batch, lst):
        lst.append(shapes.Box(cx - 10, cy - 7, 20, 14,
                              thickness=2, color=cor, batch=batch))

    def _icone_circulo(self, cx, cy, cor, batch, lst):
        lst.append(shapes.Circle(cx, cy, 9, color=cor, batch=batch))

    def _icone_triangulo(self, cx, cy, cor, batch, lst):
        lst.append(shapes.Triangle(cx - 10, cy - 8,
                                   cx + 10, cy - 8,
                                   cx,      cy + 9,
                                   color=cor, batch=batch))

    def _icone_segmento(self, cx, cy, cor, batch, lst):
        lst.append(shapes.Line(cx - 9, cy - 8, cx + 9, cy + 8,
                               thickness=2, color=cor, batch=batch))
        lst.append(shapes.Circle(cx - 9, cy - 8, 3, color=cor, batch=batch))
        lst.append(shapes.Circle(cx + 9, cy + 8, 3, color=cor, batch=batch))

    def _icone_poligono(self, cx, cy, cor, batch, lst):
        """Estrela de 5 pontas."""
        pontos = []
        for i in range(10):
            ang = math.pi / 2 + i * math.pi / 5
            r = 10 if i % 2 == 0 else 4
            pontos.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        lst.append(shapes.Polygon(*pontos, color=cor, batch=batch))