from pylab import *


# stale
M0 = 50 #kg masa rakiety
g = 9.81 #m/s**2 przysp ziemskie
K0 = 300 #m/s**2 ciag silnika poczatkowy
ak = 0.001 # stala zaniku eksponenty ciagu silnika - model eksponencjalny
h = 0.01 #s skok
b = 0 # stala oporow powietrza
l = 2 # wysokosc rakiety
simulation_time = 140 #s czas symulacji
number_of_steps = 1800 # liczba krokow


# funkcja przyspieszenia wspolrzednych uogulnionych z pomoca rownaia lagrangea 2
def f_ax(t,x,y,fi,vx,vy,vfi, m, m_prim, k):
    return (m_prim/(2*m)) * l * sin(fi) * vfi + 0.5 *l *cos(fi) * vfi**2 - (m_prim/m) * vx + k * cos(fi) + 0.5 * sin(fi) *l * (-m_prim/(m*(1+0.5*l**2)) * (l*vy*cos(fi)-l*vx*sin(fi)+l**2*vfi+l*sin(fi)*(m_prim/(2*m)*l*sin(fi)*vfi + 0.5*l*cos(fi)*vfi**2 - (m_prim/m) * vx + k *cos(fi)) - l*cos(fi)*(-m_prim/(2*m)*l*cos(fi)*vfi + 0.5*l*sin(fi)*vfi**2 - (m_prim/m) * vy + k * sin(fi)) - 2*k*(x*sin(fi) - y*(cos(fi)))))

def f_ay(t,x,y,fi,vx,vy,vfi, m, m_prim, k):
    return (m_prim/m) * vy - (m_prim/(2*m)) *l * cos(fi) * vfi + 0.5 *l * sin(fi) * vfi**2 + k*sin(fi) - m *g + (- 0.5)*l * cos(fi)*((-m_prim)/(m*(1+0.5*l**2)) * (l*vy*cos(fi)-l*vx*sin(fi)+l**2*vfi+l*sin(fi)*(m_prim/(2*m)*l*sin(fi)*vfi +0.5*l*cos(fi)*vfi**2 - (m_prim/m) * vx + k *cos(fi)) - l*cos(fi)*(-m_prim/(2*m)*l*cos(fi)*vfi +0.5*l*sin(fi)*vfi**2 - (m_prim/m) * vy + k * sin(fi)) - 2*k*(x*sin(fi) - y*(cos(fi)))))

def f_afi(t,x,y,fi,vx,vy,vfi,m, m_prim, k):
    return -m_prim/(m*(1+0.5*l**2)) * (l*vy*cos(fi)-l*vx*sin(fi)+l**2*vfi+l*sin(fi)*(m_prim/(2*m)*l*sin(fi)*vfi +
            0.5*l*cos(fi)*vfi**2 - (m_prim/m) * vx + k *cos(fi)) - l*cos(fi)*(-m_prim/(2*m)*l*cos(fi)*vfi +
            0.5*l*sin(fi)*vfi**2 - (m_prim/m) * vy + k * sin(fi)) - 2*k*(x*sin(fi) - y*(cos(fi))))

# funkcja definiujaca przedkosc otrzymana z rownania lagrangea 2
def f_vx(t,x,y,fi,vx,vy,vfi,m, m_prim, k):
    return vx

def f_vy(t,x,y,fi,vx,vy,vfi,m, m_prim, k):
    return vy

def f_vfi(t,x,y,fi,vx,vy,vfi, m, m_prim, k):
    return vfi

# funkcje do wyliczania masy i jej pochodnej oraz ciagu
def f_k(t):
    return K0 * exp(-ak * t)

def f_m(t):
    return (M0-10) * exp(-ak * t) + 10

def f_dm_dt(t):
    return M0 * (-ak) * exp(-ak * t) + 10 * ak * exp(-ak * t)



# warunki poczatkowe
x0 = 0 #m polozenie poczatkowe
vx0 = 0 #m/s predkosc poczatkowa
y0 = 10
vy0 = 4440
fi0 = pi/2
vfi0 = 0


