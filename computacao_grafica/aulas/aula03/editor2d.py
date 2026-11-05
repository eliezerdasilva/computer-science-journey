"""
CCB0941 — Computacao Grafica | M3 — Editor 2D Interativo
=========================================================
Editor 2D com transformacoes homogeneas, criacao/selecao/manipulacao de
objetos, window<->viewport (zoom/pan) e recorte (Cohen-Sutherland e
Sutherland-Hodgman).

Controles:
  CRIAR (teclado): P=poligono(Enter fecha)  C=circulo  T=triangulo
                   R=retangulo  L=segmento
  CRIAR (sidebar): clique no botao -> clique no mundo
  SELECIONAR:      clique | Shift+clique | arrastar no vazio = laco
  MOVER:           setas=transladar  Q/E=girar  +/-=escalar
  Referencia:      1=centro  2=canto bbox  3=ponto clicado
  Gerais:          Del=remover  I=info  H=cor  G=preenchimento
                   F1=recorte  Esc=cancela  Esc duas vezes=sai
  Camera:          scroll=zoom  botao do meio=pan
"""

import math

import numpy as np
import pyglet

pyglet.options.dpi_scaling = "stretch"
from pyglet import shapes
from pyglet.window import key, mouse

from abaRecursos import Sidebar, SIDEBAR_LARGURA


# ======================================================================
# BLOCO 1 — JANELA E BATCH
# ======================================================================
# Descobre a resolucao do monitor principal
tela = pyglet.display.get_display().get_default_screen()
LARGURA, ALTURA = tela.width, tela.height

janela = pyglet.window.Window(LARGURA, ALTURA,
                              caption="Editor 2D — M3",
                              fullscreen=True)
pyglet.gl.glClearColor(0, 0, 0, 1)
batch = pyglet.graphics.Batch()
batch_grade = pyglet.graphics.Batch()

MUNDO_X0 = SIDEBAR_LARGURA
MUNDO_LARGURA = LARGURA - SIDEBAR_LARGURA


# ======================================================================
# BLOCO 2 — MATRIZES HOMOGENEAS 3x3
# ======================================================================
def matriz_identidade():
    return np.eye(3)


def matriz_translacao(tx, ty):
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype=float)


def matriz_rotacao(theta_rad):
    c, s = math.cos(theta_rad), math.sin(theta_rad)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def matriz_escala(sx, sy):
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], dtype=float)


def matriz_em_torno_de(ponto, matriz_base):
    px, py = ponto
    return (matriz_translacao(px, py) @ matriz_base
            @ matriz_translacao(-px, -py))


def aplicar_matriz_em_pontos(pontos, matriz):
    if not pontos:
        return []
    pontos_h = np.array([[x, y, 1] for (x, y) in pontos]).T
    resultado = matriz @ pontos_h
    return [(float(px), float(py)) for (px, py, _) in resultado.T]


# ======================================================================
# BLOCO 3 — CAMERA (window <-> viewport)
# ======================================================================
window_centro = np.array([MUNDO_LARGURA / 2, ALTURA / 2], dtype=float)
window_half = np.array([MUNDO_LARGURA / 2, ALTURA / 2], dtype=float)
ZOOM_MIN, ZOOM_MAX = 0.1, 10.0


def matriz_mundo_para_tela():
    sx = MUNDO_LARGURA / (2 * window_half[0])
    sy = ALTURA / (2 * window_half[1])
    cx, cy = window_centro
    return (matriz_translacao(MUNDO_X0 + MUNDO_LARGURA / 2, ALTURA / 2) @
            matriz_escala(sx, sy) @
            matriz_translacao(-cx, -cy))


def converter_tela_para_mundo(x_px, y_px):
    sx = MUNDO_LARGURA / (2 * window_half[0])
    sy = ALTURA / (2 * window_half[1])
    cx, cy = window_centro
    return ((x_px - MUNDO_X0 - MUNDO_LARGURA / 2) / sx + cx,
            (y_px - ALTURA / 2) / sy + cy)


# ======================================================================
# BLOCO 4 — GEOMETRIA
# ======================================================================
def ponto_dentro_do_poligono(ponto, vertices):
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
# ======================================================================
recorte_ativo = True
recorte_janela = (-LARGURA, -ALTURA, 2 * LARGURA, 2 * ALTURA)


