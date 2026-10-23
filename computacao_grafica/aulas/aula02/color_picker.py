import pyglet

# criar a janela.
pyglet.options.dpi_scaling = "stretch"

from pyglet import shapes
from pyglet.gl import glClearColor


# ======================================================================
# 1. A JANELA e o BATCH  (pronto — como na Aula 01)
# ======================================================================
LARGURA, ALTURA = 520, 380
janela = pyglet.window.Window(LARGURA, ALTURA, caption="Aula 02: ColorPicker (a completar)")
batch = pyglet.graphics.Batch()

# COR DE FUNDO (livre — mude se quiser). glClearColor usa canais em [0,1].
glClearColor(0.16, 0.16, 0.18, 1.0)


# ======================================================================
# 2. HELPER pronto (fornecido)  ->  o clique caiu dentro de um retangulo?
# ======================================================================
# No pyglet, (px,py) do mouse ja vem no mesmo sistema do desenho (origem no
# canto inferior-esquerdo). Entao o teste de "clique dentro do retangulo" e so
# uma comparacao de caixa (bounding box). Use isto para saber se o clique caiu
# sobre um slider ou sobre o botao de reset.
def contem(px, py, x, y, w, h):
    return x <= px <= x + w and y <= py <= y + h


r, g, b = 0, 128, 128


amostra = shapes.BorderedRectangle(190, 60, 140, 70, border=2,
                                   color=(r, g, b), border_color=(90,0, 255),
                                   batch=batch)


def atualizar():
    
    amostra.color = (r, g, b)        
    print(f"RGB = ({r:3d}, {g:3d}, {b:3d})")


# ======================================================================
# 4. O LOOP DE EVENTOS
# ======================================================================
@janela.event
def on_draw():
    janela.clear()
    batch.draw()


#@janela.event
#def on_mouse_press(x, y, botao, modificadores):
     



@janela.event
def on_key_press(simbolo, modificadores):
    if simbolo == pyglet.window.key.ESCAPE:
        janela.close()


# ======================================================================
# 5. INICIA O LOOP.
# ======================================================================
if __name__ == "__main__":
    atualizar()          # sincroniza o estado inicial (e imprime no terminal)
    pyglet.app.run()
