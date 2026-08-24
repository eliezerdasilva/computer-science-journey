import pyglet

window = pyglet.window.Window(540, 500, caption="Widget Example")
batch = pyglet.graphics.Batch()
frame = pyglet.gui.Frame(window)

# Carrega imagens para os widgets
unpressed = pyglet.resource.image('button_unpressed.png')
pressed = pyglet.resource.image('button_pressed.png')
hover = pyglet.resource.image('button_hover.png')

# Cria um botão toggle
toggle_button = pyglet.gui.ToggleButton(100, 400, pressed=pressed, 
                                         unpressed=unpressed, hover=hover, 
                                         batch=batch)

def on_toggle(widget, value):
    print(f"Botão alternado: {value}")

toggle_button.set_handler('on_toggle', on_toggle)
frame.add_widget(toggle_button)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()
