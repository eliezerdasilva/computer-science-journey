import pyglet

# criar a janela.
pyglet.options.dpi_scaling = "stretch"

from pyglet import shapes
from pyglet.gl import glClearColor
from pyglet.window import mouse


# ======================================================================
# 1. A JANELA e o BATCH
# ======================================================================
LARGURA, ALTURA = 520, 460
janela = pyglet.window.Window(LARGURA, ALTURA, caption="Aula 02: ColorPicker RGB")
batch = pyglet.graphics.Batch()

# COR DE FUNDO (glClearColor usa canais em [0,1]).
glClearColor(0.14, 0.14, 0.16, 1.0)


# ======================================================================
# 2. GRUPOS DE DESENHO  (definem a ordem de sobreposição)
# ======================================================================
g_bg     = pyglet.graphics.Group(order=0)
g_track  = pyglet.graphics.Group(order=1)
g_fill   = pyglet.graphics.Group(order=2)
g_handle = pyglet.graphics.Group(order=3)
g_shape  = pyglet.graphics.Group(order=2)
g_text   = pyglet.graphics.Group(order=4)


# ======================================================================
# 3. HELPERS
# ======================================================================
def contem(px, py, x, y, w, h):
    """O clique caiu dentro do retângulo (x, y, w, h)?"""
    return x <= px <= x + w and y <= py <= y + h


def create_rounded_rect(x, y, width, height, radius, color, batch, group=None):
    """Retângulo com cantos arredondados: 2 retângulos + 4 círculos."""
    r = min(radius, width / 2, height / 2)
    parts = [
        shapes.Rectangle(x + r, y, width - 2 * r, height,
                         color=color, batch=batch, group=group),
        shapes.Rectangle(x, y + r, width, height - 2 * r,
                         color=color, batch=batch, group=group),
        shapes.Circle(x + r, y + r, r, color=color, batch=batch, group=group),
        shapes.Circle(x + width - r, y + r, r, color=color, batch=batch, group=group),
        shapes.Circle(x + r, y + height - r, r, color=color, batch=batch, group=group),
        shapes.Circle(x + width - r, y + height - r, r, color=color, batch=batch, group=group),
    ]
    return parts


def set_rounded_rect_color(parts, color):
    for shape in parts:
        shape.color = color


# ======================================================================
# 4. SLIDER (barra RGB arrastável)
# ======================================================================
class Slider:
    def __init__(self, x, y, width, height, label_text, bar_color, batch):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.value = 0
        self.dragging = False

        # trilho com bordas arredondadas
        self.track_parts = create_rounded_rect(
            x, y, width, height, radius=height / 2,
            color=(50, 50, 55), batch=batch, group=g_track
        )

        # preenchimento colorido proporcional ao valor
        self.fill = shapes.Rectangle(x, y, 1, height,
                                     color=bar_color, batch=batch, group=g_fill)

        # handle (cursor arrastável)
        self.handle_radius = height / 2 + 6
        self.handle = shapes.Circle(x, y + height / 2, self.handle_radius,
                                    color=(255, 255, 255),
                                    batch=batch, group=g_handle)

        # rótulo
        self.label = pyglet.text.Label(
            f"{label_text}: 0", x=x, y=y + height + 6,
            font_size=12, color=(255, 255, 255, 255),
            batch=batch, group=g_text
        )
        self.label_text = label_text
        self._update_visual()

    def _update_visual(self):
        rel = self.value / 255
        self.fill.width = max(1, self.width * rel)
        self.handle.x = self.x + self.width * rel
        self.label.text = f"{self.label_text}: {self.value}"

    def set_value_from_x(self, mouse_x):
        rel = (mouse_x - self.x) / self.width
        rel = max(0.0, min(1.0, rel))
        self.value = round(rel * 255)
        self._update_visual()

    def hit_test(self, mx, my):
        pad = 10
        return (self.x - pad <= mx <= self.x + self.width + pad and
                self.y - pad <= my <= self.y + self.height + pad)

    def reset(self):
        self.value = 0
        self._update_visual()


# ======================================================================
# 5. BOTÃO retangular arredondado e clicável
# ======================================================================
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color,
                 batch, on_click, radius=10):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.color = color
        self.hover_color = hover_color
        self.on_click = on_click

        self.parts = create_rounded_rect(x, y, width, height, radius,
                                         color, batch, group=g_shape)
        self.label = pyglet.text.Label(
            text, x=x + width / 2, y=y + height / 2,
            anchor_x="center", anchor_y="center",
            font_size=12, color=(255, 255, 255, 255),
            batch=batch, group=g_text
        )

    def hit_test(self, mx, my):
        return contem(mx, my, self.x, self.y, self.width, self.height)

    def set_hover(self, hovering):
        set_rounded_rect_color(self.parts, self.hover_color if hovering else self.color)


# ======================================================================
# 6. CONSTRUÇÃO DA INTERFACE
# ======================================================================
margin = 40
slider_width = LARGURA - 2 * margin
slider_height = 18

