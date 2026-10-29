"""
CCB0941 — Computacao Grafica | M3 — Editor 2D Interativo
=========================================================
Editor 2D com transformacoes homogeneas, criacao/selecao/manipulacao de
objetos, window<->viewport (zoom/pan) e recorte (Cohen-Sutherland e
Sutherland-Hodgman).

Controles:
  CRIAR:     P=poligono(Enter fecha)  C=circulo  T=triangulo  R=retangulo
  SELECIONAR: clique | Shift+clique | arrastar no vazio = laco
  MOVER:     setas=transladar  Q/E=girar  +/-=escalar  Shift+X/Y=escala 1 eixo
  Referencia: 1=centro  2=canto bbox  3=ponto clicado
  Gerais:    Del=remover  I=info  H=cor  G=preenchimento  F1=recorte  Esc=sai
  Camera:    scroll=zoom  botao do meio=pan
"""
import math

import numpy as np
import pyglet

pyglet.options.dpi_scaling = "stretch"
from pyglet import shapes
from pyglet.window import key, mouse
from pyglet import gl

from abaRecursos import Sidebar, SIDEBAR_LARGURA   # NOVO


# ======================================================================
# BLOCO 1 — JANELA E BATCH
# ======================================================================
LARGURA, ALTURA = 900, 600                      # janela um pouco mais larga
janela = pyglet.window.Window(LARGURA, ALTURA, caption="Editor 2D — M3")
pyglet.gl.glClearColor(0, 0, 0, 1)
batch = pyglet.graphics.Batch()

# area do mundo = janela MENOS sidebar
MUNDO_X0 = SIDEBAR_LARGURA
MUNDO_LARGURA = LARGURA - SIDEBAR_LARGURA



# ======================================================================
# BLOCO 2 — MATRIZES HOMOGENEAS 3x3
# Convencao: ponto = vetor coluna [x, y, 1]^T, resultado = M @ ponto
# ======================================================================
def matriz_identidade():
    return np.eye(3)


def matriz_translacao(tx, ty):
    """Translacao: [x,y,1] -> [x+tx, y+ty, 1]."""
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype=float)


def matriz_rotacao(theta_rad):
    """Rotacao anti-horaria em torno da origem."""
    c, s = math.cos(theta_rad), math.sin(theta_rad)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def matriz_escala(sx, sy):
    """Escala em torno da origem."""
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], dtype=float)


def matriz_em_torno_de(ponto, matriz_base):
    """T(p) @ M @ T(-p) — gira/escala em torno de um ponto `ponto`."""
    px, py = ponto
    return (matriz_translacao(px, py) @ matriz_base
            @ matriz_translacao(-px, -py))


def aplicar_matriz_em_pontos(pontos, matriz):
    """Aplica matriz 3x3 a lista de pontos 2D usando [x,y,1]."""
    if not pontos:
        return []
    pontos_h = np.array([[x, y, 1] for (x, y) in pontos]).T
    resultado = matriz @ pontos_h
    return [(float(px), float(py)) for (px, py, _) in resultado.T]


# ======================================================================
# BLOCO 3 — CAMERA (window <-> viewport)
# window_centro/half descrevem a regiao do MUNDO visivel.
# ======================================================================
# ======================================================================
# BLOCO 3 — CAMERA (window <-> viewport)
# window_centro/half descrevem a regiao do MUNDO visivel.
# O viewport do mundo e a area da tela a DIREITA da sidebar.
# ======================================================================
window_centro = np.array([MUNDO_LARGURA / 2, ALTURA / 2], dtype=float)
window_half = np.array([MUNDO_LARGURA / 2, ALTURA / 2], dtype=float)
ZOOM_MIN, ZOOM_MAX = 0.1, 10.0


def matriz_mundo_para_tela():
    """Mundo -> pixel, mapeando para a area do mundo (a direita da sidebar)."""
    sx = MUNDO_LARGURA / (2 * window_half[0])
    sy = ALTURA        / (2 * window_half[1])
    cx, cy = window_centro
    # centro do viewport do mundo = (MUNDO_X0 + MUNDO_LARGURA/2, ALTURA/2)
    return (matriz_translacao(MUNDO_X0 + MUNDO_LARGURA / 2, ALTURA / 2) @
            matriz_escala(sx, sy) @
            matriz_translacao(-cx, -cy))


def converter_tela_para_mundo(x_px, y_px):
    """Inversa: pixel -> mundo (para picking e criacao)."""
    sx = MUNDO_LARGURA / (2 * window_half[0])
    sy = ALTURA        / (2 * window_half[1])
    cx, cy = window_centro
    return ((x_px - MUNDO_X0 - MUNDO_LARGURA / 2) / sx + cx,
            (y_px - ALTURA / 2) / sy + cy)


# ======================================================================
# BLOCO 4 — UTILITARIOS DE GEOMETRIA (poligonos)
# ======================================================================
def ponto_dentro_do_poligono(ponto, vertices):
    """Ray casting: conta cruzamentos de um raio horizontal."""
    x, y = ponto
    dentro = False
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_int = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_int:
                dentro = not dentro
    return dentro


def calcular_area_poligono(vertices):
    """Formula do cadarco (shoelace)."""
    n = len(vertices)
    if n < 3:
        return 0.0
    soma = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        soma += x1 * y2 - x2 * y1
    return abs(soma) / 2


def calcular_perimetro_poligono(vertices):
    """Soma das distancias entre vertices consecutivos."""
    n = len(vertices)
    if n < 2:
        return 0.0
    soma = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        soma += math.hypot(x2 - x1, y2 - y1)
    return soma

def _distancia_ponto_segmento(px, py, x1, y1, x2, y2):
    """Distancia minima do ponto (px,py) ao segmento (x1,y1)-(x2,y2)."""
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)

# ======================================================================
# BLOCO 5 — RECORTE
# recorte_janela guarda o retangulo de recorte em coordenadas do MUNDO.
# ======================================================================
recorte_ativo = True
recorte_janela = (-LARGURA, -ALTURA, 2 * LARGURA, 2 * ALTURA)  # xmin,ymin,xmax,ymax