def calcular_outcode(x, y, xmin, ymin, xmax, ymax):
    codigo = 0
    if x < xmin: codigo |= 1
    if x > xmax: codigo |= 2
    if y < ymin: codigo |= 4
    if y > ymax: codigo |= 8
    return codigo


def recortar_segmento_cohen_sutherland(p1, p2, xmin, ymin, xmax, ymax):
    x1, y1 = p1
    x2, y2 = p2
    c1 = calcular_outcode(x1, y1, xmin, ymin, xmax, ymax)
    c2 = calcular_outcode(x2, y2, xmin, ymin, xmax, ymax)

    while True:
        if not (c1 | c2):
            return (x1, y1), (x2, y2)
        if c1 & c2:
            return None
        c = c1 if c1 else c2
        if c & 8:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1); y = ymax
        elif c & 4:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1); y = ymin
        elif c & 2:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1); x = xmax
        else:
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1); x = xmin
        if c == c1:
            x1, y1 = x, y
            c1 = calcular_outcode(x1, y1, xmin, ymin, xmax, ymax)
        else:
            x2, y2 = x, y
            c2 = calcular_outcode(x2, y2, xmin, ymin, xmax, ymax)


def recortar_poligono_por_aresta(vertices, lado):
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
    def __init__(self, pontos_locais, cor, tipo="poligono", preenchido=True):
        self.pontos_locais = list(pontos_locais)
        self.matriz = matriz_identidade()
        self.cor = cor
        self.tipo = tipo
        self.preenchido = preenchido
        self.circulo = None

    def obter_pontos_mundo(self):
        return aplicar_matriz_em_pontos(self.pontos_locais, self.matriz)

    def obter_pontos_tela(self):
        return aplicar_matriz_em_pontos(self.obter_pontos_mundo(),
                                        matriz_mundo_para_tela())

    def obter_bbox_mundo(self):
        if self.tipo == "circulo":
            cx, cy = aplicar_matriz_em_pontos([self.circulo["centro"]],
                                              self.matriz)[0]
            r = self.circulo["raio"] * math.sqrt(
                abs(np.linalg.det(self.matriz[:2, :2])))
            return (cx - r, cy - r, cx + r, cy + r)
        pts = self.obter_pontos_mundo()
        if not pts:
            return (0, 0, 0, 0)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return (min(xs), min(ys), max(xs), max(ys))

    def obter_centro_mundo(self):
        x0, y0, x1, y1 = self.obter_bbox_mundo()
        return ((x0 + x1) / 2, (y0 + y1) / 2)

    def contem_ponto(self, wx, wy, tolerancia=0.0):
        if self.tipo == "circulo":
            cx, cy = aplicar_matriz_em_pontos([self.circulo["centro"]],
                                              self.matriz)[0]
            det = abs(np.linalg.det(self.matriz[:2, :2]))
            r = self.circulo["raio"] * math.sqrt(det)
            return (wx - cx) ** 2 + (wy - cy) ** 2 <= (r + tolerancia) ** 2
        if self.tipo == "segmento":
            pts = self.obter_pontos_mundo()
            if len(pts) < 2:
                return False
            (x1, y1), (x2, y2) = pts[0], pts[1]
            return _distancia_ponto_segmento(wx, wy, x1, y1, x2, y2) <= 8.0 + tolerancia
        return ponto_dentro_do_poligono((wx, wy), self.obter_pontos_mundo())

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
                return 0.0, comprimento
            return 0.0, 0.0
        pts = self.obter_pontos_mundo()
        return calcular_area_poligono(pts), calcular_perimetro_poligono(pts)

    def compor_matriz(self, matriz_elementar):
        self.matriz = matriz_elementar @ self.matriz


# ======================================================================
# BLOCO 7 — ESTADO GLOBAL
# ======================================================================
objetos = []
selecionados = []

MODO_CRIAR_POLIGONO = "criar_poligono"
MODO_SELECIONAR = "selecionar"
MODO_MOVER = "mover"
MODO_CRIAR_SEGMENTO = "criar_segmento"
modo = MODO_SELECIONAR

sidebar = Sidebar(ALTURA)

ferramenta_pendente = None
pontos_criacao = []
segmento_inicio = None
circulo_inicio = None
retangulo_inicio = None
triangulo_pontos = []

laco_inicio = None
laco_fim = None

ref_modo = 1
ref_ponto = (0, 0)

PASSO_TRANS = 15
PASSO_ROT = math.radians(10)
FATOR_ESC = 1.1

