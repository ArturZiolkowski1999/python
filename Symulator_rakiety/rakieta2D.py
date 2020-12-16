from pylab import *
import matplotlib.animation as animation

# stale
M0 = 12.284 #kg masa rakiety bez paliwa
MP = 48.4 # masa rakiety z paliwem
g = 9.81 #m/s**2 przysp ziemskie
s = 0.01 # stala zaniku eksponenty ciagu silnika - model eksponencjalny
c = 3000.0 # v spalin
h = 0.05 #s skok
b = 0.2 # stala oporow powietrza
l = 2 # wysokosc rakiety
ro = 1.2 #kg/m**3
Ay = 0.01 #m**2 czolowa powierzchnia rakiety
Ax = 0.4 #m**2 boczna powierzchnia rakiety
Cd = 0.01 # wspolczynnik silu opou
simulation_time = 50 #s czas symulacji
number_of_steps = 1000 # liczba krokow
xrange_right = 1000
xrange_left = -1000
yrange = 3000

# warunki poczatkowe
x0 = 0 #m polozenie poczatkowe
vx0 = 0 #m/s predkosc poczatkowa
y0 = 0
vy0 = 0
fi0 = pi/2 - 0.01
vfi0 = 0


# funkcja przyspieszenia wspolrzednych uogulnionych z pomoca rownaia lagrangea 2
def f_ax(t,x,y,fi,vx,vy,vfi, m, m_prim):
    if y >= 0:
        return s * c * (1.0 - (M0 / m)) * cos(fi) - 0.5 * ro*Ax*Cd*vx**2
    else:
        return 0

def f_ay(t,x,y,fi,vx,vy,vfi, m, m_prim):
    if y >= 0:
        return -g + s * c * (1.0 - (M0/m)) * sin(fi) - 0.5 * ro*Ay*Cd*vy**2
    else:
        return 0

def f_afi(t,x,y,fi,vx,vy,vfi,m, m_prim):
    if y >= 0:
        return  + (l/2) * s * c * (1.0 - (M0 / m)) * cos(fi) * cos(fi)
    else:
        return 0

# funkcja definiujaca przedkosc otrzymana z rownania lagrangea 2
def f_vx(t,x,y,fi,vx,vy,vfi,m, m_prim):
    if y >= 0:
        return vx
    else:
        return 0

def f_vy(t,x,y,fi,vx,vy,vfi,m, m_prim):
    if y >= 0:
        return vy
    else:
        return 0

def f_vfi(t,x,y,fi,vx,vy,vfi, m, m_prim):
    return vfi

# funkcje do wyliczania masy i jej pochodnej oraz ciagu

def f_m(t):
    return M0 + MP * exp(-s * t)

def f_dm_dt(t):
    return -s*(MP * exp(-s * t))





#tablice z obliczonymi danymi
t = np.arange(0, simulation_time, h)
x = [x0] #tablica polozen x
vx = [vx0] #tablica predkosci x
y = [y0]
vy = [vy0]
fi = [fi0]
vfi = [vfi0]
#definicja ciagu i masy
m = [M0 + MP]
m_prim = [f_dm_dt(0)]


#petla wyliczajaca kolejne elementy tablicy za pomoca metody rundego kutty 4 rzedu
for i in range(len(t) - 1):
    #warunek lotu
    #if (y[i] >= 0):
        #wspolrzedna x
        (t, x, y, fi, vx, vy, vfi)
        K1ax = h * f_ax(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i])
        K1vx = h * f_vx(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i])
        K1ay = h * f_ay(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i])
        K1vy = h * f_vy(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i])
        K1afi = h * f_afi(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i])
        K1vfi = h * f_vfi(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i])

        K2ax = h * f_ax(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i])
        K2vx = h * f_vx(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i])
        K2ay = h * f_ay(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i])
        K2vy = h * f_vy(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i])
        K2afi = h * f_afi(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i])
        K2vfi = h * f_vfi(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i])

        K3ax = h * f_ax(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i])
        K3vx = h * f_vx(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i])
        K3ay = h * f_ay(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i])
        K3vy = h * f_vy(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i])
        K3afi = h * f_afi(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i])
        K3vfi = h * f_vfi(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i])

        K4ax = h * f_ax(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i])
        K4vx = h * f_vx(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i])
        K4ay = h * f_ay(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i])
        K4vy = h * f_vy(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i])
        K4afi = h * f_afi(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i])
        K4vfi = h * f_vfi(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i])

        x.append(x[i] + (K1vx + 2 * K2vx + 2 * K3vx + K4vx) / 6.0)
        vx.append(vx[i] + (K1ax + 2 * K2ax + 2 * K3ax + K4ax) / 6.0)
        y.append(y[i] + (K1vy + 2 * K2vy + 2 * K3vy + K4vy) / 6.0)
        vy.append(vy[i] + (K1ay + 2 * K2ay + 2 * K3ay + K4ay) / 6.0)
        fi.append(fi[i] + (K1vfi + 2 * K2vfi + 2 * K3vfi + K4vfi) / 6.0)
        vfi.append(vfi[i] + (K1afi + 2 * K2afi + 2 * K3afi + K4afi) / 6.0)

        #masa , jej pochodna i ciag
        m.append(f_m(i))
        m_prim.append(f_dm_dt(i))


subplot(2, 4, 1)
plot(t, y)
title("y(t)")
subplot(2, 4, 5)
plot(t, vy)
title("vy(t)")
subplot(2, 4, 2)
plot(t, x)
title("x(t)")
subplot(2, 4, 6)
plot(t, vx)
title("vx(t)")
subplot(2, 4, 3)
plot(t, fi)
title("fi(t)")
subplot(2, 4, 7)
plot(t, vfi)
title("vfi(t)")
subplot(2, 4, 4)
plot(t, m_prim)
title("m'(t)")
subplot(2, 4, 8)
plot(t, m)
title("m(t)")


fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(xrange_left, xrange_right), ylim=(-1, yrange))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], 'x-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [x[i]]
    thisy = [y[i]]
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*h))
    return line, time_text


ani = animation.FuncAnimation(fig, animate, len(y),
                              interval=h*100, blit=True, init_func=init)
plt.show()