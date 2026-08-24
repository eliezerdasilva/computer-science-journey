import pyglet
import math

from pyglet import shapes

LARGURA = 800
ALTURA = 600

janela = pyglet.window.Window(
    LARGURA,
    ALTURA,
    caption="Espiral"
)

objetos = []

cx = 400
cy = 300

theta = 0

# =========================
# GERANDO OS PONTOS
# =========================

pontos = []

while theta < 6 * math.pi:

    r = 8 * theta

    x = cx + r * math.cos(theta)
    y = cy + r * math.sin(theta)

    pontos.append((x, y))

    theta += 0.05


print("Pontos criados:", len(pontos))


# =========================
# DESENHANDO AS LINHAS
# =========================

for i in range(len(pontos) - 1):

    x1, y1 = pontos[i]
    x2, y2 = pontos[i + 1]

    linha = shapes.Line(
        x1, y1,
        x2, y2,
        thickness=3,
        color=(255, 255, 255)
    )

    objetos.append(linha)


@janela.event
def on_draw():

    janela.clear()

    for objeto in objetos:
        objeto.draw()


pyglet.app.run()