PALETA = [(240, 140, 40)]
paleta_idx = 0

grade_shapes = []
grade_cache_key = None

shapes_list = []
label_info = pyglet.text.Label("", x=SIDEBAR_LARGURA + 8, y=ALTURA - 8,
                               anchor_y='top', font_size=10,
                               color=(255, 255, 255, 255))

GRADE_ESPACO = 50.0
GRADE_COR = (80, 80, 80)
GRADE_COR_EIXO = (0, 255, 0)

janela._mouse_x = 0
janela._mouse_y = 0
janela._pan_ant = (0, 0)


# ======================================================================
# BLOCO 8 — RENDERIZACAO
# ======================================================================
def desenhar_objeto(obj):
    cor = obj.cor + (255,) if len(obj.cor) == 3 else obj.cor
    w2v = matriz_mundo_para_tela()

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

    pts_mundo = obj.obter_pontos_mundo()

    if obj.preenchido:
        if recorte_ativo:
            pts_mundo = recortar_poligono_sutherland_hodgman(pts_mundo)
        if len(pts_mundo) < 3:
            return
        pts_tela = aplicar_matriz_em_pontos(pts_mundo, w2v)
        shapes_list.append(shapes.Polygon(*pts_tela, color=cor, batch=batch))
        return

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
    """Grade em batch separado, com cache por (cx, cy, hw, hh)."""
    global grade_shapes, grade_cache_key

    chave = (window_centro[0], window_centro[1],
             window_half[0], window_half[1])

    if grade_cache_key == chave:
        return

    for s in grade_shapes:
        s.delete()
    grade_shapes = []

    w2v = matriz_mundo_para_tela()
    cx, cy = window_centro
    hw, hh = window_half
    xmin_mundo, xmax_mundo = cx - hw, cx + hw
    ymin_mundo, ymax_mundo = cy - hh, cy + hh

    x0 = math.floor(xmin_mundo / GRADE_ESPACO) * GRADE_ESPACO
    x1 = math.ceil(xmax_mundo / GRADE_ESPACO) * GRADE_ESPACO
    y0 = math.floor(ymin_mundo / GRADE_ESPACO) * GRADE_ESPACO
    y1 = math.ceil(ymax_mundo / GRADE_ESPACO) * GRADE_ESPACO

    x = x0
    while x <= x1:
        (px1, py1), (px2, py2) = aplicar_matriz_em_pontos(
            [(x, ymin_mundo), (x, ymax_mundo)], w2v)
        cor = GRADE_COR_EIXO if abs(x) < 1e-6 else GRADE_COR
        grade_shapes.append(shapes.Line(px1, py1, px2, py2,
                                        thickness=1, color=cor,
                                        batch=batch_grade))
        x += GRADE_ESPACO

    y = y0
    while y <= y1:
        (px1, py1), (px2, py2) = aplicar_matriz_em_pontos(
            [(xmin_mundo, y), (xmax_mundo, y)], w2v)
        cor = GRADE_COR_EIXO if abs(y) < 1e-6 else GRADE_COR
        grade_shapes.append(shapes.Line(px1, py1, px2, py2,
                                        thickness=1, color=cor,
                                        batch=batch_grade))
        y += GRADE_ESPACO

    grade_cache_key = chave


def desenhar_hud():
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

    if laco_inicio and laco_fim:
        x0, y0 = laco_inicio
        x1, y1 = laco_fim
        shapes_list.append(shapes.Rectangle(min(x0, x1), min(y0, y1),
                                            abs(x1 - x0), abs(y1 - y0),
                                            color=(80, 120, 200, 60),
                                            batch=batch))


def desenhar_preview_criacao():
    mx, my = janela._mouse_x, janela._mouse_y

    if ferramenta_pendente == "circulo" and circulo_inicio is not None:
        shapes_list.append(shapes.Line(circulo_inicio[0], circulo_inicio[1],
                                       mx, my, thickness=1,
                                       color=(255, 255, 0), batch=batch))
        shapes_list.append(shapes.Circle(mx, my, 3,
                                         color=(255, 255, 0), batch=batch))

    if ferramenta_pendente == "segmento" and segmento_inicio is not None:
        shapes_list.append(shapes.Line(segmento_inicio[0], segmento_inicio[1],
                                       mx, my, thickness=1,
                                       color=(255, 255, 0), batch=batch))

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

    if modo == MODO_CRIAR_SEGMENTO and segmento_inicio is not None:
        shapes_list.append(shapes.Line(segmento_inicio[0], segmento_inicio[1],
                                       mx, my, thickness=1,
                                       color=(255, 255, 0), batch=batch))