# --- 5.1 Cohen-Sutherland (segmentos) ---
def calcular_outcode(x, y, xmin, ymin, xmax, ymax):
    """Bits: 1=LEFT 2=RIGHT 4=BOTTOM 8=TOP."""
    codigo = 0
    if x < xmin: codigo |= 1
    if x > xmax: codigo |= 2
    if y < ymin: codigo |= 4
    if y > ymax: codigo |= 8
    return codigo


def recortar_segmento_cohen_sutherland(p1, p2, xmin, ymin, xmax, ymax):
    """Recorta segmento p1-p2. Retorna (q1, q2) ou None."""
    x1, y1 = p1
    x2, y2 = p2
    c1 = calcular_outcode(x1, y1, xmin, ymin, xmax, ymax)
    c2 = calcular_outcode(x2, y2, xmin, ymin, xmax, ymax)

    while True:
        if not (c1 | c2):
            return (x1, y1), (x2, y2)     # ambos dentro
        if c1 & c2:
            return None                    # ambos fora (mesmo lado)
        c = c1 if c1 else c2
        if c & 8:      # TOP
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1); y = ymax
        elif c & 4:    # BOTTOM
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1); y = ymin
        elif c & 2:    # RIGHT
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1); x = xmax
        else:          # LEFT
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1); x = xmin
        if c == c1:
            x1, y1 = x, y
            c1 = calcular_outcode(x1, y1, xmin, ymin, xmax, ymax)
        else:
            x2, y2 = x, y
            c2 = calcular_outcode(x2, y2, xmin, ymin, xmax, ymax)


# --- 5.2 Sutherland-Hodgman (poligonos) ---
def recortar_poligono_por_aresta(vertices, lado):
    """Recorta poligono contra UMA aresta da janela (L, R, B, T)."""
    if not vertices:
        return []
    xmin, ymin, xmax, ymax = recorte_janela

    def dentro(p):
        return {
            'L': p[0] >= xmin, 'R': p[0] <= xmax,
            'B': p[1] >= ymin, 'T': p[1] <= ymax,
        }[lado]

    def intersecao(a, b):
        ax, ay = a
        bx, by = b
        if lado == 'L':
            if bx == ax:
                return (xmin, ay)
            return (xmin, ay + (by - ay) * (xmin - ax) / (bx - ax))
        if lado == 'R':
            if bx == ax:
                return (xmax, ay)
            return (xmax, ay + (by - ay) * (xmax - ax) / (bx - ax))
        if lado == 'B':
            if by == ay:
                return (ax, ymin)
            return (ax + (bx - ax) * (ymin - ay) / (by - ay), ymin)
        # 'T'
        if by == ay:
            return (ax, ymax)
        return (ax + (bx - ax) * (ymax - ay) / (by - ay), ymax)

    saida = []
    n = len(vertices)
    for i in range(n):
        atual = vertices[i]
        anterior = vertices[i - 1]
        atual_dentro = dentro(atual)
        anterior_dentro = dentro(anterior)
        if atual_dentro:
            if not anterior_dentro:
                saida.append(intersecao(anterior, atual))
            saida.append(atual)
        elif anterior_dentro:
            saida.append(intersecao(anterior, atual))
    return saida


def recortar_poligono_sutherland_hodgman(vertices):
    """Aplica Sutherland-Hodgman nas 4 arestas da janela de recorte."""
    if not vertices:
        return []
    resultado = list(vertices)
    for lado in ('L', 'R', 'B', 'T'):
        resultado = recortar_poligono_por_aresta(resultado, lado)
        if not resultado:
            break
    return resultado


# ======================================================================
# BLOCO 6 — OBJETO 2D
# ======================================================================
class Objeto2D:
    """Objeto grafico: pontos locais + matriz acumulada + atributos visuais."""

    def __init__(self, pontos_locais, cor, tipo="poligono", preenchido=True):
        self.pontos_locais = list(pontos_locais)
        self.matriz = matriz_identidade()
        self.cor = cor
        self.tipo = tipo
        self.preenchido = preenchido
        self.circulo = None   # {'centro':(x,y), 'raio':r} quando tipo == 'circulo'

    # ---------- pipeline de coordenadas ----------
    def obter_pontos_mundo(self):
        return aplicar_matriz_em_pontos(self.pontos_locais, self.matriz)

    def obter_pontos_tela(self):
        return aplicar_matriz_em_pontos(self.obter_pontos_mundo(),
                                        matriz_mundo_para_tela())

    # ---------- bounding box e centro (em MUNDO) ----------
    def obter_bbox_mundo(self):
        pts = self.obter_pontos_mundo()
        if not pts:
            return (0, 0, 0, 0)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return (min(xs), min(ys), max(xs), max(ys))

    def obter_centro_mundo(self):
        x0, y0, x1, y1 = self.obter_bbox_mundo()
        return ((x0 + x1) / 2, (y0 + y1) / 2)

    # ---------- teste de selecao ----------
    def contem_ponto(self, wx, wy):
        if self.tipo == "circulo":
            cx, cy = aplicar_matriz_em_pontos([self.circulo["centro"]],
                                            self.matriz)[0]
            r = self.circulo["raio"] * math.sqrt(
                abs(np.linalg.det(self.matriz[:2, :2])))
            return (wx - cx) ** 2 + (wy - cy) ** 2 <= r * r
        if self.tipo == "segmento":
            # distancia ponto-segmento <= tolerancia
            pts = self.obter_pontos_mundo()
            if len(pts) < 2:
                return False
            (x1, y1), (x2, y2) = pts[0], pts[1]
            return _distancia_ponto_segmento(wx, wy, x1, y1, x2, y2) <= 8.0
        return ponto_dentro_do_poligono((wx, wy), self.obter_pontos_mundo())

    # ---------- propriedades ----------
    def obter_area_perimetro(self):
        if self.tipo == "circulo":
            r = self.circulo["raio"] * math.sqrt(
                abs(np.linalg.det(self.matriz[:2, :2])))
            return math.pi * r * r, 2 * math.pi * r
        if self.tipo == "segmento":
            pts = self.obter_pontos_mundo()
            if len(pts) >= 2:
                comprimento = math.hypot(pts[1][0] - pts[0][0],
                                        pts[1][1] - pts[0][1])
                return 0.0, comprimento   # area 0, "perimetro" = comprimento
            return 0.0, 0.0
        pts = self.obter_pontos_mundo()
        return calcular_area_poligono(pts), calcular_perimetro_poligono(pts)

    # ---------- manipulacao ----------
    def compor_matriz(self, matriz_elementar):
        """Convencao do scaffold: M <- nova @ M (a nova entra a esquerda)."""
        self.matriz = matriz_elementar @ self.matriz


