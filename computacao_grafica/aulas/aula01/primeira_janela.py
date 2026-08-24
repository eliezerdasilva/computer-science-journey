import pyglet
import math
from pyglet.gl import *
 
pyglet.options.dpi_scaling = "stretch"
from pyglet import shapes

LARGURA, ALTURA = 800, 600
janela = pyglet.window.Window(LARGURA, ALTURA, caption="Aula 01: Primeira janela")

batch = pyglet.graphics.Batch()

COR_CIRCULO = (46, 204, 113)      
cores_ciclo = [(46, 204, 113), (155, 89, 182), (241, 196, 15), (26, 188, 156)]
indice_cor = 0

circulo = shapes.Circle(x=200, y=300, radius=60, color=COR_CIRCULO, batch=batch)
quadrado = shapes.Rectangle(x=380, y=260, width=80, height=80,
                            color=(52, 152, 219), batch=batch)
triangulo = shapes.Triangle(x=560, y=240, x2=720, y2=240, x3=640, y3=380,
                            color=(231, 76, 60), batch=batch)
linha = shapes.Line(50, 50, 750, 50, thickness=3, color=(149, 165, 166),
                    batch=batch)

pontos_do_mouse = []

CENTRO_X = janela.width // 2   
CENTRO_Y = janela.height // 2  
TAMANHO_EIXO = 300

linha_x = pyglet.shapes.Line(
    CENTRO_X - TAMANHO_EIXO, CENTRO_Y,  
    CENTRO_X + TAMANHO_EIXO, CENTRO_Y,  
    color=(255, 0, 0), 
    batch=batch                 
)

linha_y = pyglet.shapes.Line(
    CENTRO_X, CENTRO_Y - TAMANHO_EIXO,  
    CENTRO_X, CENTRO_Y + TAMANHO_EIXO,  
    color=(0, 255, 0),  
    batch=batch                  
)

circulo_azul = pyglet.shapes.Circle(

    00, 300,
    100,
    color=(50, 150, 255),
    segments=36,
    batch=batch
)

# Espiral
cx, cy = 400, 300
pontos = []
objetosLinhas = []
theta = 0.0
while theta < 6 * math.pi:
    r = 8.0 * theta
    x = cx + r * math.cos(theta)
    y = cy + r * math.sin(theta)
    pontos.append((x, y))
    theta += 0.05

for i in range(len(pontos) - 1):
    linha = pyglet.shapes.Line(pontos[i][0], pontos[i][1],
                              pontos[i+1][0], pontos[i+1][1],
                              thickness=3, color=(149, 165, 166), batch=batch)
    objetosLinhas.append(linha)

for x, y in pontos:
    pyglet.shapes.Circle(x, y, radius=2, color=(255, 0, 0), batch=batch)

@janela.event
def on_key_press(simbolo, modificadores):
    global indice_cor
    if simbolo == pyglet.window.key.C:
        indice_cor = (indice_cor + 1) % len(cores_ciclo)
        circulo.color = cores_ciclo[indice_cor]
    elif simbolo == pyglet.window.key.RIGHT:
        quadrado.x += 20
    elif simbolo == pyglet.window.key.LEFT:
        quadrado.x -= 20
    elif simbolo == pyglet.window.key.UP:
        quadrado.y += 20
    elif simbolo == pyglet.window.key.DOWN:
        quadrado.y -= 20
    elif simbolo == pyglet.window.key.ESCAPE:
        janela.close()

@janela.event
def on_mouse_press(x, y, botao, modificadores):
    ponto = shapes.Circle(x=x, y=y, radius=5, color=(236, 240, 241), batch=batch)
    pontos_do_mouse.append(ponto)
    print(f"clique em ({x}, {y})   ->   {len(pontos_do_mouse)} ponto(s)")

@janela.event
def on_draw():
    glClearColor(0.8, 0.1, 0.1, 1.0)
    janela.clear()
    for objeto in objetosLinhas:
            objeto.draw()
    batch.draw()

# Atividae D
circulos_desenhados = []
pontos_do_mouse_circulo = []
@janela.event
def on_mouse_press(x, y, botao, modificadores):
    # A coordenada do pyget é invertida em relação ao OpenGl
    # Coordenadas originais (origem embaixo)
    print(f"Pyglet: x={x}, y={y}")
    
    # Converter para origem no topo
    y_top = ALTURA - y
    print(f"Top-down: x={x}, y={y_top}")
    
    # Criar ponto na posição convertida
    ponto = shapes.Circle(x=x, y=y_top, radius=5, 
                          color=(236, 0, 241), batch=batch)
    pontos_do_mouse.append(ponto)
    pontos_do_mouse_circulo.append((x, y))  # Armazena o ponto para o círculo
    if len(pontos_do_mouse_circulo) == 2:
        x1, y1 = pontos_do_mouse_circulo[0]  # Primeiro clique (centro)
        x2, y2 = pontos_do_mouse_circulo[1]  # Segundo clique (ponto na borda)
        
        # Calcula o raio (distância entre os dois pontos)
        raio = math.hypot(x2 - x1, y2 - y1)
        
        # Cria o círculo
        circulo = shapes.Circle(x=x1, y=y1, radius=raio, 
                                color=(255, 255, 255), batch=batch)
        circulos_desenhados.append(circulo)
        
        # Limpa a lista para o próximo par
        pontos_do_mouse_circulo.clear()
        
        print(f"Círculo criado: centro=({x1}, {y1}), raio={raio:.2f}")


if __name__ == "__main__":
    pyglet.app.run()