"""
Testes das transformacoes do editor 2D (editor2d.py)
=====================================================
Importa as funcoes do editor e verifica, passo a passo, com prints no
terminal, cada transformacao por matriz homogenea.

Como o editor2d.py cria uma Window do pyglet ao ser importado, este script
precisa rodar em ambiente com display. Em servidor headless, use:

    xvfb-run -a python teste_transformacoes.py

Ou, no WSL2 sem X, instale um X server (VcXsrv/X410) e exporte DISPLAY.
"""

import math

import numpy as np

# Importa tudo que interessa do editor (a criacao da Window e efeito colateral).
import editor2d as ed
print(ed.__file__)
print(dir(ed))


# ======================================================================
# UTILITARIOS DE IMPRESSAO
# ======================================================================
def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def subtitulo(texto):
    print("\n--- " + texto + " ---")


def imprimir_matriz(nome, M):
    print(f"{nome} =")
    for linha in M:
        print("  [" + "  ".join(f"{v:9.4f}" for v in linha) + "]")


def imprimir_pontos(nome, pts):
    print(f"{nome} =")
    for i, (x, y) in enumerate(pts):
        print(f"  P{i} = ({x:9.4f}, {y:9.4f})")


def approx(a, b, tol=1e-9):
    return abs(a - b) <= tol


def pontos_aproximados(pts_a, pts_b, tol=1e-9):
    if len(pts_a) != len(pts_b):
        return False
    for (xa, ya), (xb, yb) in zip(pts_a, pts_b):
        if not (approx(xa, xb, tol) and approx(ya, yb, tol)):
            return False
    return True


def verificar(condicao, mensagem):
    status = "OK  " if condicao else "FALHOU"
    print(f"  [{status}] {mensagem}")
    return condicao


# ======================================================================
# TESTE 1 — MATRIZES ELEMENTARES
# ======================================================================
def teste_1_matrizes_elementares():
    titulo("TESTE 1 — Matrizes elementares (identidade, translacao, rotacao, escala)")

    subtitulo("1.1 Identidade")
    I = ed.matriz_identidade()
    imprimir_matriz("I", I)
    verificar(approx(I[0, 0], 1) and approx(I[1, 1], 1) and approx(I[2, 2], 1),
              "diagonal principal = 1")
    verificar(approx(I[0, 1], 0) and approx(I[1, 0], 0),
              "fora da diagonal = 0")

    subtitulo("1.2 Translocao T(15, -7)")
    T = ed.matriz_translacao(15, -7)
    imprimir_matriz("T(15,-7)", T)
    verificar(approx(T[0, 2], 15) and approx(T[1, 2], -7),
              "coluna de translacao = (15, -7)")

    subtitulo("1.3 Rotacao R(30 deg)")
    theta = math.radians(30)
    R = ed.matriz_rotacao(theta)
    imprimir_matriz("R(30)", R)
    verificar(approx(R[0, 0], math.cos(theta)) and approx(R[0, 1], -math.sin(theta)),
              "linha 0 = [cos, -sin, 0]")
    verificar(approx(R[1, 0], math.sin(theta)) and approx(R[1, 1], math.cos(theta)),
              "linha 1 = [sin, cos, 0]")
    verificar(approx(np.linalg.det(R[:2, :2]), 1.0),
              "det(R 2x2) = 1 (preserva area)")

    subtitulo("1.4 Escala S(2, 0.5)")
    S = ed.matriz_escala(2, 0.5)
    imprimir_matriz("S(2, 0.5)", S)
    verificar(approx(S[0, 0], 2) and approx(S[1, 1], 0.5),
              "diagonal = (2, 0.5)")