# ======================================================================
# BLOCO 7 — ESTADO GLOBAL DO EDITOR
# ======================================================================
# ======================================================================
# BLOCO 7 — ESTADO GLOBAL DO EDITOR
# ======================================================================
objetos = []
selecionados = []

MODO_CRIAR_POLIGONO = "criar_poligono"
MODO_SELECIONAR = "selecionar"
MODO_MOVER = "mover"
MODO_CRIAR_SEGMENTO = "criar_segmento"
# NOVO: ferramentas vindas da sidebar
FERRAMENTA_RETANGULO = "retangulo"
FERRAMENTA_CIRCULO   = "circulo"
FERRAMENTA_TRIANGULO = "triangulo"
FERRAMENTA_SEGMENTO  = "segmento"
FERRAMENTA_POLIGONO  = "poligono"

# --- NOVOS MODOS de manipulacao (sidebar) ---
FERRAMENTA_GIRAR_ESQ  = "girar_esq"
FERRAMENTA_GIRAR_DIR  = "girar_dir"
FERRAMENTA_AUMENTAR   = "aumentar"
FERRAMENTA_DIMINUIR   = "diminuir"
FERRAMENTA_TRANSLADAR = "transladar"

# --- buffers de criacao multi-clique ---
retangulo_inicio = None    # 1o clique (pixel) do retangulo 2-cliques
triangulo_pontos = []      # lista de (x, y) em pixel

modo = MODO_SELECIONAR

# --- sidebar (novo) ---
sidebar = Sidebar(ALTURA)

# --- buffers de criacao (novo: "ferramenta pendente") ---
# Quando o usuario clica numa ferramenta da sidebar, guardamos aqui.
# O primeiro clique no mundo consome essa ferramenta.
ferramenta_pendente = None    # None | "retangulo" | "circulo" | "triangulo" | "segmento" | "poligono"

# --- estados de criacao ---
pontos_criacao = []              # poligono nao convexo em PIXEL
segmento_inicio = None           # 1o clique do segmento (em PIXEL)
circulo_inicio = None            # 1o clique do circulo (em PIXEL)
laco_inicio = None
laco_fim = None

ref_modo = 1
ref_ponto = (0, 0)

PASSO_TRANS = 15
PASSO_ROT = math.radians(10)
FATOR_ESC = 1.1

# paleta agora vem da sidebar
PALETA = [(240, 140, 40)]   # mantida para compat (nao usada quando ha sidebar)
paleta_idx = 0

shapes_list = []
label_info = pyglet.text.Label("", x=SIDEBAR_LARGURA + 8, y=ALTURA - 8,
                               anchor_y='top', font_size=10,
                               color=(255, 255, 255, 255))

GRADE_ESPACO = 50.0
GRADE_COR = (80, 80, 80)
GRADE_COR_EIXO = (0, 255, 0)
# ======================================================================
# BLOCO 8 — RENDERIZACAO
# ======================================================================
def desenhar_objeto(obj):
    """Pipeline: local -> matriz -> mundo -> recorte -> W2V -> pixel -> shape.

    - Poligono preenchido: recorta com Sutherland-Hodgman (poligono inteiro).
    - Poligono so contorno: recorta cada aresta com Cohen-Sutherland (segmento).
    - Circulo: recorte aproximado por bbox (tudo ou nada).
    """
    cor = obj.cor + (255,) if len(obj.cor) == 3 else obj.cor
    w2v = matriz_mundo_para_tela()
        # ---------- segmento ----------
    if obj.tipo == "segmento":
        pts_mundo = obj.obter_pontos_mundo()
        if len(pts_mundo) < 2:
            return
        a, b = pts_mundo[0], pts_mundo[1]
        if recorte_ativo:
            segmento = recortar_segmento_cohen_sutherland(
                a, b, *recorte_janela)
        else:
            segmento = (a, b)
        if segmento is None:
            return
        pa, pb = segmento
        pa_tela = aplicar_matriz_em_pontos([pa], w2v)[0]
        pb_tela = aplicar_matriz_em_pontos([pb], w2v)[0]
        shapes_list.append(shapes.Line(pa_tela[0], pa_tela[1],
                                       pb_tela[0], pb_tela[1],
                                       thickness=2, color=cor, batch=batch))
        return
    # ---------- circulo ----------
    if obj.tipo == "circulo":
        c_mundo = aplicar_matriz_em_pontos([obj.circulo["centro"]],
                                           obj.matriz)[0]
        r_mundo = obj.circulo["raio"] * math.sqrt(
            abs(np.linalg.det(obj.matriz[:2, :2])))
        if recorte_ativo:
            xmin, ymin, xmax, ymax = recorte_janela
            if (c_mundo[0] + r_mundo < xmin or c_mundo[0] - r_mundo > xmax or
                    c_mundo[1] + r_mundo < ymin or c_mundo[1] - r_mundo > ymax):
                return
        cx_px, cy_px = aplicar_matriz_em_pontos([c_mundo], w2v)[0]
        borda_mundo = (c_mundo[0] + r_mundo, c_mundo[1])
        bx_px, by_px = aplicar_matriz_em_pontos([borda_mundo], w2v)[0]
        r_px = math.hypot(bx_px - cx_px, by_px - cy_px)
        shapes_list.append(shapes.Circle(cx_px, cy_px, r_px,
                                         color=cor, batch=batch))
        return

    # ---------- poligonos ----------
    pts_mundo = obj.obter_pontos_mundo()

    # ----- MODO PREENCHIDO: Sutherland-Hodgman (recorta o poligono inteiro)
    if obj.preenchido:
        if recorte_ativo:
            pts_mundo = recortar_poligono_sutherland_hodgman(pts_mundo)
        if len(pts_mundo) < 3:
            return
        pts_tela = aplicar_matriz_em_pontos(pts_mundo, w2v)
        shapes_list.append(shapes.Polygon(*pts_tela, color=cor, batch=batch))
        return

    # ----- MODO SO CONTORNO: Cohen-Sutherland (recorta aresta por aresta)
    n = len(pts_mundo)
    for i in range(n):
        a = pts_mundo[i]
        b = pts_mundo[(i + 1) % n]

        if recorte_ativo:
            segmento = recortar_segmento_cohen_sutherland(
                a, b, *recorte_janela)
        else:
            segmento = (a, b)

        if segmento is None:
            continue
        pa, pb = segmento
        pa_tela = aplicar_matriz_em_pontos([pa], w2v)[0]
        pb_tela = aplicar_matriz_em_pontos([pb], w2v)[0]
        shapes_list.append(shapes.Line(pa_tela[0], pa_tela[1],
                                       pb_tela[0], pb_tela[1],
                                       thickness=2, color=cor, batch=batch))