#tablice z obliczonymi danymi
t = linspace(0, simulation_time, number_of_steps) #s czas od startu do 40 sekundy, 1000 krokow
x = [x0] #tablica polozen x
vx = [vx0] #tablica predkosci x
y = [y0]
vy = [vy0]
fi = [fi0]
vfi = [vfi0]
#definicja ciagu i masy
k = [K0]
m = [M0]
m_prim = [f_dm_dt(0)]


#petla wyliczajaca kolejne elementy tablicy za pomoca metody rundego kutty 4 rzedu
for i in range(len(t) - 1):
    #warunek lotu
    #if (y[i] >= 0):
        #wspolrzedna x
        (t, x, y, fi, vx, vy, vfi)
        K1ax = h * f_ax(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i], k[i])
        K1vx = h * f_vx(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i], k[i])
        K1ay = h * f_ay(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i], k[i])
        K1vy = h * f_vy(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i], k[i])
        K1afi = h * f_afi(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i], k[i])
        K1vfi = h * f_vfi(t[i], x[i], y[i], fi[i], vx[i], vy[i], vfi[i], m[i], m_prim[i], k[i])

        K2ax = h * f_ax(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i], k[i])
        K2vx = h * f_vx(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i], k[i])
        K2ay = h * f_ay(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i], k[i])
        K2vy = h * f_vy(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i], k[i])
        K2afi = h * f_afi(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i], k[i])
        K2vfi = h * f_vfi(t[i] + 0.5 * h, x[i] + K1ax * 0.5, y[i] + K1ay * 0.5, fi[i] + K1afi * 0.5, vx[i] + K1vx * 0.5, vy[i] + K1vy * 0.5, vfi[i] + K1vfi * 0.5, m[i], m_prim[i], k[i])

        K3ax = h * f_ax(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i], k[i])
        K3vx = h * f_vx(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i], k[i])
        K3ay = h * f_ay(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i], k[i])
        K3vy = h * f_vy(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i], k[i])
        K3afi = h * f_afi(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i], k[i])
        K3vfi = h * f_vfi(t[i] + 0.5 * h, x[i] + K2ax * 0.5, y[i] + K2ay * 0.5, fi[i] + K2afi * 0.5, vx[i] + K2vx * 0.5, vy[i] + K2vy * 0.5, vfi[i] + K2vfi * 0.5, m[i], m_prim[i], k[i])

        K4ax = h * f_ax(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i], k[i])
        K4vx = h * f_vx(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i], k[i])
        K4ay = h * f_ay(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i], k[i])
        K4vy = h * f_vy(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i], k[i])
        K4afi = h * f_afi(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i], k[i])
        K4vfi = h * f_vfi(t[i] + h, x[i] + K3ax, y[i] + K3ay, fi[i] + K3afi, vx[i] + K3vx, vy[i] + K3vy, vfi[i] + K3vfi, m[i], m_prim[i], k[i])

        x.append(x[i] + (K1vx + 2 * K2vx + 2 * K3vx + K4vx) / 6.0)
        vx.append(vx[i] + (K1ax + 2 * K2ax + 2 * K3ax + K4ax) / 6.0)
        y.append(y[i] + (K1vy + 2 * K2vy + 2 * K3vy + K4vy) / 6.0)
        vy.append(vy[i] + (K1ay + 2 * K2ay + 2 * K3ay + K4ay) / 6.0)
        fi.append(fi[i] + (K1vfi + 2 * K2vfi + 2 * K3vfi + K4vfi) / 6.0)
        vfi.append(vfi[i] + (K1afi + 2 * K2afi + 2 * K3afi + K4afi) / 6.0)

        #masa , jej pochodna i ciag
        k.append(f_k(i))
        m.append(f_m(i))
        m_prim.append(f_dm_dt(i))
   #

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
plot(t, k)
title("k(t)")
subplot(2, 4, 8)
plot(t, m)
title("m(t)")
show()