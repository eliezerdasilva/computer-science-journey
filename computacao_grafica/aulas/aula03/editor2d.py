"""
CCB0941 — Computacao Grafica | M3 — Editor 2D Interativo
=========================================================
Projeto: editor 2D com transformacoes homogeneas, criacao/ selecao/manipulacao
de objetos, window<->viewport, zoom/pan e recorte (Cohen-Sutherland e
Sutherland-Hodgman).

Controles (resumo — detalhes no README.md):
  MODO CRIAR:       P=poligono  C=circulo  T=triangulo  R=retangulo  ESC=cancela
  MODO SELECIONAR:  clique=seleciona  Shift+clique=multi  Laco=arrasta no vazio
  MODO MOVER:       setas transladam  (+/-) escala  Q/E rotaciona
  Referencia:       1=centro  2=canto bbox  3=ponto clicado (roda/escala)
  Teclas gerais:    Del=remove  R=reset transform  I=info(area/perimetro)
                    Zoom: scroll  Pan: botao do meio / Shift+arrastar
                    Recorte: F1 alterna on/off   H=cor   G=preenchimento
                    ESC=sai
"""

import math

import numpy as np
import pyglet

pyglet.options.dpi_scaling = "stretch"
from pyglet import shapes
from pyglet.window import key, mouse


# ======================================================================
# PASSO 0 — JANELA E BATCH
# ======================================================================
LARGURA, ALTURA = 800, 600
janela = pyglet.window.Window(LARGURA, ALTURA, caption="Editor 2D — M3")
batch = pyglet.graphics.Batch()


# ======================================================================
# PASSO 0 — MATRIZES HOMOGENEAS 3x3 (convencao: p' = M @ p, coluna)
# ======================================================================
def matriz_identidade():
    return np.eye(3)


def matriz_translacao(tx, ty):
    """Translacao: [x,y,1] -> [x+tx, y+ty, 1]."""
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype=float)


def matriz_rotacao(theta_rad):
    """Rotacao anti-horaria em torno da origem (TODO 1)."""
    c, s = math.cos(theta_rad), math.sin(theta_rad)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def matriz_escala(sx, sy):
    """Escala em torno da origem (TODO 2)."""
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], dtype=float)


def aplicar_transformacao(pontos, matriz):
    """Aplica matriz 3x3 a lista de pontos 2D (vetor homogeneo [x,y,1])."""
    if not pontos:
        return []
    pts_h = np.array([[x, y, 1] for (x, y) in pontos]).T
    res = matriz @ pts_h
    return [(float(px), float(py)) for (px, py, _) in res.T]


# ======================================================================
# PASSO 0 — TRANSFORMACAO EM TORNO DE UM PONTO p (usada em rot/escala)
# ======================================================================
def matriz_em_torno_de(ponto, matriz):
    """MT(p) @ M @ MT(-p) — gira/escala em torno de `ponto` (requisito)."""
    px, py = ponto
    return (matriz_translacao(px, py) @ matriz
            @ matriz_translacao(-px, -py))


# ======================================================================
# PASSO WINDOW<->VIEWPORT — matriz de mapeamento do mundo para a tela
# ======================================================================
# A "window" e a regiao do MUNDO visivel; o "viewport" e a tela (pixels).
# Guardamos a window em variaveis (cx, cy = centro em mundo; half_w, half_h =
# metades); zoom multiplica half_w/half_h, pan muda (cx, cy).
window_centro = np.array([LARGURA / 2, ALTURA / 2], dtype=float)
window_half = np.array([LARGURA / 2, ALTURA / 2], dtype=float)   # 1:1 inicial
ZOOM_MIN, ZOOM_MAX = 0.1, 10.0


def matriz_window_para_viewport():
    """Mundo -> pixel da janela. Preserva razao de aspecto (sem deformar).

    Escala sx = LARGURA / (2*half_w), sy = ALTURA / (2*half_h). Para o zoom
    nao deformar, half_w/half_h devem manter a mesma razao de LARGURA/ALTURA;
    garantimos isso em `aplicar_zoom`.
    """
    sx = LARGURA / (2 * window_half[0])
    sy = ALTURA / (2 * window_half[1])
    cx, cy = window_centro
    # Mapeia mundo (cx,cy) para o centro do viewport e escala:
    #   x_px = sx*(x - cx) + LARGURA/2
    return (matriz_translacao(LARGURA / 2, ALTURA / 2) @
            matriz_escala(sx, sy) @
            matriz_translacao(-cx, -cy))