def desenhar_grade():
    """Desenha a grade em coordenadas do MUNDO, convertida para a tela via W2V.

    So desenha as linhas que estao dentro do retangulo visivel (window),
    para nao gerar milhares de shapes quando o zoom esta afastado.
    """
    w2v = matriz_mundo_para_tela()

    # limites do mundo visivel (a "window" da camera)
    cx, cy = window_centro
    hw, hh = window_half
    xmin_mundo, xmax_mundo = cx - hw, cx + hw
    ymin_mundo, ymax_mundo = cy - hh, cy + hh

    # primeira linha vertical >= xmin_mundo
    x0 = math.floor(xmin_mundo / GRADE_ESPACO) * GRADE_ESPACO
    # ultima linha vertical <= xmax_mundo
    x1 = math.ceil(xmax_mundo / GRADE_ESPACO) * GRADE_ESPACO

    y0 = math.floor(ymin_mundo / GRADE_ESPACO) * GRADE_ESPACO
    y1 = math.ceil(ymax_mundo / GRADE_ESPACO) * GRADE_ESPACO

    # linhas verticais
    x = x0
    while x <= x1:
        # converte os dois extremos da linha (em mundo) para pixel
        (px_topo, py_topo), (px_base, py_base) = aplicar_matriz_em_pontos(
            [(x, ymin_mundo), (x, ymax_mundo)], w2v)
        cor = GRADE_COR_EIXO if abs(x) < 1e-6 else GRADE_COR
        shapes_list.append(shapes.Line(px_topo, py_topo, px_base, py_base,
                                       thickness=1, color=cor, batch=batch))
        x += GRADE_ESPACO

    # linhas horizontais
    y = y0
    while y <= y1:
        (px_esq, py_esq), (px_dir, py_dir) = aplicar_matriz_em_pontos(
            [(xmin_mundo, y), (xmax_mundo, y)], w2v)
        cor = GRADE_COR_EIXO if abs(y) < 1e-6 else GRADE_COR
        shapes_list.append(shapes.Line(px_esq, py_esq, px_dir, py_dir,
                                       thickness=1, color=cor, batch=batch))
        y += GRADE_ESPACO
        

def desenhar_hud():
    """Borda do recorte, laco de selecao, preview do poligono em criacao."""
    # borda da janela de recorte (em mundo -> tela)

        # preview do segmento em criacao
    if modo == MODO_CRIAR_SEGMENTO and segmento_inicio is not None:
        # pega a posicao atual do mouse (pyglet fornece via janela)
        mx, my = janela._mouse_x, janela._mouse_y
        shapes_list.append(shapes.Line(segmento_inicio[0], segmento_inicio[1],
                                       mx, my, thickness=1,
                                       color=(255, 255, 0), batch=batch))
    if recorte_ativo:
        xmin, ymin, xmax, ymax = recorte_janela
        w2v = matriz_mundo_para_tela()
        cantos = aplicar_matriz_em_pontos(
            [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)], w2v)
        for i in range(4):
            a = cantos[i]
            b = cantos[(i + 1) % 4]
            shapes_list.append(shapes.Line(a[0], a[1], b[0], b[1],
                                           thickness=1, color=(90, 90, 120),
                                           batch=batch))

    # laco de selecao
    if laco_inicio and laco_fim:
        x0, y0 = laco_inicio
        x1, y1 = laco_fim
        shapes_list.append(shapes.Rectangle(min(x0, x1), min(y0, y1),
                                            abs(x1 - x0), abs(y1 - y0),
                                            color=(80, 120, 200, 60),
                                            batch=batch))

    # preview do poligono em criacao
    if pontos_criacao:
        for p in pontos_criacao:
            shapes_list.append(shapes.Circle(p[0], p[1], 3,
                                             color=(255, 255, 255),
                                             batch=batch))
        for i in range(len(pontos_criacao) - 1):
            a = pontos_criacao[i]
            b = pontos_criacao[i + 1]
            shapes_list.append(shapes.Line(a[0], a[1], b[0], b[1],
                                           thickness=1, color=(255, 255, 0),
                                           batch=batch))


def desenhar_bbox_selecionados():
    """Bounding box amarela em volta dos selecionados (em MUNDO -> tela)."""
    w2v = matriz_mundo_para_tela()
    for obj in selecionados:
        x0, y0, x1, y1 = obj.obter_bbox_mundo()
        (px0, py0), (px1, py1) = aplicar_matriz_em_pontos(
            [(x0, y0), (x1, y1)], w2v)
        esquerda = min(px0, px1)
        base = min(py0, py1)
        largura = abs(px1 - px0)
        altura = abs(py1 - py0)
        shapes_list.append(shapes.Box(esquerda, base, largura, altura,
                              thickness=2, color=(255, 140, 0),   # laranja
                              batch=batch))