# título
titulo = pyglet.text.Label(
    "Seletor de Cor RGB", x=margin, y=ALTURA - 40,
    font_size=18, color=(255, 255, 255, 255),
    batch=batch, group=g_text
)

# 3 sliders (R, G, B)
slider_r = Slider(margin, ALTURA - 120, slider_width, slider_height,
                  "R", (220, 60, 60), batch)
slider_g = Slider(margin, ALTURA - 180, slider_width, slider_height,
                  "G", (60, 200, 90), batch)
slider_b = Slider(margin, ALTURA - 240, slider_width, slider_height,
                  "B", (70, 120, 230), batch)
sliders = [slider_r, slider_g, slider_b]
active_slider = None  # controle global de arraste




# --- funções de callback ---
def reset_colors():
    for s in sliders:
        s.reset()
    atualizar()


def minimizar():
    janela.minimize()


def fechar():
    janela.close()


# ======================================================================
# Preview da cor resultante + botão Resetar (lado a lado)
# ======================================================================
preview_y    = 100
preview_h    = 80
btn_reset_w  = 140
btn_reset_h  = 38
gap          = 20

preview_w    = slider_width - btn_reset_w - gap

# preview à esquerda
preview_parts = create_rounded_rect(
    margin, preview_y, preview_w, preview_h, radius=16,
    color=(0, 0, 0), batch=batch, group=g_shape
)
rgb_label = pyglet.text.Label(
    "RGB = (0, 0, 0)",
    x=margin + preview_w / 2,
    y=preview_y + preview_h / 2,
    anchor_x="center", anchor_y="center",
    font_size=14, color=(255, 255, 255, 255),
    batch=batch, group=g_text
)

# botão Resetar à direita, centralizado verticalmente com o preview
btn_reset_x = margin + preview_w + gap
btn_reset_y = preview_y + (preview_h - btn_reset_h) / 2

btn_reset = Button(
    btn_reset_x, btn_reset_y,
    btn_reset_w, btn_reset_h, "Resetar",
    color=(80, 80, 90),
    hover_color=(110, 110, 125),
    batch=batch,
    on_click=reset_colors
)

# botões minimizar e fechar (canto superior direito)
btn_size = 30
pad = 12
btn_fechar = Button(LARGURA - btn_size - pad, ALTURA - btn_size - pad,
                    btn_size, btn_size, "X",
                    color=(180, 60, 60), hover_color=(220, 80, 80),
                    batch=batch, on_click=fechar, radius=8)
btn_min = Button(LARGURA - 2 * btn_size - pad * 2, ALTURA - btn_size - pad,
                 btn_size, btn_size, "_",
                 color=(80, 80, 90), hover_color=(110, 110, 125),
                 batch=batch, on_click=minimizar, radius=8)

buttons = [btn_reset, btn_fechar, btn_min]


# ======================================================================
# 7. ATUALIZAÇÃO DO ESTADO
# ======================================================================
def atualizar():
    r = slider_r.value
    print (r)
    g = slider_g.value
    b = slider_b.value
    set_rounded_rect_color(preview_parts, (r, g, b))
    rgb_label.text = f"RGB = ({r}, {g}, {b})"
    print(f"RGB = ({r:3d}, {g:3d}, {b:3d})")


# ======================================================================
# 8. O LOOP DE EVENTOS
# ======================================================================
@janela.event
def on_draw():
    janela.clear()
    batch.draw()


# É chamado quando o usuário pressiona um botão do mouse. é a funcao que reconhece se o click esta dentro do slider ou do botao. 
# Ai ela chama caso o click esteja dentro do slider ou do botao.
@janela.event
def on_mouse_press(x, y, botao, modificadores):
    global active_slider
    if botao != mouse.LEFT:
        return

    # botões primeiro
    for btn in buttons:
        if btn.hit_test(x, y):
            btn.on_click()
            return

    # sliders
    for s in sliders:
        if s.hit_test(x, y):
            active_slider = s
            #Aqui chama a funcao que atualiza o valor do slider de acordo com a posicao do mouse.
            s.set_value_from_x(x)
            atualizar()
            return


@janela.event
def on_mouse_drag(x, y, dx, dy, botoes, modificadores):
    if botoes & mouse.LEFT and active_slider is not None:
        active_slider.set_value_from_x(x)
        atualizar()


@janela.event
def on_mouse_release(x, y, botao, modificadores):
    global active_slider
    if botao == mouse.LEFT:
        active_slider = None


@janela.event
def on_mouse_motion(x, y, dx, dy):
    for btn in buttons:
        btn.set_hover(btn.hit_test(x, y))


@janela.event
def on_key_press(simbolo, modificadores):
    if simbolo == pyglet.window.key.ESCAPE:
        janela.close()


# ======================================================================
# 9. INICIA O LOOP.
# ======================================================================
if __name__ == "__main__":
    atualizar()
    pyglet.app.run()