# ======================================================================
# TESTE 2 — APLICACAO EM PONTOS
# ======================================================================
def teste_2_aplicacao_em_pontos():
    titulo("TESTE 2 — Aplicacao de matrizes em pontos (via aplicar_matriz_em_pontos)")

    subtitulo("2.1 Translacao de (10, 5) por T(15, -7)")
    p = [(10, 5)]
    resultado = ed.aplicar_matriz_em_pontos(p, ed.matriz_translacao(15, -7))
    imprimir_pontos("resultado", resultado)
    verificar(pontos_aproximados(resultado, [(25, -2)]),
              "(10,5) + (15,-7) = (25,-2)")

    subtitulo("2.2 Rotacao de (1, 0) por 90 deg (anti-horario)")
    resultado = ed.aplicar_matriz_em_pontos([(1, 0)], ed.matriz_rotacao(math.radians(90)))
    imprimir_pontos("resultado", resultado)
    verificar(pontos_aproximados(resultado, [(0, 1)]),
              "(1,0) girado 90 deg = (0,1)")

    subtitulo("2.3 Rotacao de (0, 1) por 90 deg")
    resultado = ed.aplicar_matriz_em_pontos([(0, 1)], ed.matriz_rotacao(math.radians(90)))
    imprimir_pontos("resultado", resultado)
    verificar(pontos_aproximados(resultado, [(-1, 0)]),
              "(0,1) girado 90 deg = (-1,0)")

    subtitulo("2.4 Escala de (3, 4) por S(2, 0.5)")
    resultado = ed.aplicar_matriz_em_pontos([(3, 4)], ed.matriz_escala(2, 0.5))
    imprimir_pontos("resultado", resultado)
    verificar(pontos_aproximados(resultado, [(6, 2)]),
              "(3,4) escalado por (2,0.5) = (6,2)")

    subtitulo("2.5 Aplicar em varios pontos de uma vez (poligono)")
    quadrado_local = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    resultado = ed.aplicar_matriz_em_pontos(quadrado_local, ed.matriz_translacao(10, 20))
    imprimir_pontos("quadrado transladado por (10,20)", resultado)
    esperado = [(9, 19), (11, 19), (11, 21), (9, 21)]
    verificar(pontos_aproximados(resultado, esperado),
              "todos os 4 vertices foram transladados")


# ======================================================================
# TESTE 3 — COMPOSICAO: A ORDEM IMPORTA
# ======================================================================
def teste_3_composicao_ordem():
    titulo("TESTE 3 — Composicao: T*R != R*T (a ordem importa)")

    p = [(1, 0)]
    T = ed.matriz_translacao(15, 0)
    R = ed.matriz_rotacao(math.radians(90))

    subtitulo("3.1 'Girar 90 depois transladar 15': M = T @ R")
    M1 = T @ R
    imprimir_matriz("T @ R", M1)
    r1 = ed.aplicar_matriz_em_pontos(p, M1)
    imprimir_pontos("resultado", r1)
    verificar(pontos_aproximados(r1, [(15, 1)]),
              "(1,0) -> gira p/ (0,1) -> translada -> (15,1)")

    subtitulo("3.2 'Transladar 15 depois girar 90': M = R @ T")
    M2 = R @ T
    imprimir_matriz("R @ T", M2)
    r2 = ed.aplicar_matriz_em_pontos(p, M2)
    imprimir_pontos("resultado", r2)
    verificar(pontos_aproximados(r2, [(0, 16)]),
              "(1,0) -> translada p/ (16,0) -> gira -> (0,16)")

    subtitulo("3.3 Conclusao")
    diferentes = not pontos_aproximados(r1, r2)
    verificar(diferentes, "T@R e R@T produzem resultados DIFERENTES (matrizes nao comutam)")


# ======================================================================
# TESTE 4 — ROTACAO EM TORNO DE UM PONTO
# ======================================================================
def teste_4_rotacao_em_torno_de():
    titulo("TESTE 4 — Rotacao em torno de um ponto p (matriz_em_torno_de)")

    p_ref = (10, 10)
    R90 = ed.matriz_rotacao(math.radians(90))

    subtitulo("4.1 Rotacionar (11, 10) por 90 deg em torno de (10, 10)")
    M = ed.matriz_em_torno_de(p_ref, R90)
    imprimir_matriz("T(10,10) @ R(90) @ T(-10,-10)", M)
    resultado = ed.aplicar_matriz_em_pontos([(11, 10)], M)
    imprimir_pontos("resultado", resultado)
    # (11,10) e 1 unidade a direita de (10,10); girar 90 anti-horario
    # leva para 1 unidade ACIMA: (10, 11)
    verificar(pontos_aproximados(resultado, [(10, 11)]),
              "(11,10) em torno de (10,10) -> (10,11)")

    subtitulo("4.2 O ponto de referencia (10, 10) NAO se move")
    resultado = ed.aplicar_matriz_em_pontos([p_ref], M)
    imprimir_pontos("resultado", resultado)
    verificar(pontos_aproximados(resultado, [p_ref]),
              "ponto de referencia fica fixo")

    subtitulo("4.3 Comparacao: girar 90 em torno da ORIGEM vs em torno de (10,10)")
    r_origem = ed.aplicar_matriz_em_pontos([(11, 10)], R90)
    r_ponto = ed.aplicar_matriz_em_pontos([(11, 10)], M)
    imprimir_pontos("em torno da origem (0,0)", r_origem)
    imprimir_pontos("em torno de (10,10)", r_ponto)
    verificar(not pontos_aproximados(r_origem, r_ponto),
              "resultados diferentes (a referencia muda o resultado)")


