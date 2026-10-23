
import pyglet
from pyglet import shapes
from pyglet.window import mouse


# ---------------------------------------------------------------------------
# Utilitário: "retângulo" com bordas arredondadas feito a partir de
# shapes.Rectangle (corpo) + shapes.Circle (cantos).
# ---------------------------------------------------------------------------
def create_rounded_rect(x, y, width, height, radius, color, batch, group=None):
    """Retorna uma lista de shapes que, juntos, formam um retângulo
    com cantos arredondados. Todos compartilham a mesma referência de
    cor (atualizável depois via set_rounded_rect_color)."""
    r = min(radius, width / 2, height / 2)
    parts = [
        # corpo horizontal (faixa central, largura total menos os cantos)
        shapes.Rectangle(x + r, y, width - 2 * r, height, color=color,
                          batch=batch, group=group),
        # corpo vertical (faixa central, altura total menos os cantos)
        shapes.Rectangle(x, y + r, width, height - 2 * r, color=color,
                          batch=batch, group=group),
        # 4 cantos arredondados
        shapes.Circle(x + r, y + r, r, color=color, batch=batch, group=group),
        shapes.Circle(x + width - r, y + r, r, color=color, batch=batch, group=group),
        shapes.Circle(x + r, y + height - r, r, color=color, batch=batch, group=group),
        shapes.Circle(x + width - r, y + height - r, r, color=color, batch=batch, group=group),
    ]
    return parts


def set_rounded_rect_color(parts, color):
    for shape in parts:
        shape.color = color