def texto_status():
    """Linha de status no topo da tela."""
    estado_recorte = "ON" if recorte_ativo else "OFF"
    if selecionados:
        area, perim = selecionados[0].obter_area_perimetro()
        return (f"Modo: {modo} | sel: {len(selecionados)} | "
                f"area={area:.1f} perim={perim:.1f} | ref={ref_modo} "
                f"| recorte={estado_recorte} | H=cor G=fill I=info")
    return   (f"Modo: {modo} | obj: {len(objetos)} | ref={ref_modo} "
            f"| recorte={estado_recorte} | L=segmento H=cor G=fill I=info")


# ======================================================================
# BLOCO 8 — RENDERIZACAO
# ======================================================================
# ... (desenhar_objeto permanece igual) ...

def desenhar_preview_criacao():
    """Preview das ferramentas pendentes (2 cliques ou N cliques)."""
    mx, my = janela._mouse_x, janela._mouse_y

    # circulo: linha do centro ate o cursor
    if ferramenta_pendente == "circulo" and circulo_inicio is not None:
        shapes_list.append(shapes.Line(circulo_inicio[0], circulo_inicio[1],
                                       mx, my, thickness=1,
                                       color=(255, 255, 0), batch=batch))
        shapes_list.append(shapes.Circle(mx, my, 3,
                                         color=(255, 255, 0), batch=batch))

    # segmento
    if ferramenta_pendente == "segmento" and segmento_inicio is not None:
        shapes_list.append(shapes.Line(segmento_inicio[0], segmento_inicio[1],
                                       mx, my, thickness=1,
                                       color=(255, 255, 0), batch=batch))

    # retangulo: 1o canto fixo, 2o segue o cursor
    if ferramenta_pendente == "retangulo" and retangulo_inicio is not None:
        x0, y0 = retangulo_inicio
        shapes_list.append(shapes.Line(x0, y0, mx, y0, thickness=1,
                                       color=(255, 255, 0), batch=batch))
        shapes_list.append(shapes.Line(mx, y0, mx, my, thickness=1,
                                       color=(255, 255, 0), batch=batch))
        shapes_list.append(shapes.Line(mx, my, x0, my, thickness=1,
                                       color=(255, 255, 0), batch=batch))
        shapes_list.append(shapes.Line(x0, my, x0, y0, thickness=1,
                                       color=(255, 255, 0), batch=batch))

    # triangulo: 2 pontos fixos + cursor formando o 3o
    if ferramenta_pendente == "triangulo" and triangulo_pontos:
        pts_preview = triangulo_pontos + [(mx, my)]
        for i in range(len(pts_preview) - 1):
            a = pts_preview[i]
            b = pts_preview[i + 1]
            shapes_list.append(shapes.Line(a[0], a[1], b[0], b[1],
                                           thickness=1,
                                           color=(255, 255, 0), batch=batch))
        if len(triangulo_pontos) == 2:
            a = triangulo_pontos[0]
            shapes_list.append(shapes.Line(mx, my, a[0], a[1],
                                           thickness=1,
                                           color=(255, 255, 0), batch=batch))
        for p in triangulo_pontos:
            shapes_list.append(shapes.Circle(p[0], p[1], 3,
                                             color=(255, 255, 255),
                                             batch=batch))

    # poligono (caminho antigo e sidebar)
    if ferramenta_pendente == "poligono" and pontos_criacao:
        for p in pontos_criacao:
            shapes_list.append(shapes.Circle(p[0], p[1], 3,
                                             color=(255, 255, 255),
                                             batch=batch))
        for i in range(len(pontos_criacao) - 1):
            a = pontos_criacao[i]
            b = pontos_criacao[i + 1]
            shapes_list.append(shapes.Line(a[0], a[1], b[0], b[1],
                                           thickness=1,
                                           color=(255, 255, 0), batch=batch))


def atualizar_tela():
    """Reconstroi todos os shapes (do zero) e o HUD."""
    global shapes_list
    for shape in shapes_list:
        shape.delete()
    shapes_list = []

    desenhar_grade()

    for obj in objetos:
        desenhar_objeto(obj)

    desenhar_hud()
    desenhar_preview_criacao()      # NOVO: previews de criacao
    desenhar_bbox_selecionados()

    sidebar.desenhar(batch, shapes_list)   # NOVO: sidebar por cima do mundo

    label_info.text = texto_status()


# ======================================================================
# BLOCO 9 — MANIPULACAO DOS SELECIONADOS
# ======================================================================
def aplicar_matriz_nos_selecionados(matriz_elementar, referencia=None):
    """Compoe a matriz elementar em cada selecionado (opcionalmente em torno
    de um ponto de referencia)."""
    for obj in selecionados:
        if referencia is None:
            obj.compor_matriz(matriz_elementar)
        else:
            obj.compor_matriz(matriz_em_torno_de(referencia, matriz_elementar))


def resolver_ponto_referencia(obj):
    """1=centro do objeto, 2=canto do bbox, 3=ponto clicado."""
    if ref_modo == 1:
        return obj.obter_centro_mundo()
    if ref_modo == 2:
        x0, y0, _, _ = obj.obter_bbox_mundo()
        return (x0, y0)
    return ref_ponto


# ======================================================================
# BLOCO 10 — CRIACAO DE OBJETOS (todos no centro da window)
# ======================================================================
# ======================================================================
# BLOCO 10 — CRIACAO DE OBJETOS
# ======================================================================
def criar_circulo_por_centro_e_raio(centro_mundo, ponto_borda_mundo):
    """Cria circulo a partir de centro + ponto na borda (raio = distancia)."""
    global modo
    r = math.hypot(ponto_borda_mundo[0] - centro_mundo[0],
                   ponto_borda_mundo[1] - centro_mundo[1])
    if r < 1e-6:
        return
    obj = Objeto2D([], sidebar.cor_atual(), tipo="circulo")
    obj.circulo = {"centro": (0.0, 0.0), "raio": r}
    obj.matriz = matriz_translacao(centro_mundo[0], centro_mundo[1])
    objetos.append(obj)
    modo = MODO_SELECIONAR
    sidebar.resetar_ferramenta()       # <-- ADICIONAR

    atualizar_tela()