def viewport_para_mundo(x_px, y_px):
    """Inversa da matriz acima: pixel -> mundo (necessaria para criar objetos)."""
    sx = LARGURA / (2 * window_half[0])
    sy = ALTURA / (2 * window_half[1])
    cx, cy = window_centro
    wx = (x_px - LARGURA / 2) / sx + cx
    wy = (y_px - ALTURA / 2) / sy + cy
    return wx, wy


# ======================================================================
# PASSO OBJETOS — classe base dos objetos graficos
# ======================================================================
class Objeto2D:
    """Cada objeto guarda pontos locais + matriz acumulada (comeca identidade)."""

    def __init__(self, pontos_locais, cor, tipo="poligono", preenchido=True):
        self.pontos_locais = list(pontos_locais)
        self.matriz = matriz_identidade()
        self.cor = cor
        self.tipo = tipo            # 'poligono' | 'circulo' | 'triangulo' | 'retangulo'
        self.preenchido = preenchido
        # Para circulo: guarda centro e raio em coordenadas LOCAIS.
        self.circulo = None         # dict {'centro':(x,y), 'raio':r} ou None

    # -- pipeline: local -> acumulada -> window->viewport -> pixels
    def pontos_mundo(self):
        return aplicar_transformacao(self.pontos_locais, self.matriz)

    def pontos_tela(self):
        w2v = matriz_window_para_viewport()
        return aplicar_transformacao(self.pontos_mundo(), w2v)

    # bounding box no MUNDO (para referencia de rotacao/escala e laço)
    def bbox_mundo(self):
        pts = self.pontos_mundo()
        if not pts:
            return (0, 0, 0, 0)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return (min(xs), min(ys), max(xs), max(ys))

    def centro_mundo(self):
        x0, y0, x1, y1 = self.bbox_mundo()
        return ((x0 + x1) / 2, (y0 + y1) / 2)

    # ------------------------------------------------------------------
    # PASSO SELECAO — teste "ponto caiu dentro?" (em coordenadas de MUNDO)
    # ------------------------------------------------------------------
    def contem(self, wx, wy):
        if self.tipo == "circulo":
            cx, cy = aplicar_transformacao([self.circulo["centro"]], self.matriz)[0]
            # raio efetivo: media dos eixos da matriz (escala uniforme esperada)
            r = self.circulo["raio"] * math.sqrt(abs(np.linalg.det(self.matriz[:2, :2])))
            return (wx - cx) ** 2 + (wy - cy) ** 2 <= r * r
        return _ponto_em_poligono((wx, wy), self.pontos_mundo())

    # ------------------------------------------------------------------
    # PASSO PROPRIEDADES — area e perimetro
    # ------------------------------------------------------------------
    def area_perimetro(self):
        if self.tipo == "circulo":
            r = self.circulo["raio"] * math.sqrt(abs(np.linalg.det(self.matriz[:2, :2])))
            return math.pi * r * r, 2 * math.pi * r
        pts = self.pontos_mundo()
        return _area_shoelace(pts), _perimetro(pts)

    # ------------------------------------------------------------------
    # PASSO MANIPULACAO — compoe matrizes 3x3 (nunca edita pontos)
    # ------------------------------------------------------------------
    def aplicar(self, matriz_elementar):
        """Convencao herdada do scaffold: M <- nova @ M (nova a esquerda)."""
        self.matriz = matriz_elementar @ self.matriz


def _ponto_em_poligono(p, pts):
    """Ray casting: conta cruzamentos de um raio horizontal com as arestas."""
    x, y = p
    dentro = False
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        if ((y1 > y) != (y2 > y)):
            xint = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xint:
                dentro = not dentro
    return dentro


def _area_shoelace(pts):
    """Formula do cadarco: area com sinal; retorna valor absoluto."""
    n = len(pts)
    if n < 3:
        return 0.0
    s = 0.0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def _perimetro(pts):
    n = len(pts)
    if n < 2:
        return 0.0
    s = 0.0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        s += math.hypot(x2 - x1, y2 - y1)
    return s