# ======================================================================
# TESTE 5 — INVARIANTES: ROTACAO PRESERVA DISTANCIA, AREA E PERIMETRO
# ======================================================================
def teste_5_invariantes_rotacao():
    titulo("TESTE 5 — Invariantes de rotacao (distancia, area, perimetro)")

    triangulo = [(0, 0), (3, 0), (0, 4)]   # triangulo 3-4-5

    area_antes = ed.calcular_area_poligono(triangulo)
    perim_antes = ed.calcular_perimetro_poligono(triangulo)

    subtitulo("5.1 Estado antes da rotacao")
    imprimir_pontos("triangulo", triangulo)
    print(f"  area      = {area_antes:.6f}   (esperado = 6.0)")
    print(f"  perimetro = {perim_antes:.6f}   (esperado = 12.0: 3+4+5)")

    subtitulo("5.2 Rotacionar 30 deg em torno da origem")
    R30 = ed.matriz_rotacao(math.radians(30))
    triangulo_rot = ed.aplicar_matriz_em_pontos(triangulo, R30)
    imprimir_pontos("triangulo_rotacionado", triangulo_rot)

    area_depois = ed.calcular_area_poligono(triangulo_rot)
    perim_depois = ed.calcular_perimetro_poligono(triangulo_rot)
    print(f"  area      = {area_depois:.6f}")
    print(f"  perimetro = {perim_depois:.6f}")

    verificar(approx(area_antes, area_depois, tol=1e-9),
              "area preservada")
    verificar(approx(perim_antes, perim_depois, tol=1e-9),
              "perimetro preservado")

    subtitulo("5.3 Distancias entre vertices preservadas")
    d_orig = math.hypot(3 - 0, 0 - 0)
    d_rot = math.hypot(triangulo_rot[1][0] - triangulo_rot[0][0],
                       triangulo_rot[1][1] - triangulo_rot[0][1])
    print(f"  d(P0,P1) antes = {d_orig:.6f}")
    print(f"  d(P0,P1) depois = {d_rot:.6f}")
    verificar(approx(d_orig, d_rot, tol=1e-9),
              "distancias preservadas")


# ======================================================================
# TESTE 6 — ESCALA: AREA CRESCE COM O QUADRADO DO FATOR
# ======================================================================
def teste_6_area_escala():
    titulo("TESTE 6 — Escala uniforme: area cresce com o quadrado do fator")

    quadrado = [(0, 0), (2, 0), (2, 2), (0, 2)]   # lado 2, area 4
    area_antes = ed.calcular_area_poligono(quadrado)
    print(f"  area original = {area_antes:.6f}   (esperado = 4.0)")

    for k in (2.0, 3.0, 0.5):
        S = ed.matriz_escala(k, k)
        q2 = ed.aplicar_matriz_em_pontos(quadrado, S)
        area = ed.calcular_area_poligono(q2)
        esperado = area_antes * k * k
        verificar(approx(area, esperado, tol=1e-9),
                  f"k={k}: area={area:.4f}, esperado={esperado:.4f} (k^2)")

    subtitulo("6.1 Escala NAO uniforme: area cresce com sx*sy")
    S = ed.matriz_escala(3, 0.5)
    q2 = ed.aplicar_matriz_em_pontos(quadrado, S)
    area = ed.calcular_area_poligono(q2)
    esperado = area_antes * 3 * 0.5
    verificar(approx(area, esperado, tol=1e-9),
              f"area={area:.4f}, esperado={esperado:.4f} (sx*sy)")


