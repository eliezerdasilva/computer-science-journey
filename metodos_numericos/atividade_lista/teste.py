<<<<<<< Updated upstream
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Valores iniciais
p_a = 0.5
p_b_a = 0.8
p_b = 0.6

# Fórmula de Bayes

def bayes(p_a, p_b_a, p_b):
    return (p_b_a * p_a) / p_b

# Criação da figura
fig, ax = plt.subplots(figsize=(8,5))
plt.subplots_adjust(left=0.15, bottom=0.35)

# Valor inicial
resultado = bayes(p_a, p_b_a, p_b)

# Gráfico
barra = ax.bar(['P(A|B)'], [resultado])
ax.set_ylim(0, 1)
ax.set_ylabel('Probabilidade')
ax.set_title('Teorema de Bayes Interativo')

# Sliders
ax_p_a = plt.axes([0.15, 0.22, 0.7, 0.03])
ax_p_b_a = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_p_b = plt.axes([0.15, 0.08, 0.7, 0.03])

slider_p_a = Slider(ax_p_a, 'P(A)', 0.01, 1.0, valinit=p_a)
slider_p_b_a = Slider(ax_p_b_a, 'P(B|A)', 0.01, 1.0, valinit=p_b_a)
slider_p_b = Slider(ax_p_b, 'P(B)', 0.01, 1.0, valinit=p_b)

# Atualização do gráfico

def atualizar(val):
    novo_p_a = slider_p_a.val
    novo_p_b_a = slider_p_b_a.val
    novo_p_b = slider_p_b.val

    resultado = bayes(novo_p_a, novo_p_b_a, novo_p_b)

    # Evita probabilidades maiores que 1
    resultado = min(resultado, 1)

    barra[0].set_height(resultado)
    ax.set_title(f'Teorema de Bayes Interativo\nP(A|B) = {resultado:.3f}')

    fig.canvas.draw_idle()

# Eventos dos sliders
slider_p_a.on_changed(atualizar)
slider_p_b_a.on_changed(atualizar)
slider_p_b.on_changed(atualizar)

=======
import math
import matplotlib.pyplot as plt

def normal_pdf(x, mu=0, sigma=1):
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-(x-mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma))

xs = [x / 10.0 for x in range(-50, 50)]

plt.plot(xs, [normal_pdf(x, sigma=1) for x in xs], '-', label='mu=0,sigma=1')
plt.plot(xs, [normal_pdf(x, sigma=2) for x in xs], '--', label='mu=0,sigma=2')
plt.plot(xs, [normal_pdf(x, sigma=0.5) for x in xs], ':', label='mu=0,sigma=0.5')
plt.plot(xs, [normal_pdf(x, mu=-1) for x in xs], '-.', label='mu=-1,sigma=1')

plt.legend()
plt.title("Various Normal pdfs")
plt.xlabel("x")
plt.ylabel("Probability density")
>>>>>>> Stashed changes
plt.show()