def criar_retangulo_em(ponto_mundo):
    """Retangulo 100x60 centrado no ponto clicado."""
    global modo
    locais = [(-50, -30), (50, -30), (50, 30), (-50, 30)]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="retangulo")
    obj.matriz = matriz_translacao(ponto_mundo[0], ponto_mundo[1])
    objetos.append(obj)
    modo = MODO_SELECIONAR
    sidebar.resetar_ferramenta()       # <-- ADICIONAR
    atualizar_tela()
def criar_retangulo_2cliques(p1_pixel, p2_pixel):
    """Retangulo delimitado por 2 cantos dados em PIXEL."""
    global modo
    a = converter_tela_para_mundo(*p1_pixel)
    b = converter_tela_para_mundo(*p2_pixel)
    xmin, xmax = min(a[0], b[0]), max(a[0], b[0])
    ymin, ymax = min(a[1], b[1]), max(a[1], b[1])
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    locais = [(xmin - cx, ymin - cy), (xmax - cx, ymin - cy),
              (xmax - cx, ymax - cy), (xmin - cx, ymax - cy)]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="retangulo")
    obj.matriz = matriz_translacao(cx, cy)
    objetos.append(obj)
    modo = MODO_SELECIONAR
    sidebar.resetar_ferramenta()       # <-- desliga o azul do botao
    atualizar_tela()


def criar_triangulo_3cliques(pontos_pixel):
    """Triangulo a partir de 3 vertices dados em PIXEL."""
    global modo
    pts_mundo = [converter_tela_para_mundo(x, y) for (x, y) in pontos_pixel]
    cx = sum(p[0] for p in pts_mundo) / 3
    cy = sum(p[1] for p in pts_mundo) / 3
    locais = [(x - cx, y - cy) for (x, y) in pts_mundo]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="triangulo")
    obj.matriz = matriz_translacao(cx, cy)
    objetos.append(obj)
    modo = MODO_SELECIONAR
    sidebar.resetar_ferramenta()       # <-- ADICIONAR
    sidebar.resetar_ferramenta()
    atualizar_tela()

def criar_triangulo_em(ponto_mundo):
    """Triangulo centrado no ponto clicado."""
    global modo
    locais = [(-50, -30), (50, -30), (0, 50)]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="triangulo")
    obj.matriz = matriz_translacao(ponto_mundo[0], ponto_mundo[1])
    objetos.append(obj)
    sidebar.resetar_ferramenta()       # <-- ADICIONAR
    modo = MODO_SELECIONAR
    atualizar_tela()


def criar_segmento(inicio_mundo, fim_mundo):
    """Cria um segmento entre dois pontos em MUNDO."""
    global modo
    cx = (inicio_mundo[0] + fim_mundo[0]) / 2
    cy = (inicio_mundo[1] + fim_mundo[1]) / 2
    locais = [
        (inicio_mundo[0] - cx, inicio_mundo[1] - cy),
        (fim_mundo[0] - cx,    fim_mundo[1] - cy),
    ]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="segmento")
    obj.matriz = matriz_translacao(cx, cy)
    objetos.append(obj)
    sidebar.resetar_ferramenta()       # <-- ADICIONAR
    modo = MODO_SELECIONAR
    atualizar_tela()


def finalizar_criacao_poligono():
    """Fecha o poligono: converte pontos de pixel para mundo e normaliza."""
    global pontos_criacao, modo,ferramenta_pendente
    if len(pontos_criacao) >= 3:
        pts_mundo = [converter_tela_para_mundo(x, y)
                     for (x, y) in pontos_criacao]
        cx = sum(p[0] for p in pts_mundo) / len(pts_mundo)
        cy = sum(p[1] for p in pts_mundo) / len(pts_mundo)
        locais = [(x - cx, y - cy) for (x, y) in pts_mundo]
        obj = Objeto2D(locais, sidebar.cor_atual(), tipo="poligono")
        obj.matriz = matriz_translacao(cx, cy)
        objetos.append(obj)
    pontos_criacao = []
    modo = MODO_SELECIONAR
    atualizar_tela()