# ======================================================================
# PASSO RECORTE — Cohen-Sutherland (segmentos) e Sutherland-Hodgman (polig.)
# ======================================================================
# Janela de recorte em coordenadas do MUNDO (retangulo). Editavel.
recorte_on = True
recorte_janela = (-LARGURA, -ALTURA, 2 * LARGURA, 2 * ALTURA)  # xmin,ymin,xmax,ymax


def cs_outcode(x, y, xmin, ymin, xmax, ymax):
    """Outcode de Cohen-Sutherland: bits LEFT/RIGHT/BOTTOM/TOP."""
    cod = 0
    if x < xmin: cod |= 1        # LEFT
    if x > xmax: cod |= 2        # RIGHT
    if y < ymin: cod |= 4        # BOTTOM
    if y > ymax: cod |= 8        # TOP
    return cod


def cohen_sutherland(p1, p2, xmin, ymin, xmax, ymax):
    """Recorta segmento p1-p2 contra retangulo; retorna (q1,q2) ou None."""
    x1, y1 = p1
    x2, y2 = p2
    c1 = cs_outcode(x1, y1, xmin, ymin, xmax, ymax)
    c2 = cs_outcode(x2, y2, xmin, ymin, xmax, ymax)
    while True:
        if not (c1 | c2):
            return (x1, y1), (x2, y2)        # trivialmente dentro
        if c1 & c2:
            return None                       # trivialmente fora
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
            c1 = cs_outcode(x1, y1, xmin, ymin, xmax, ymax)
        else:
            x2, y2 = x, y
            c2 = cs_outcode(x2, y2, xmin, ymin, xmax, ymax)


def _clip_poligono_aresta(pts, lado):
    """Um passo de Sutherland-Hodgman: recorta contra uma aresta (lado)."""
    if not pts:
        return []
    xmin, ymin, xmax, ymax = recorte_janela
    dentro = lambda p: {
        'L': p[0] >= xmin, 'R': p[0] <= xmax,
        'B': p[1] >= ymin, 'T': p[1] <= ymax,
    }[lado]
    intersec = lambda a, b: {
        'L': (xmin, a[1] + (b[1] - a[1]) * (xmin - a[0]) / (b[0] - a[0])),
        'R': (xmax, a[1] + (b[1] - a[1]) * (xmax - a[0]) / (b[0] - a[0])),
        'B': (a[0] + (b[0] - a[0]) * (ymin - a[1]) / (b[1] - a[1]), ymin),
        'T': (a[0] + (b[0] - a[0]) * (ymax - a[1]) / (b[1] - a[1]), ymax),
    }[lado]
    out = []
    for i in range(len(pts)):
        cur, prev = pts[i], pts[i - 1]
        if dentro(cur):
            if not dentro(prev):
                out.append(intersec(prev, cur))
            out.append(cur)
        elif dentro(prev):
            out.append(intersec(prev, cur))
    return out


def sutherland_hodgman(pts):
    """Recorta poligono contra a janela retangular (4 arestas)."""
    if not pts:
        return []
    res = list(pts)
    for lado in ('L', 'R', 'B', 'T'):
        res = _clip_poligono_aresta(res, lado)
        if not res:
            break
    return res


# ======================================================================
# ESTADO GERAL — objetos, selecao, modo
# ======================================================================
objetos = []
selecionados = []

MODO_CRIAR_POLIGONO = "criar_poligono"
MODO_SELECIONAR     = "selecionar"
MODO_MOVER          = "mover"
MODO_LACO           = "laco"
modo = MODO_SELECIONAR

# buffers de criacao
criando_poligono = False
pontos_criacao = []          # em MUNDO
# buffer do laco
laco_inicio = None
laco_fim = None

# referencia de rotacao/escala: 1=centro 2=canto bbox 3=ponto clicado
ref_modo = 1
ref_ponto = (0, 0)

# parametros de teclado
PASSO_TRANS = 15
PASSO_ROT = math.radians(10)
FATOR_ESC = 1.1

# cores pre-configuradas (H cicla)
PALETA = [(240, 140, 40), (60, 180, 240), (120, 220, 120),
          (230, 90, 120), (200, 160, 240)]
paleta_idx = 0

