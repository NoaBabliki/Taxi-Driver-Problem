import matplotlib.pyplot as plt
import numpy as np

i = 0

def fig1(fig):
    ax = fig.add_subplot(111)
    ax.plot(x, np.sin(x))


def fig2(fig):
    ax = fig.add_subplot(111)
    ax.plot(x, np.cos(x))


def fig3(fig):
    ax = fig.add_subplot(111)
    ax.plot(x, np.tan(x))


def fig4(fig):
    ax1 = fig.add_subplot(311)
    ax1.plot(x, np.sin(x))
    ax2 = fig.add_subplot(312)
    ax2.plot(x, np.cos(x))
    ax3 = fig.add_subplot(313)
    ax3.plot(x, np.tan(x))

switch_figs = {
    0: fig1,
    1: fig2,
    2: fig3,
    3: fig4
}  # dictionary

def onclick1(fig):
    global i
    print(i)
    fig.clear()
    i += 1
    i %= 4
    switch_figs[i](fig)
    plt.draw()

x = np.linspace(0, 2*np.pi, 1000)
fig = plt.figure()

switch_figs[0](fig)


fig.canvas.mpl_connect('button_press_event', lambda event: onclick1(fig))

plt.show()