# ======================================================================
# BLOCO 11 — EVENTOS DE MOUSE
# ======================================================================
# ======================================================================
# BLOCO 11 — EVENTOS DE MOUSE
# ======================================================================
@janela.event
def on_mouse_press(x, y, button, modifiers):
    global modo, laco_inicio, laco_fim, ref_ponto, selecionados
    global segmento_inicio, circulo_inicio, ferramenta_pendente, pontos_criacao
    global retangulo_inicio, triangulo_pontos

    # --- 1) SIDEBAR tem prioridade ---
    if button == mouse.LEFT and x < SIDEBAR_LARGURA:
        evento = sidebar.processar_clique(x, y)
        if evento is not None:
            tipo_evento, valor = evento
            if tipo_evento == "ferramenta":
                if valor == "selecionar":
                    modo = MODO_SELECIONAR
                    ferramenta_pendente = None
                else:
                    # qualquer ferramenta da sidebar ativa "pendente"
                    ferramenta_pendente = valor
                # zera buffers de criacao ao trocar de ferramenta
                pontos_criacao = []
                segmento_inicio = None
                circulo_inicio = None
                retangulo_inicio = None
                triangulo_pontos = []
            atualizar_tela()
            return
        return

    # --- 2) PAN (botao do meio) ---
    if button == mouse.MIDDLE:
        janela._pan_ant = (x, y)
        return

    # --- 3) NOVA DINAMICA: ferramenta pendente consome o clique no mundo ---
       # --- 3) FERRAMENTA PENDENTE consome o clique no mundo ---
    if button == mouse.LEFT and ferramenta_pendente is not None:
        wx, wy = converter_tela_para_mundo(x, y)

        # --- botoes de manipulacao (nao criam, agem sobre selecionados) ---
        if ferramenta_pendente == "girar_esq":
            aplicar_matriz_nos_selecionados(matriz_rotacao(+PASSO_ROT))
            sidebar.resetar_ferramenta()
            ferramenta_pendente = None
            atualizar_tela()
            return
        if ferramenta_pendente == "girar_dir":
            aplicar_matriz_nos_selecionados(matriz_rotacao(-PASSO_ROT))
            sidebar.resetar_ferramenta()
            ferramenta_pendente = None
            atualizar_tela()
            return
        if ferramenta_pendente == "aumentar":
            aplicar_matriz_nos_selecionados(
                matriz_escala(FATOR_ESC, FATOR_ESC))
            sidebar.resetar_ferramenta()
            ferramenta_pendente = None
            atualizar_tela()
            return
        if ferramenta_pendente == "diminuir":
            aplicar_matriz_nos_selecionados(
                matriz_escala(1/FATOR_ESC, 1/FATOR_ESC))
            sidebar.resetar_ferramenta()
            ferramenta_pendente = None
            atualizar_tela()
            return
        if ferramenta_pendente == "transladar":
            # transladar segue o cursor enquanto arrasta; usa 1 clique simples
            # como translação de PASSO_TRANS na direcao do clique em relacao
            # ao centro dos selecionados
            if selecionados:
                cxs = sum(o.obter_centro_mundo()[0] for o in selecionados) / len(selecionados)
                cys = sum(o.obter_centro_mundo()[1] for o in selecionados) / len(selecionados)
                dx = wx - cxs
                dy = wy - cys
                aplicar_matriz_nos_selecionados(matriz_translacao(dx, dy))
            sidebar.resetar_ferramenta()
            ferramenta_pendente = None
            atualizar_tela()
            return

        # --- retangulo: 2 cliques (extremos) ---
        if ferramenta_pendente == "retangulo":
            if retangulo_inicio is None:
                retangulo_inicio = (x, y)
            else:
                criar_retangulo_2cliques(retangulo_inicio, (x, y))
                retangulo_inicio = None
                ferramenta_pendente = None
            atualizar_tela()
            return

        # --- triangulo: 3 cliques ---
        if ferramenta_pendente == "triangulo":
            triangulo_pontos.append((x, y))
            if len(triangulo_pontos) == 3:
                criar_triangulo_3cliques(triangulo_pontos)
                triangulo_pontos = []
                ferramenta_pendente = None
            atualizar_tela()
            return

        # --- circulo: 2 cliques (centro + borda) ---
        if ferramenta_pendente == "circulo":
            if circulo_inicio is None:
                circulo_inicio = (x, y)
            else:
                centro_mundo = converter_tela_para_mundo(*circulo_inicio)
                criar_circulo_por_centro_e_raio(centro_mundo, (wx, wy))
                circulo_inicio = None
                ferramenta_pendente = None
            atualizar_tela()
            return

        # --- segmento: 2 cliques ---
        if ferramenta_pendente == "segmento":
            if segmento_inicio is None:
                segmento_inicio = (x, y)
            else:
                inicio_mundo = converter_tela_para_mundo(*segmento_inicio)
                criar_segmento(inicio_mundo, (wx, wy))
                segmento_inicio = None
                ferramenta_pendente = None
            atualizar_tela()
            return

        # --- poligono: N cliques + Enter ---
        if ferramenta_pendente == "poligono":
            pontos_criacao.append((x, y))
            atualizar_tela()
            return

    # --- 4) Comportamento antigo (modo do teclado) ---
    if modo == MODO_CRIAR_POLIGONO and button == mouse.LEFT:
        pontos_criacao.append((x, y))
        atualizar_tela()
        return

    if modo == MODO_CRIAR_SEGMENTO and button == mouse.LEFT:
        if segmento_inicio is None:
            segmento_inicio = (x, y)
        else:
            inicio_mundo = converter_tela_para_mundo(*segmento_inicio)
            fim_mundo = converter_tela_para_mundo(x, y)
            criar_segmento(inicio_mundo, fim_mundo)
            segmento_inicio = None
        atualizar_tela()
        return

    if modo == MODO_SELECIONAR and button == mouse.LEFT:
        wx, wy = converter_tela_para_mundo(x, y)
        alvo = None
        for obj in reversed(objetos):
            if obj.contem_ponto(wx, wy):
                alvo = obj
                break
        shift = bool(modifiers & key.MOD_SHIFT)
        if alvo is None:
            laco_inicio = (x, y)
            laco_fim = (x, y)
            if not shift:
                selecionados = []
        else:
            if shift:
                if alvo in selecionados:
                    selecionados.remove(alvo)
                else:
                    selecionados.append(alvo)
            else:
                selecionados = [alvo]
        atualizar_tela()
        return

    if modo == MODO_MOVER and button == mouse.LEFT and ref_modo == 3:
        wx, wy = converter_tela_para_mundo(x, y)
        ref_ponto = (wx, wy)

@janela.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    global laco_fim
    if button == mouse.MIDDLE:
        ax, ay = janela._pan_ant
        dwx, dwy = converter_tela_para_mundo(ax, ay)
        nwx, nwy = converter_tela_para_mundo(x, y)
        window_centro[0] += (dwx - nwx)
        window_centro[1] += (dwy - nwy)
        janela._pan_ant = (x, y)
        atualizar_tela()
        return
    if modo == MODO_SELECIONAR and laco_inicio is not None:
        laco_fim = (x, y)
        atualizar_tela()


@janela.event
def on_mouse_release(x, y, button, modifiers):
    global laco_inicio, laco_fim, selecionados
    if button == mouse.MIDDLE:
        return
    if modo == MODO_SELECIONAR and laco_inicio is not None:
        x0, y0 = laco_inicio
        x1, y1 = laco_fim
        pxmin, pxmax = min(x0, x1), max(x0, x1)
        pymin, pymax = min(y0, y1), max(y0, y1)
        w2v = matriz_mundo_para_tela()
        novos = []
        for obj in objetos:
            cx, cy = obj.obter_centro_mundo()
            (pcx, pcy), = aplicar_matriz_em_pontos([(cx, cy)], w2v)
            if pxmin <= pcx <= pxmax and pymin <= pcy <= pymax:
                novos.append(obj)
        if novos:
            if modifiers & key.MOD_SHIFT:
                for obj in novos:
                    if obj not in selecionados:
                        selecionados.append(obj)
            else:
                selecionados = novos
        laco_inicio = None
        laco_fim = None
        atualizar_tela()