# shapes pyglet reconstruidos a cada frame
shapes_list = []
# texto HUD
label_info = pyglet.text.Label("", x=8, y=ALTURA - 8, anchor_y='top',
                               font_size=10, color=(230, 230, 230, 255))

# ----------------------------------------------------------------------
# Helpers de pipeline de render
# ----------------------------------------------------------------------
def _cor_atual():
    return PALETA[paleta_idx] + (255,) if len(PALETA[paleta_idx]) == 3 else PALETA[paleta_idx]


def _clip_tela_poligono(pts_tela):
    """Recorta poligono em pixels contra a tela (0..LARGURA, 0..ALTURA)."""
    global recorte_janela
    backup = recorte_janela
    recorte_janela = (0, 0, LARGURA, ALTURA)
    try:
        return sutherland_hodgman(pts_tela)
    finally:
        recorte_janela = backup


def _desenhar_objeto(obj):
    """Pipeline: pontos locais -> acumulada -> window->viewport -> recorte -> shapes."""
    cor = obj.cor + (255,) if len(obj.cor) == 3 else obj.cor
    if obj.tipo == "circulo":
        c_mundo = aplicar_transformacao([obj.circulo["centro"]], obj.matriz)[0]
        cx_px, cy_px = aplicar_transformacao([c_mundo], matriz_window_para_viewport())[0]
        r_mundo = obj.circulo["raio"] * math.sqrt(abs(np.linalg.det(obj.matriz[:2, :2])))
        # transforma 2 pontos do circulo p/ medir raio em pixels (evita deformacao)
        w2v = matriz_window_para_viewport()
        p1 = aplicar_transformacao([(c_mundo[0] + r_mundo, c_mundo[1])], w2v)[0]
        r_px = math.hypot(p1[0] - cx_px, p1[1] - cy_px)
        shapes_list.append(shapes.Circle(cx_px, cy_px, r_px, color=cor, batch=batch))
        return

    pts_tela = obj.pontos_tela()
    if recorte_on:
        # para polígono: recorta em pixel contra a tela; em mundo faria mais
        # sentido contra recorte_janela, mas o requisito pede borda visivel.
        pts_tela = _clip_tela_poligono(pts_tela)
    if len(pts_tela) < 3:
        return
    if obj.preenchido:
        shapes_list.append(shapes.Polygon(*pts_tela, color=cor, batch=batch))
    else:
        for i in range(len(pts_tela)):
            a, b = pts_tela[i], pts_tela[(i + 1) % len(pts_tela)]
            shapes_list.append(shapes.Line(a[0], a[1], b[0], b[1],
                                           thickness=2, color=cor, batch=batch))


def _desenhar_hud():
    """Desenha janela de recorte (borda), laço e texto de info."""
    # janela de recorte (em mundo -> tela)
    if recorte_on:
        xmin, ymin, xmax, ymax = recorte_janela
        w2v = matriz_window_para_viewport()
        cantos = aplicar_transformacao(
            [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)], w2v)
        for i in range(4):
            a, b = cantos[i], cantos[(i + 1) % 4]
            shapes_list.append(shapes.Line(a[0], a[1], b[0], b[1],
                                           thickness=1, color=(90, 90, 120), batch=batch))
    # laço de seleção
    if laco_inicio and laco_fim:
        x0, y0 = laco_inicio; x1, y1 = laco_fim
        shapes_list.append(shapes.Rectangle(min(x0, x1), min(y0, y1),
                                            abs(x1 - x0), abs(y1 - y0),
                                            color=(80, 120, 200, 60), batch=batch))
    # objeto em criação (preview)
    if pontos_criacao:
        for p in pontos_criacao:
            shapes_list.append(shapes.Circle(p[0], p[1], 3, color=(255, 255, 255),
                                             batch=batch))
        if len(pontos_criacao) > 1:
            for i in range(len(pontos_criacao) - 1):
                a, b = pontos_criacao[i], pontos_criacao[i + 1]
                shapes_list.append(shapes.Line(a[0], a[1], b[0], b[1],
                                               thickness=1, color=(255, 255, 0), batch=batch))