# ======================================================================
# TESTE 7 — OBJETO2D: PIPELINE COMPLETO (local -> mundo -> tela)
# ======================================================================
def teste_7_objeto_pipeline():
    titulo("TESTE 7 — Objeto2D: pipeline local -> mundo -> tela")

    local = [(-1, -1), (1, -1), (1, 1), (-1, 1)]     # quadrado 2x2
    obj = ed.Objeto2D(local, (255, 0, 0), tipo="poligono")
    obj.compor_matriz(ed.matriz_translacao(100, 200))  # poe em (100,200)

    subtitulo("7.1 Pontos em MUNDO (apos matriz do objeto)")
    pts_mundo = obj.obter_pontos_mundo()
    imprimir_pontos("mundo", pts_mundo)
    verificar(pontos_aproximados(pts_mundo,
              [(99, 199), (101, 199), (101, 201), (99, 201)]),
              "translacao de (100,200) aplicada")

    subtitulo("7.2 Bounding box em MUNDO")
    x0, y0, x1, y1 = obj.obter_bbox_mundo()
    print(f"  bbox = ({x0}, {y0}, {x1}, {y1})")
    verificar(approx(x0, 99) and approx(y0, 199) and approx(x1, 101) and approx(y1, 201),
              "bbox minima = (99,199), maxima = (101,201)")

    subtitulo("7.3 Centro em MUNDO")
    cx, cy = obj.obter_centro_mundo()
    print(f"  centro = ({cx}, {cy})")
    verificar(approx(cx, 100) and approx(cy, 200),
              "centro = (100, 200)")

    subtitulo("7.4 Pontos em TELA (apos W2V)")
    pts_tela = obj.obter_pontos_tela()
    imprimir_pontos("tela", pts_tela)
    print("  (com window 1:1, a tela do pyglet e 1400x1000,")
    print("   centro do mundo (700,500) mapeia para (700,500) em pixel)")

    subtitulo("7.5 Composicao: transladar de novo por (50, 50)")
    obj.compor_matriz(ed.matriz_translacao(50, 50))
    pts_mundo2 = obj.obter_pontos_mundo()
    imprimir_pontos("mundo apos 2a translacao", pts_mundo2)
    verificar(pontos_aproximados(pts_mundo2,
              [(149, 249), (151, 249), (151, 251), (149, 251)]),
              "as duas translacoes se somam (100+50=150, 200+50=250)")


# ======================================================================
# TESTE 8 — SELECAO (contem_ponto) ANTES E DEPOIS DE TRANSFORMAR
# ======================================================================
def teste_8_selecao():
    titulo("TESTE 8 — Selecao: contem_ponto antes e depois de transformar")

    local = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    obj = ed.Objeto2D(local, (0, 255, 0), tipo="poligono")
    obj.compor_matriz(ed.matriz_translacao(100, 100))

    subtitulo("8.1 Antes de rotacionar")
    verificar(obj.contem_ponto(100, 100),
              "(100,100) [centro] esta dentro")
    verificar(obj.contem_ponto(101, 100),
              "(101,100) [borda] esta dentro")
    verificar(not obj.contem_ponto(105, 100),
              "(105,100) [fora] NAO esta dentro")

    subtitulo("8.2 Rotacionar 45 deg em torno do centro (100,100)")
    R45 = ed.matriz_rotacao(math.radians(45))
    obj.compor_matriz(ed.matriz_em_torno_de((100, 100), R45))

    verificar(obj.contem_ponto(100, 100),
              "centro continua dentro (nao se move)")
    # (105,100) era fora; apos rotacao, ainda deve estar fora
    verificar(not obj.contem_ponto(105, 100),
              "(105,100) continua fora")

    subtitulo("8.3 Circulo: distingue dentro/fora por distancia")
    circ = ed.Objeto2D([], (0, 0, 255), tipo="circulo")
    circ.circulo = {"centro": (0, 0), "raio": 5}
    circ.compor_matriz(ed.matriz_translacao(50, 50))
    verificar(circ.contem_ponto(50, 50),
              "centro do circulo (50,50) esta dentro")
    verificar(circ.contem_ponto(53, 50),
              "ponto (53,50) a 3 do centro esta dentro")
    verificar(not circ.contem_ponto(56, 50),
              "ponto (56,50) a 6 do centro esta fora")