def desenhar_bbox_selecionados():
    w2v = matriz_mundo_para_tela()
    for obj in selecionados:
        x0, y0, x1, y1 = obj.obter_bbox_mundo()
        (px0, py0), (px1, py1) = aplicar_matriz_em_pontos(
            [(x0, y0), (x1, y1)], w2v)
        shapes_list.append(shapes.Box(min(px0, px1), min(py0, py1),
                                      abs(px1 - px0), abs(py1 - py0),
                                      thickness=2, color=(255, 140, 0),
                                      batch=batch))


def texto_status():
    estado = "ON" if recorte_ativo else "OFF"
    if selecionados:
        a, p = selecionados[0].obter_area_perimetro()
        return (f"Modo: {modo} | sel: {len(selecionados)} | "
                f"area={a:.1f} perim={p:.1f} | ref={ref_modo} "
                f"| recorte={estado}")
    return (f"Modo: {modo} | obj: {len(objetos)} | ref={ref_modo} "
            f"| recorte={estado}")


def atualizar_tela():
    global shapes_list
    for s in shapes_list:
        s.delete()
    shapes_list = []

    desenhar_grade()
    for obj in objetos:
        desenhar_objeto(obj)
    desenhar_hud()
    desenhar_preview_criacao()
    desenhar_bbox_selecionados()
    sidebar.desenhar(batch, shapes_list)
    label_info.text = texto_status()


# ======================================================================
# BLOCO 9 — MANIPULACAO DOS SELECIONADOS
# ======================================================================
def aplicar_matriz_nos_selecionados(matriz_elementar, referencia=None):
    for obj in selecionados:
        if referencia is None:
            obj.compor_matriz(matriz_elementar)
        else:
            obj.compor_matriz(matriz_em_torno_de(referencia, matriz_elementar))


def resolver_ponto_referencia(obj):
    if ref_modo == 1:
        return obj.obter_centro_mundo()
    if ref_modo == 2:
        x0, y0, _, _ = obj.obter_bbox_mundo()
        return (x0, y0)
    return ref_ponto


# ======================================================================
# BLOCO 10 — CRIACAO DE OBJETOS
# ======================================================================
def criar_circulo_por_centro_e_raio(centro_mundo, ponto_borda_mundo):
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
    sidebar.resetar_ferramenta()
    atualizar_tela()


def criar_retangulo_em(ponto_mundo):
    global modo
    locais = [(-50, -30), (50, -30), (50, 30), (-50, 30)]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="retangulo")
    obj.matriz = matriz_translacao(ponto_mundo[0], ponto_mundo[1])
    objetos.append(obj)
    modo = MODO_SELECIONAR
    sidebar.resetar_ferramenta()
    atualizar_tela()


def criar_retangulo_2cliques(p1_pixel, p2_pixel):
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
    sidebar.resetar_ferramenta()
    atualizar_tela()


def criar_triangulo_3cliques(pontos_pixel):
    global modo
    pts_mundo = [converter_tela_para_mundo(x, y) for (x, y) in pontos_pixel]
    cx = sum(p[0] for p in pts_mundo) / 3
    cy = sum(p[1] for p in pts_mundo) / 3
    locais = [(x - cx, y - cy) for (x, y) in pts_mundo]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="triangulo")
    obj.matriz = matriz_translacao(cx, cy)
    objetos.append(obj)
    modo = MODO_SELECIONAR
    sidebar.resetar_ferramenta()
    atualizar_tela()


def criar_triangulo_em(ponto_mundo):
    global modo
    locais = [(-50, -30), (50, -30), (0, 50)]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="triangulo")
    obj.matriz = matriz_translacao(ponto_mundo[0], ponto_mundo[1])
    objetos.append(obj)
    modo = MODO_SELECIONAR
    sidebar.resetar_ferramenta()
    atualizar_tela()