def _info_texto():
    if selecionados:
        o = selecionados[0]
        a, p = o.area_perimetro()
        return (f"Modo: {modo} | sel: {len(selecionados)} | "
                f"area={a:.1f} perim={p:.1f} | ref={ref_modo} "
                f"| recorte={'ON' if recorte_on else 'OFF'} "
                f"| H=cor G=fill I=info")
    return (f"Modo: {modo} | obj: {len(objetos)} | ref={ref_modo} "
            f"| recorte={'ON' if recorte_on else 'OFF'} | H=cor G=fill")


def redesenhar():
    """Reconstroi todos os shapes (aceitavel no scaffold) + HUD."""
    global shapes_list
    for s in shapes_list:
        s.delete()
    shapes_list = []
    for o in objetos:
        _desenhar_objeto(o)
    _desenhar_hud()
    # bounding box dos selecionados (item opcional, mas util p/ ref)
    for o in selecionados:
        x0, y0, x1, y1 = o.bbox_mundo()
        w2v = matriz_window_para_viewport()
        cantos = aplicar_transformacao([(x0, y0), (x1, y1)], w2v)
        (px0, py0), (px1, py1) = cantos
        shapes_list.append(shapes.Box(min(px0, py1), min(py0, py1),
                                      abs(px1 - px0), abs(py1 - py0),
                                      thickness=1, color=(255, 255, 0), batch=batch))
    label_info.text = _info_texto()


# ======================================================================
# PASSO MANIPULACAO — aplica transformacao aos selecionados
# ======================================================================
def aplicar_nos_selecionados(matriz_elementar, referencia=None):
    """Compoe a matriz elementar (em torno de `referencia` se dada) em cada sel."""
    for o in selecionados:
        if referencia is None:
            o.aplicar(matriz_elementar)
        else:
            o.aplicar(matriz_em_torno_de(referencia, matriz_elementar))


def referencia_atual(objeto):
    """Resolve o ponto de referencia (1=centro 2=canto bbox 3=ponto clicado)."""
    if ref_modo == 1:
        return objeto.centro_mundo()
    if ref_modo == 2:
        x0, y0, x1, y1 = objeto.bbox_mundo()
        return (x0, y0)   # canto superior esquerdo do bbox
    return ref_ponto


# ======================================================================
# EVENTOS — MOUSE
# ======================================================================
@janela.event
def on_mouse_press(x, y, button, modifiers):
    global modo, laco_inicio, laco_fim, ref_ponto, ref_modo, selecionados
    wx, wy = viewport_para_mundo(x, y)

    # ---- PAN (botao do meio) -------------------------------------
    if button == mouse.MIDDLE:
        janela._pan_ant = (x, y)
        return

    # ---- criar poligono ------------------------------------------
    if modo == MODO_CRIAR_POLIGONO and button == mouse.LEFT:
        # clique direito fecha o poligono (>=3 pontos)
        pontos_criacao.append((x, y))   # guarda em PIXEL; converte no fechamento
        redesenhar()
        return

    # ---- selecionar ----------------------------------------------
    if modo == MODO_SELECIONAR and button == mouse.LEFT:
        alvo = None
        # percorre de tras p/ frente (ultimo desenhado tem prioridade)
        for o in reversed(objetos):
            if o.contem(wx, wy):
                alvo = o
                break
        shift = bool(modifiers & key.MOD_SHIFT)
        if alvo is None:
            # laço retangular
            laco_inicio = (x, y); laco_fim = (x, y)
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
        redesenhar()
        return

    # ---- mover: grava ponto de referencia se ref_modo==3 -----------
    if modo == MODO_MOVER and button == mouse.LEFT:
        if ref_modo == 3:
            ref_ponto = (wx, wy)
        return


@janela.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    global laco_fim
    # PAN
    if button == mouse.MIDDLE:
        ax, ay = janela._pan_ant
        dwx, dwy = viewport_para_mundo(ax, ay)
        nwx, nwy = viewport_para_mundo(x, y)
        window_centro[0] += (dwx - nwx); window_centro[1] += (dwy - nwy)
        janela._pan_ant = (x, y)
        redesenhar()
        return
    # LAÇO
    if modo == MODO_SELECIONAR and laco_inicio is not None:
        laco_fim = (x, y)
        redesenhar()