# ======================================================================
# TESTE 9 — WINDOW <-> VIEWPORT
# ======================================================================
def teste_9_camera():
    titulo("TESTE 9 — Window <-> Viewport (mundo <-> tela)")

    subtitulo("9.1 Estado inicial da camera")
    print(f"  window_centro = {ed.window_centro}")
    print(f"  window_half   = {ed.window_half}")
    print(f"  LARGURA, ALTURA = {ed.LARGURA}, {ed.ALTURA}")

    subtitulo("9.2 Centro do mundo mapeia para o centro da tela")
    w2v = ed.matriz_mundo_para_tela()
    imprimir_matriz("W2V", w2v)
    centro_mundo = tuple(ed.window_centro)
    centro_px = ed.aplicar_matriz_em_pontos([centro_mundo], w2v)[0]
    imprimir_pontos("centro_mundo em pixel", [centro_px])
    verificar(approx(centro_px[0], ed.LARGURA / 2) and approx(centro_px[1], ed.ALTURA / 2),
              f"centro do mundo -> ({ed.LARGURA/2}, {ed.ALTURA/2})")

    subtitulo("9.3 Ida e volta: mundo -> tela -> mundo")
    p_mundo = (123.0, 456.0)
    p_tela = ed.aplicar_matriz_em_pontos([p_mundo], w2v)[0]
    p_volta = ed.converter_tela_para_mundo(p_tela[0], p_tela[1])
    imprimir_pontos("p_mundo original", [p_mundo])
    imprimir_pontos("p_tela", [p_tela])
    imprimir_pontos("p_volta (via inversa)", [p_volta])
    verificar(pontos_aproximados([p_volta], [p_mundo], tol=1e-6),
              "converter_tela_para_mundo e a inversa correta")

    subtitulo("9.4 Canto do viewport = canto da window")
    canto_px = ed.converter_tela_para_mundo(0, 0)
    canto_esperado = (ed.window_centro[0] - ed.window_half[0],
                      ed.window_centro[1] - ed.window_half[1])
    imprimir_pontos("canto_px=(0,0) em mundo", [canto_px])
    imprimir_pontos("canto_esperado", [canto_esperado])
    verificar(pontos_aproximados([canto_px], [canto_esperado], tol=1e-6),
              "(0,0) em pixel = canto inferior esquerdo da window")


# ======================================================================
# TESTE 10 — RECORTE: SUTHERLAND-HODGMAN
# ======================================================================
def teste_10_sutherland_hodgman():
    titulo("TESTE 10 — Recorte de poligono (Sutherland-Hodgman)")

    # Janela de recorte pequena em mundo
    ed.recorte_janela = (0, 0, 10, 10)
    print(f"  recorte_janela = {ed.recorte_janela}")

    subtitulo("10.1 Poligono inteiramente dentro (nao deve mudar)")
    poligono_dentro = [(2, 2), (8, 2), (8, 8), (2, 8)]
    recortado = ed.recortar_poligono_sutherland_hodgman(poligono_dentro)
    imprimir_pontos("original", poligono_dentro)
    imprimir_pontos("recortado", recortado)
    verificar(len(recortado) == 4, "4 vertices preservados")

    subtitulo("10.2 Poligono inteiramente fora (deve desaparecer)")
    poligono_fora = [(20, 20), (30, 20), (30, 30), (20, 30)]
    recortado = ed.recortar_poligono_sutherland_hodgman(poligono_fora)
    imprimir_pontos("original", poligono_fora)
    imprimir_pontos("recortado", recortado)
    verificar(len(recortado) == 0, "poligono fora vira vazio")

    subtitulo("10.3 Poligono cruzando a borda direita (x=10)")
    poligono_cruza = [(5, 2), (15, 2), (15, 8), (5, 8)]
    recortado = ed.recortar_poligono_sutherland_hodgman(poligono_cruza)
    imprimir_pontos("original", poligono_cruza)
    imprimir_pontos("recortado", recortado)
    # o pedaco com x=15 vira x=10
    tem_x10 = any(approx(px, 10) for px, _ in recortado)
    verificar(tem_x10, "borda direita cortada em x=10")

    subtitulo("10.4 Aresta horizontal cruzando borda (o caso que causou o bug)")
    # retangulo alinhado com topo exatamente na borda y=10
    poligono_alinhado = [(3, 5), (7, 5), (7, 15), (3, 15)]
    try:
        recortado = ed.recortar_poligono_sutherland_hodgman(poligono_alinhado)
        imprimir_pontos("recortado", recortado)
        verificar(len(recortado) >= 3,
                  "aresta horizontal nao crashou (guard bx==ax / by==ay)")
    except ZeroDivisionError:
        verificar(False, "division by zero NAO foi tratada")

    # restaura janela larga para nao afetar testes seguintes
    ed.recorte_janela = (-ed.LARGURA, -ed.ALTURA, 2 * ed.LARGURA, 2 * ed.ALTURA)