def criar_segmento(inicio_mundo, fim_mundo):
    global modo
    cx = (inicio_mundo[0] + fim_mundo[0]) / 2
    cy = (inicio_mundo[1] + fim_mundo[1]) / 2
    locais = [
        (inicio_mundo[0] - cx, inicio_mundo[1] - cy),
        (fim_mundo[0] - cx, fim_mundo[1] - cy),
    ]
    obj = Objeto2D(locais, sidebar.cor_atual(), tipo="segmento")
    obj.matriz = matriz_translacao(cx, cy)
    objetos.append(obj)
    modo = MODO_SELECIONAR
    sidebar.resetar_ferramenta()
    atualizar_tela()


def finalizar_criacao_poligono():
    global pontos_criacao, modo, ferramenta_pendente
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
    ferramenta_pendente = None
    sidebar.resetar_ferramenta()
    atualizar_tela()


def criar_circulo_no_centro():
    global modo
    c = (window_centro[0], window_centro[1])
    criar_circulo_por_centro_e_raio(c, (c[0] + 40, c[1]))
    modo = MODO_SELECIONAR
    atualizar_tela()


def criar_triangulo_no_centro():
    global modo
    criar_triangulo_em((window_centro[0], window_centro[1]))
    modo = MODO_SELECIONAR
    atualizar_tela()


def criar_retangulo_no_centro():
    global modo
    criar_retangulo_em((window_centro[0], window_centro[1]))
    modo = MODO_SELECIONAR
    atualizar_tela()


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
                    ferramenta_pendente = valor
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

    # --- 3) FERRAMENTA PENDENTE consome o clique no mundo ---
    if button == mouse.LEFT and ferramenta_pendente is not None:
        wx, wy = converter_tela_para_mundo(x, y)

        # --- 3.1) BOTOES DE MANIPULACAO (matrizes homogeneas em torno da ref) ---
        if ferramenta_pendente in ("girar_esq", "girar_dir", "aumentar",
                                   "diminuir", "transladar"):
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                if ferramenta_pendente == "girar_esq":
                    obj.compor_matriz(
                        matriz_em_torno_de(ref, matriz_rotacao(+PASSO_ROT)))
                elif ferramenta_pendente == "girar_dir":
                    obj.compor_matriz(
                        matriz_em_torno_de(ref, matriz_rotacao(-PASSO_ROT)))
                elif ferramenta_pendente == "aumentar":
                    obj.compor_matriz(
                        matriz_em_torno_de(
                            ref, matriz_escala(FATOR_ESC, FATOR_ESC)))
                elif ferramenta_pendente == "diminuir":
                    obj.compor_matriz(
                        matriz_em_torno_de(
                            ref, matriz_escala(1/FATOR_ESC, 1/FATOR_ESC)))
                elif ferramenta_pendente == "transladar":
                    obj.compor_matriz(
                        matriz_em_torno_de(
                            ref, matriz_translacao(wx - ref[0], wy - ref[1])))
            sidebar.resetar_ferramenta()
            ferramenta_pendente = None
            atualizar_tela()
            return

        # --- 3.2) RETANGULO: 2 cliques ---
        if ferramenta_pendente == "retangulo":
            if retangulo_inicio is None:
                retangulo_inicio = (x, y)
            else:
                criar_retangulo_2cliques(retangulo_inicio, (x, y))
                retangulo_inicio = None
                ferramenta_pendente = None
            atualizar_tela()
            return

        # --- 3.3) TRIANGULO: 3 cliques ---
        if ferramenta_pendente == "triangulo":
            triangulo_pontos.append((x, y))
            if len(triangulo_pontos) == 3:
                criar_triangulo_3cliques(triangulo_pontos)
                triangulo_pontos = []
                ferramenta_pendente = None
            atualizar_tela()
            return

        # --- 3.4) CIRCULO: 2 cliques ---
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

        # --- 3.5) SEGMENTO: 2 cliques ---
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

        # --- 3.6) POLIGONO: N cliques + Enter ---
        if ferramenta_pendente == "poligono":
            pontos_criacao.append((x, y))
            atualizar_tela()
            return

    # --- 4) COMPORTAMENTO ANTIGO (modo do teclado) ---
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
        sx = MUNDO_LARGURA / (2 * window_half[0])
        tol = 4.0 / sx if sx > 0 else 0.0

        alvo = None
        for obj in reversed(objetos):
            if obj.contem_ponto(wx, wy, tol):
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
    global window_half
    fator = 1.1 ** (-scroll_y)
    novo = window_half * fator
    if MUNDO_LARGURA / (2 * novo[0]) > ZOOM_MAX:
        return
    if MUNDO_LARGURA / (2 * novo[0]) < ZOOM_MIN:
        return
    window_half = novo
    atualizar_tela()