@janela.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    """Zoom: multiplica half_w/half_h pelo mesmo fator (mantem aspecto)."""
    global window_half
    fator = 1.1 ** (-scroll_y)
    novo = window_half * fator
    if LARGURA / (2 * novo[0]) > ZOOM_MAX or LARGURA / (2 * novo[0]) < ZOOM_MIN:
        return
    window_half = novo
    atualizar_tela()
@janela.event
def on_mouse_motion(x, y, dx, dy):
    janela._mouse_x = x
    janela._mouse_y = y
    if modo == MODO_CRIAR_SEGMENTO and segmento_inicio is not None:
        atualizar_tela()

# ======================================================================
# BLOCO 12 — EVENTOS DE TECLADO
# ======================================================================
@janela.event
def on_key_press(simbolo, modifiers):
    global modo, pontos_criacao, selecionados, segmento_inicio
    global ref_modo, recorte_ativo, paleta_idx, ferramenta_pendente
    global triangulo_pontos, retangulo_inicio, circulo_inicio

    K = key

    # --- modos ---
    if simbolo == K.P:
        modo = MODO_CRIAR_POLIGONO
        pontos_criacao = []
        atualizar_tela()
        return
    if simbolo == K.C:
        criar_circulo_no_centro(); return
    if simbolo == K.T:
        criar_triangulo_no_centro(); return
    if simbolo == K.R and modo != MODO_MOVER:
        criar_retangulo_no_centro(); return
    if simbolo == K.S:
        modo = MODO_SELECIONAR
        pontos_criacao = []
        atualizar_tela(); return
    if simbolo == K.M:
        modo = MODO_MOVER
        atualizar_tela(); return
    #Segmento
    if simbolo == K.L:
        modo = MODO_CRIAR_SEGMENTO
        segmento_inicio = None
        atualizar_tela()
        return
    # --- fechar poligono em criacao ---
    # --- fechar poligono em criacao (teclado OU sidebar) ---
    # --- Enter: fecha poligono OU triangulo (se 3 pontos ja foram dados) ---
    if simbolo == K.ENTER:
        if ferramenta_pendente == "poligono" and len(pontos_criacao) >= 3:
            finalizar_criacao_poligono()
            ferramenta_pendente = None
            sidebar.resetar_ferramenta()
            return
        if ferramenta_pendente == "triangulo" and len(triangulo_pontos) == 3:
            criar_triangulo_3cliques(triangulo_pontos)
            triangulo_pontos = []
            ferramenta_pendente = None
            return
        if modo == MODO_CRIAR_POLIGONO and len(pontos_criacao) >= 3:
            finalizar_criacao_poligono()
            return

   

    # --- referencia de rotacao/escala ---
    if simbolo in (K._1, K._2, K._3):
        ref_modo = {K._1: 1, K._2: 2, K._3: 3}[simbolo]
        atualizar_tela(); return

    # --- recorte on/off ---
    if simbolo == K.F1:
        recorte_ativo = not recorte_ativo
        atualizar_tela(); return

    # --- cor (cicla paleta) ---
    if simbolo == K.H:
        paleta_idx = (paleta_idx + 1) % len(PALETA)
        for obj in selecionados:
            obj.cor = PALETA[paleta_idx]
        atualizar_tela(); return

    # --- preenchimento ---
    if simbolo == K.G:
        for obj in selecionados:
            obj.preenchido = not obj.preenchido
        atualizar_tela(); return

    # --- info ---
    if simbolo == K.I:
        for obj in selecionados:
            a, p = obj.obter_area_perimetro()
            print(f"[{obj.tipo}] area={a:.2f} perim={p:.2f}")
        return

    # --- remover ---
    if simbolo == K.DELETE:
        for obj in selecionados:
            if obj in objetos:
                objetos.remove(obj)
        selecionados = []
        atualizar_tela(); return
    

    # --- manipulacao (transladar/girar/escalar) ---
    if modo == MODO_MOVER and selecionados:
        if simbolo == K.LEFT:
            aplicar_matriz_nos_selecionados(matriz_translacao(-PASSO_TRANS, 0))
        elif simbolo == K.RIGHT:
            aplicar_matriz_nos_selecionados(matriz_translacao(PASSO_TRANS, 0))
        elif simbolo == K.UP:
            aplicar_matriz_nos_selecionados(matriz_translacao(0, PASSO_TRANS))
        elif simbolo == K.DOWN:
            aplicar_matriz_nos_selecionados(matriz_translacao(0, -PASSO_TRANS))
        elif simbolo == K.Q:
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                aplicar_matriz_nos_selecionados(matriz_rotacao(PASSO_ROT), ref)
        elif simbolo == K.E:
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                aplicar_matriz_nos_selecionados(matriz_rotacao(-PASSO_ROT), ref)
        elif simbolo in (K.PLUS, K.EQUAL):
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                aplicar_matriz_nos_selecionados(
                    matriz_escala(FATOR_ESC, FATOR_ESC), ref)
        elif simbolo == K.MINUS:
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                aplicar_matriz_nos_selecionados(
                    matriz_escala(1 / FATOR_ESC, 1 / FATOR_ESC), ref)
        elif simbolo == K.X and (modifiers & key.MOD_SHIFT):
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                aplicar_matriz_nos_selecionados(matriz_escala(FATOR_ESC, 1.0), ref)
        elif simbolo == K.Y and (modifiers & key.MOD_SHIFT):
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                aplicar_matriz_nos_selecionados(matriz_escala(1.0, FATOR_ESC), ref)
        atualizar_tela()
        return

     # --- Esc: cancela criacao em andamento ---
    if simbolo == K.ESCAPE:
                ferramenta_pendente = None
                pontos_criacao = []
                segmento_inicio = None
                circulo_inicio = None
                retangulo_inicio = None
                triangulo_pontos = []
                sidebar.resetar_ferramenta()
                modo = MODO_SELECIONAR
                atualizar_tela()
                return

# ======================================================================
# BLOCO 13 — DRAW E MAIN
# ======================================================================
@janela.event
def on_draw():
    janela.clear()
    batch.draw()
    label_info.draw()

if __name__ == "__main__":
    pyglet.app.run()