# ---------------------------------------------------------------------------
# Slider (barra RGB) com handler arrastável
# ---------------------------------------------------------------------------
class Slider:
    def __init__(self, x, y, width, height, label_text, bar_color,
                 batch, group_track, group_fill, group_handle, group_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = 0  # 0 a 255
        self.dragging = False

        # trilho (fundo) da barra, com bordas arredondadas
        self.track_parts = create_rounded_rect(
            x, y, width, height, radius=height / 2,
            color=(50, 50, 55), batch=batch, group=group_track
        )

        # preenchimento colorido (proporcional ao valor atual)
        self.fill = shapes.Rectangle(x, y, 1, height, color=bar_color,
                                      batch=batch, group=group_fill)

        # handler (o "cursor" que o usuário arrasta)
        self.handle_radius = height / 2 + 6
        self.handle = shapes.Circle(x, y + height / 2, self.handle_radius,
                                     color=(255, 255, 255), batch=batch,
                                     group=group_handle)
        self.handle.opacity = 255

        self.label = pyglet.text.Label(
            f"{label_text}: 0", x=x, y=y + height + 6,
            font_size=12,# bold=True,
            color=(255, 255, 255, 255),
            batch=batch, group=group_text
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
        """Área clicável: a trilha inteira (não só o handler)."""
        pad = 10
        return (self.x - pad <= mx <= self.x + self.width + pad and
                self.y - pad <= my <= self.y + self.height + pad)

    def reset(self):
        self.value = 0
        self._update_visual()


# ---------------------------------------------------------------------------
# Botão retangular arredondado e clicável
# ---------------------------------------------------------------------------
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color,
                 batch, group_shape, group_text, on_click, radius=10):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.color = color
        self.hover_color = hover_color
        self.on_click = on_click

        self.parts = create_rounded_rect(x, y, width, height, radius,
                                          color, batch, group_shape)
        self.label = pyglet.text.Label(
            text, x=x + width / 2, y=y + height / 2,
            anchor_x="center", anchor_y="center",
            font_size=12, #bold=True, 
            color=(255, 255, 255, 255),
            batch=batch, group=group_text
        )

    def hit_test(self, mx, my):
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

    def set_hover(self, hovering):
        set_rounded_rect_color(self.parts, self.hover_color if hovering else self.color)


# ---------------------------------------------------------------------------
# Janela principal
# ---------------------------------------------------------------------------
class RGBWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=480, height=440, caption="Seletor de Cor RGB - pyglet")

        self.batch = pyglet.graphics.Batch()

        # grupos de desenho (ordem define o que fica por cima)
        self.g_bg = pyglet.graphics.Group(order=0)
        self.g_track = pyglet.graphics.Group(order=1)
        self.g_fill = pyglet.graphics.Group(order=2)
        self.g_handle = pyglet.graphics.Group(order=3)
        self.g_shape = pyglet.graphics.Group(order=1)
        self.g_text = pyglet.graphics.Group(order=4)

        pyglet.gl.glClearColor(0.14, 0.14, 0.16, 1)

        margin = 40
        slider_width = self.width - 2 * margin
        slider_height = 18

        self.title_label = pyglet.text.Label(
            "Seletor de Cor RGB", x=margin, y=self.height - 40,
            font_size=18, #bold=True,
            color=(255, 255, 255, 255),
            batch=self.batch, group=self.g_text
        )

        # três sliders: R, G, B
        self.slider_r = Slider(margin, self.height - 110, slider_width, slider_height,
                                "R", (220, 60, 60), self.batch,
                                self.g_track, self.g_fill, self.g_handle, self.g_text)
        self.slider_g = Slider(margin, self.height - 170, slider_width, slider_height,
                                "G", (60, 200, 90), self.batch,
                                self.g_track, self.g_fill, self.g_handle, self.g_text)
        self.slider_b = Slider(margin, self.height - 230, slider_width, slider_height,
                                "B", (70, 120, 230), self.batch,
                                self.g_track, self.g_fill, self.g_handle, self.g_text)
        self.sliders = [self.slider_r, self.slider_g, self.slider_b]
        self.active_slider = None

        # retângulo de preview da cor resultante, com bordas arredondadas
        preview_y = 90
        preview_height = 80
        self.preview_parts = create_rounded_rect(
            margin, preview_y, slider_width, preview_height, radius=16,
            color=(0, 0, 0), batch=self.batch, group=self.g_shape
        )
        self.rgb_label = pyglet.text.Label(
            "RGB = (0, 0, 0)", x=margin + slider_width / 2, y=preview_y + preview_height / 2,
            anchor_x="center", anchor_y="center", font_size=14,# bold=True,
            color=(255, 255, 255, 255), batch=self.batch, group=self.g_text
        )

        # botão de reset
        self.btn_reset = Button(
            margin, 35, 140, 38, "Resetar",
            color=(80, 80, 90), hover_color=(110, 110, 125),
            batch=self.batch, group_shape=self.g_shape, group_text=self.g_text,
            on_click=self.reset_colors
        )

        # botões de minimizar e fechar (canto superior direito)
        btn_size = 30
        pad = 12
        self.btn_close = Button(
            self.width - btn_size - pad, self.height - btn_size - pad,
            btn_size, btn_size, "X",
            color=(180, 60, 60), hover_color=(220, 80, 80),
            batch=self.batch, group_shape=self.g_shape, group_text=self.g_text,
            on_click=self.close, radius=8
        )
        self.btn_minimize = Button(
            self.width - 2 * btn_size - pad * 2, self.height - btn_size - pad,
            btn_size, btn_size, "_",
            color=(80, 80, 90), hover_color=(110, 110, 125),
            batch=self.batch, group_shape=self.g_shape, group_text=self.g_text,
            on_click=self.minimize, radius=8
        )
        self.buttons = [self.btn_reset, self.btn_close, self.btn_minimize]

        self._update_preview()

    # -----------------------------------------------------------------
    # Lógica de cor
    # -----------------------------------------------------------------
    def _update_preview(self):
        r, g, b = self.slider_r.value, self.slider_g.value, self.slider_b.value
        set_rounded_rect_color(self.preview_parts, (r, g, b))
        self.rgb_label.text = f"RGB = ({r}, {g}, {b})"
        print(f"RGB = ({r:3d}, {g:3d}, {b:3d})")

    def reset_colors(self):
        for slider in self.sliders:
            slider.reset()
        self._update_preview()

    # -----------------------------------------------------------------
    # Eventos nativos do pyglet
    # -----------------------------------------------------------------
    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != mouse.LEFT:
            return

        # botões
        for btn in self.buttons:
            if btn.hit_test(x, y):
                btn.on_click()
                return

        # sliders
        for slider in self.sliders:
            if slider.hit_test(x, y):
                self.active_slider = slider
                slider.set_value_from_x(x)
                self._update_preview()
                return

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT and self.active_slider is not None:
            self.active_slider.set_value_from_x(x)
            self._update_preview()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.active_slider = None

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons:
            btn.set_hover(btn.hit_test(x, y))


if __name__ == "__main__":
    window = RGBWindow()
    pyglet.app.run()