# ======================================================================
# TESTE 11 — RECORTE: COHEN-SUTHERLAND
# ======================================================================
def teste_11_cohen_sutherland():
    titulo("TESTE 11 — Recorte de segmento (Cohen-Sutherland)")

    janela = (0, 0, 10, 10)
    xmin, ymin, xmax, ymax = janela
    print(f"  janela = {janela}")

    subtitulo("11.1 Segmento inteiramente dentro")
    p1, p2 = (2, 2), (8, 8)
    r = ed.recortar_segmento_cohen_sutherland(p1, p2, xmin, ymin, xmax, ymax)
    print(f"  entrada = {p1}, {p2}")
    print(f"  saida   = {r}")
    verificar(r is not None and approx(r[0][0], 2) and approx(r[1][0], 8),
              "aceito como veio")

    subtitulo("11.2 Segmento inteiramente fora")
    r = ed.recortar_segmento_cohen_sutherland((-5, -5), (-2, -2),
                                              xmin, ymin, xmax, ymax)
    print(f"  entrada = (-5,-5), (-2,-2)")
    print(f"  saida   = {r}")
    verificar(r is None, "rejeitado (trivial)")

    subtitulo("11.3 Segmento cruzando a borda direita")
    p1, p2 = (5, 5), (15, 5)
    r = ed.recortar_segmento_cohen_sutherland(p1, p2, xmin, ymin, xmax, ymax)
    print(f"  entrada = {p1}, {p2}")
    print(f"  saida   = {r}")
    verificar(r is not None and approx(r[1][0], 10),
              "borda direita cortada em x=10")

    subtitulo("11.4 Segmento diagonal cruzando duas bordas")
    p1, p2 = (-5, -5), (15, 15)
    r = ed.recortar_segmento_cohen_sutherland(p1, p2, xmin, ymin, xmax, ymax)
    print(f"  entrada = {p1}, {p2}")
    print(f"  saida   = {r}")
    verificar(r is not None and approx(r[0][0], 0) and approx(r[1][0], 10),
              "corta em (0,0) e (10,10)")


# ======================================================================
# TESTE 12 — BOUNDING BOX (verificacao do bug que voce corrigiu)
# ======================================================================
def teste_12_bbox():
    titulo("TESTE 12 — Bounding box correta em MUNDO")

    # quadrado deslocado para a direita: o bug antigo mostrava bbox a esquerda
    local = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    obj = ed.Objeto2D(local, (255, 255, 0), tipo="poligono")
    obj.compor_matriz(ed.matriz_translacao(200, 200))

    x0, y0, x1, y1 = obj.obter_bbox_mundo()
    imprimir_pontos("vertices", obj.obter_pontos_mundo())
    print(f"  bbox = ({x0}, {y0}, {x1}, {y1})")

    verificar(approx(x0, 199) and approx(x1, 201),
              f"xmin={x0}, xmax={x1} (esperado 199 e 201)")
    verificar(approx(y0, 199) and approx(y1, 201),
              f"ymin={y0}, ymax={y1} (esperado 199 e 201)")

    subtitulo("12.2 Rotacionar e reavaliar bbox")
    obj.compor_matriz(ed.matriz_em_torno_de((200, 200), ed.matriz_rotacao(math.radians(45))))
    x0, y0, x1, y1 = obj.obter_bbox_mundo()
    print(f"  bbox apos rotacao 45 deg = ({x0:.4f}, {y0:.4f}, {x1:.4f}, {y1:.4f})")
    # sqrt(2) ~ 1.4142: bbox do quadrado 2x2 girado 45 eh ~2.828 x 2.828
    largura = x1 - x0
    altura = y1 - y0
    print(f"  largura={largura:.4f}, altura={altura:.4f} (esperado ~2.828)")
    verificar(approx(largura, 2 * math.sqrt(2), tol=1e-6),
              "largura do bbox apos rotacao 45 = 2*sqrt(2)")
    verificar(approx(altura, 2 * math.sqrt(2), tol=1e-6),
              "altura do bbox apos rotacao 45 = 2*sqrt(2)")


# ======================================================================
# MAIN
# ======================================================================
def main():
    print("\n" + "#" * 70)
    print("#  TESTES DAS TRANSFORMACOES DO EDITOR 2D")
    print("#" * 70)

    teste_1_matrizes_elementares()
    teste_2_aplicacao_em_pontos()
    teste_3_composicao_ordem()
    teste_4_rotacao_em_torno_de()
    teste_5_invariantes_rotacao()
    teste_6_area_escala()
    teste_7_objeto_pipeline()
    teste_8_selecao()
    teste_9_camera()
    teste_10_sutherland_hodgman()
    teste_11_cohen_sutherland()
    teste_12_bbox()

    print("\n" + "#" * 70)
    print("#  FIM DOS TESTES")
    print("#" * 70 + "\n")


if __name__ == "__main__":
    main()