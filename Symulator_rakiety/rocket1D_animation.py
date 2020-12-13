from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from pylab import *

# Stałe początkowe
G = 9.8  # acceleration due to gravity, in m/s^2
M = 1.0  # mass of pendulum 1 in kg
L = 2.5 # lengh of... in m
b = 0.1 # stala oporow powietrza
K0 = 100 #m/s**2 ciag silnika poczatkowy
ak = 0.002 # stala zaniku eksponenty ciagu silnika - model eksponencjalny
simulation_time = 140 #s czas symulacji

# definicje równań różniczkowych
def derivs(state, t):

    dydx = np.zeros_like(state)
    # x  0
    dydx[0] = state[1]
    # vx  1
    dydx[1] = 0
    # y  2
    dydx[2] = state[3]
    # vy  3
    dydx[3] = -G + K0 * exp(-ak * t**3) - b * state[3]
    # fi  4
    dydx[4] = state[5]
    # vfi  5
    dydx[5] = -L*G* cos(state[4])

    return dydx

# tworzenie kroku i tablicy czasu
dt = 0.05
t = np.arange(0, simulation_time, dt)

# Początkowe warunki
y0 = L
vy0 = 0.0
x0 = 1000.0
vx0 = 0.0
fi0 = 0
vfi0 = 0.0


# stan początkowy w tabeli
state = [x0, vx0, y0, vy0, fi0, vfi0]

# całkowanie prędkośći by otrzymać kąt
y = integrate.odeint(derivs, state, t)

# obliczanie x i y za pomocą kąta
y1 = y[:, 2]

x1 = y[:, 0]

fi1 = y[:, 4]
# plotowanie animacji
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 6000), ylim=(-1, 6000))
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
    thisx = [x1[i]]
    thisy = [y1[i]]
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text


ani = animation.FuncAnimation(fig, animate, range(1, len(y)),
                              interval=dt*100, blit=True, init_func=init)
plt.show()