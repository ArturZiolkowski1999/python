from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from pylab import *

# Stałe początkowe
G = 9.8  # acceleration due to gravity, in m/s^2
M = 1.0  # mass of pendulum 1 in kg
L = 2 # lengh of... in m

# definicje równań różniczkowych
def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    dydx[1] = (-L/M) * state[0]

    dydx[2] = state[3]

    dydx[3] = (-L/M) * state[2]

    dydx[4] = state[5]

    dydx[5] = -L*G* cos(state[4])

    return dydx

# tworzenie kroku i tablicy czasu
dt = 0.05
t = np.arange(0, 20, dt)

# Początkowe warunki
y0 = L
vy0 = 0.0
x0 = 0.0
vx0 = 0.0
fi0 = 0
vfi0 = 0.0


# stan początkowy w tabeli
state = [x0, vx0, y0, vy0, fi0, vfi0]

# całkowanie prędkośći by otrzymać kąt
y = integrate.odeint(derivs, state, t)

# obliczanie x i y za pomocą kąta
y1 = L*sin(y[:, 4])

x1 = L*cos(y[:, 4])

fi1 = y[:, 4]

# plotowanie animacji
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=True, xlim=(-10, 10), ylim=(-10, 10))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [0, x1[i]]
    thisy = [0, y1[i]]
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text


ani = animation.FuncAnimation(fig, animate, range(1, len(y)),
                              interval=dt*1000, blit=True, init_func=init)
plt.show()