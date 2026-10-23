import pyglet
import pyglet.gl as gl

#display = pyglet.display.get_display()
#screen = display.get_default_screen()
config = gl.Config(double_buffer=True)
window = pyglet.window.Window(config=config, style=pyglet.window.Window.WINDOW_STYLE_DIALOG)
window.set_caption("Aula 02: ColorPicker RGB")
#window.set_fullscreen(True)
#window = pyglet.window.Window(resizable=True) Pode redirecionar para fullscreen, mas o mouse nao funciona direito.
window.set_minimum_size(320, 200)
window.set_maximum_size(1024, 768)
window.set_location(600, 100)
tipoCursor = window.get_system_mouse_cursor(window.CURSOR_HAND)
window.set_mouse_cursor(tipoCursor)
# Configuração mais simples
config = gl.Config(double_buffer=True, depth_size=24)
batch = pyglet.graphics.Batch()

pyglet.app.run()