@janela.event
def on_mouse_motion(x, y, dx, dy):
    janela._mouse_x = x
    janela._mouse_y = y
    precisa = (
        (ferramenta_pendente == "circulo" and circulo_inicio is not None)
        or (ferramenta_pendente == "segmento" and segmento_inicio is not None)
        or (ferramenta_pendente == "retangulo" and retangulo_inicio is not None)
        or (ferramenta_pendente == "triangulo" and len(triangulo_pontos) >= 1)
        or (ferramenta_pendente == "poligono" and len(pontos_criacao) >= 1)
        or (modo == MODO_CRIAR_SEGMENTO and segmento_inicio is not None)
    )
    if precisa:
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

    if simbolo == K.P:
        modo = MODO_CRIAR_POLIGONO
        pontos_criacao = []
        atualizar_tela()
        return
    if simbolo == K.C:
        criar_circulo_no_centro()
        return
    if simbolo == K.T:
        criar_triangulo_no_centro()
        return
    if simbolo == K.R and modo != MODO_MOVER:
        criar_retangulo_no_centro()
        return
    if simbolo == K.S:
        modo = MODO_SELECIONAR
        pontos_criacao = []
        atualizar_tela()
        return
    if simbolo == K.M:
        modo = MODO_MOVER
        atualizar_tela()
        return
    if simbolo == K.L:
        modo = MODO_CRIAR_SEGMENTO
        segmento_inicio = None
        atualizar_tela()
        return

    if simbolo == K.ENTER:
        if ferramenta_pendente == "poligono" and len(pontos_criacao) >= 3:
            finalizar_criacao_poligono()
            return
        if ferramenta_pendente == "triangulo" and len(triangulo_pontos) == 3:
            criar_triangulo_3cliques(triangulo_pontos)
            triangulo_pontos = []
            ferramenta_pendente = None
            return
        if modo == MODO_CRIAR_POLIGONO and len(pontos_criacao) >= 3:
            finalizar_criacao_poligono()
            return

    if simbolo in (K._1, K._2, K._3):
        ref_modo = {K._1: 1, K._2: 2, K._3: 3}[simbolo]
        atualizar_tela()
        return

    if simbolo == K.F1:
        recorte_ativo = not recorte_ativo
        atualizar_tela()
        return

    if simbolo == K.H:
        paleta_idx = (paleta_idx + 1) % len(PALETA)
        for obj in selecionados:
            obj.cor = PALETA[paleta_idx]
        atualizar_tela()
        return

    if simbolo == K.G:
        for obj in selecionados:
            obj.preenchido = not obj.preenchido
        atualizar_tela()
        return

    if simbolo == K.I:
        for obj in selecionados:
            a, p = obj.obter_area_perimetro()
            print(f"[{obj.tipo}] area={a:.2f} perim={p:.2f}")
        return

    if simbolo == K.DELETE:
        for obj in selecionados:
            if obj in objetos:
                objetos.remove(obj)
        selecionados = []
        atualizar_tela()
        return

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
                obj.compor_matriz(
                    matriz_em_torno_de(ref, matriz_rotacao(PASSO_ROT)))
        elif simbolo == K.E:
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                obj.compor_matriz(
                    matriz_em_torno_de(ref, matriz_rotacao(-PASSO_ROT)))
        elif simbolo in (K.PLUS, K.EQUAL):
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                obj.compor_matriz(
                    matriz_em_torno_de(ref, matriz_escala(FATOR_ESC, FATOR_ESC)))
        elif simbolo == K.MINUS:
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                obj.compor_matriz(
                    matriz_em_torno_de(ref,
                                       matriz_escala(1/FATOR_ESC, 1/FATOR_ESC)))
        elif simbolo == K.X and (modifiers & key.MOD_SHIFT):
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                obj.compor_matriz(
                    matriz_em_torno_de(ref, matriz_escala(FATOR_ESC, 1.0)))
        elif simbolo == K.Y and (modifiers & key.MOD_SHIFT):
            for obj in selecionados:
                ref = resolver_ponto_referencia(obj)
                obj.compor_matriz(
                    matriz_em_torno_de(ref, matriz_escala(1.0, FATOR_ESC)))
        atualizar_tela()
        return

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
    batch_grade.draw()
    batch.draw()
    label_info.draw()


if __name__ == "__main__":
    pyglet.app.run()