@janela.event
def on_mouse_release(x, y, button, modifiers):
    global laco_inicio, laco_fim, selecionados, modo
    if button == mouse.MIDDLE:
        return
    # fecha laço: seleciona objetos cujo centro cai na regiao
    if modo == MODO_SELECIONAR and laco_inicio is not None:
        x0, y0 = laco_inicio; x1, y1 = laco_fim
        pxmin, pxmax = min(x0, x1), max(x0, x1)
        pymin, pymax = min(y0, y1), max(y0, y1)
        w2v = matriz_window_para_viewport()
        novos = []
        for o in objetos:
            cx, cy = o.centro_mundo()
            (pcx, pcy), = aplicar_transformacao([(cx, cy)], w2v)
            if pxmin <= pcx <= pxmax and pymin <= pcy <= pymax:
                novos.append(o)
        if novos:
            if modifiers & key.MOD_SHIFT:
                for o in novos:
                    if o not in selecionados:
                        selecionados.append(o)
            else:
                selecionados = novos
        laco_inicio = None; laco_fim = None
        redesenhar()


@janela.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    """Zoom: multiplica half_w/half_h mantendo a razao de aspecto."""
    global window_half
    fator = 1.1 ** (-scroll_y)   # scroll pra cima = zoom in
    novo = window_half * fator
    # clamp
    if LARGURA / (2 * novo[0]) > ZOOM_MAX or LARGURA / (2 * novo[0]) < ZOOM_MIN:
        return
    window_half = novo
    redesenhar()


# ======================================================================
# EVENTOS — TECLADO
# ======================================================================
@janela.event
def on_key_press(simbolo, modifiers):
    global modo, criando_poligono, pontos_criacao, selecionados
    global ref_modo, recorte_on, paleta_idx

    K = key

    # ---- modos ---------------------------------------------------
    if simbolo == K.P:
        modo = MODO_CRIAR_POLIGONO
        pontos_criacao = []
        redesenhar(); return
    if simbolo == K.C:
        _criar_circulo(); return
    if simbolo == K.T:
        _criar_triangulo(); return
    if simbolo == K.R and modo != MODO_MOVER:
        _criar_retangulo(); return
    if simbolo == K.S:
        modo = MODO_SELECIONAR
        pontos_criacao = []
        redesenhar(); return
    if simbolo == K.M:
        modo = MODO_MOVER
        redesenhar(); return

    # ---- fechar poligono em criacao ------------------------------
    if modo == MODO_CRIAR_POLIGONO and simbolo == K.ENTER:
        _fechar_poligono(); return

    # ---- referencia de rotacao/escala ---------------------------
    if simbolo in (K._1, K._2, K._3):
        ref_modo = {K._1: 1, K._2: 2, K._3: 3}[simbolo]
        redesenhar(); return

    # ---- recorte on/off -----------------------------------------
    if simbolo == K.F1:
        recorte_on = not recorte_on
        redesenhar(); return

    # ---- cor (cicla paleta) -------------------------------------
    if simbolo == K.H:
        paleta_idx = (paleta_idx + 1) % len(PALETA)
        for o in selecionados:
            o.cor = PALETA[paleta_idx]
        redesenhar(); return

    # ---- preenchimento ------------------------------------------
    if simbolo == K.G:
        for o in selecionados:
            o.preenchido = not o.preenchido
        redesenhar(); return

    # ---- info area/perimetro ------------------------------------
    if simbolo == K.I:
        for o in selecionados:
            a, p = o.area_perimetro()
            print(f"[{o.tipo}] area={a:.2f} perim={p:.2f}")
        return

    # ---- remover selecionados -----------------------------------
    if simbolo == K.DELETE:
        for o in selecionados:
            if o in objetos:
                objetos.remove(o)
        selecionados = []
        redesenhar(); return

    # ---- manipulação: translacao/rotacao/escala (PASSO 0 + PASSO MANIP) ----
    if modo == MODO_MOVER and selecionados:
        if simbolo == K.LEFT:
            aplicar_nos_selecionados(matriz_translacao(-PASSO_TRANS, 0))
        elif simbolo == K.RIGHT:
            aplicar_nos_selecionados(matriz_translacao(PASSO_TRANS, 0))
        elif simbolo == K.UP:
            aplicar_nos_selecionados(matriz_translacao(0, PASSO_TRANS))
        elif simbolo == K.DOWN:
            aplicar_nos_selecionados(matriz_translacao(0, -PASSO_TRANS))
        elif simbolo == K.Q:
            for o in selecionados:
                r = referencia_atual(o)
                aplicar_nos_selecionados(matriz_rotacao(PASSO_ROT), r)
        elif simbolo == K.E:
            for o in selecionados:
                r = referencia_atual(o)
                aplicar_nos_selecionados(matriz_rotacao(-PASSO_ROT), r)
        elif simbolo in (K.PLUS, K.EQUAL):
            for o in selecionados:
                r = referencia_atual(o)
                aplicar_nos_selecionados(matriz_escala(FATOR_ESC, FATOR_ESC), r)
        elif simbolo == K.MINUS:
            for o in selecionados:
                r = referencia_atual(o)
                aplicar_nos_selecionados(matriz_escala(1 / FATOR_ESC, 1 / FATOR_ESC), r)
        # escala NAO uniforme: Shift + '+'/'-' em X ou Y (opcional)
        elif simbolo == K.X and (modifiers & key.MOD_SHIFT):
            for o in selecionados:
                r = referencia_atual(o)
                aplicar_nos_selecionados(matriz_escala(FATOR_ESC, 1.0), r)
        elif simbolo == K.Y and (modifiers & key.MOD_SHIFT):
            for o in selecionados:
                r = referencia_atual(o)
                aplicar_nos_selecionados(matriz_escala(1.0, FATOR_ESC), r)
        redesenhar()
        return

    if simbolo == K.ESCAPE:
        janela.close()


# ======================================================================
# CRIAÇÃO — helpers (recebem input do mouse em PIXEL, guardam em MUNDO)
# ======================================================================
def _fechar_poligono():
    """Fecha o poligono em criacao convertendo os pontos para MUNDO."""
    global pontos_criacao, modo
    if len(pontos_criacao) >= 3:
        pts_mundo = [viewport_para_mundo(x, y) for (x, y) in pontos_criacao]
        # normaliza: subtrai centroide p/ ter coords locais pequenas
        cx = sum(p[0] for p in pts_mundo) / len(pts_mundo)
        cy = sum(p[1] for p in pts_mundo) / len(pts_mundo)
        locais = [(x - cx, y - cy) for (x, y) in pts_mundo]
        obj = Objeto2D(locais, PALETA[paleta_idx], tipo="poligono")
        obj.matriz = matriz_translacao(cx, cy)   # posiciona de volta
        objetos.append(obj)
    pontos_criacao = []
    modo = MODO_SELECIONAR
    redesenhar()


def _criar_circulo():
    """Cria circulo no centro da window atual (raio 40 mundo)."""
    global modo
    cx, cy = window_centro
    r = 40.0
    obj = Objeto2D([], PALETA[paleta_idx], tipo="circulo")
    obj.circulo = {"centro": (0.0, 0.0), "raio": r}
    obj.matriz = matriz_translacao(cx, cy)   # centroide vai p/ (0,0) e posiciona
    objetos.append(obj)
    modo = MODO_SELECIONAR
    redesenhar()


def _criar_triangulo():
    """Triangulo equilatero em coords locais, centrado em (0,0)."""
    global modo
    locais = [(-50, -30), (50, -30), (0, 50)]
    cx, cy = window_centro
    obj = Objeto2D(locais, PALETA[paleta_idx], tipo="triangulo")
    obj.matriz = matriz_translacao(cx, cy)
    objetos.append(obj)
    modo = MODO_SELECIONAR
    redesenhar()


def _criar_retangulo():
    """Retangulo 100x60 em coords locais centrado em (0,0)."""
    global modo
    locais = [(-50, -30), (50, -30), (50, 30), (-50, 30)]
    cx, cy = window_centro
    obj = Objeto2D(locais, PALETA[paleta_idx], tipo="retangulo")
    obj.matriz = matriz_translacao(cx, cy)
    objetos.append(obj)
    modo = MODO_SELECIONAR
    redesenhar()


# ======================================================================
# DRAW
# ======================================================================
@janela.event
def on_draw():
    janela.clear()
    batch.draw()
    label_info.draw()


# ======================================================================
# MAIN
# ======================================================================
if __name__ == "__main__":
    # cria um retangulo de exemplo p/ o usuario ver algo de inicio
    _criar_retangulo()
    pyglet.app.run()