from pylab import *

# stale
m = 50 #kg masa rakiety
g = 9.81 #m/s**2 przysp ziemskie
K0 = 300 #m/s**2 ciag silnika poczatkowy
ak = 0.002 # stala zaniku eksponenty ciagu silnika - model eksponencjalny
h = 0.01 #s skok
b = 0.1 # stala oporow powietrza


#parametry poczatkowe
x0 = 0 #m polozenie poczatkowe
v0 = 0 #m/s predkosc poczatkowa

# tablice z zmiennymi
t = linspace(0, 1100, 8000) #s czas od startu do 10 sekundy, 1000 krokow
x = [x0] #tablica polozen
v = [v0] #tablica predkosci
k = [K0] # tablicu ciagu silnika

def K(t):
    return K0 * exp(-ak * t)

# funkcja definiujaca przyspieszenie otrzymana z pomoca rownaia lagrangea 2
def a(t, x, v):
    if v >= -0.1:
        return -g + K0 * exp(-ak * t**3) - b * v
    else:
        return -g + K0 * exp(-ak * t**3) - 10*b * v # funkcja na pale lepiej gdy v sie zmniejsza


# funkcja definiujaca przedkosc otrzymana z rownania lagrangea 2
def dx_dt(t, x, v):
    return v

#petla wyliczajaca kolejne elementy tablicy za pomoca metody rundego kutty 4 rzedu

for i in range(len(t) - 1):
    if (x[i] >= 0):
        K1f = h * a(t[i], x[i], v[i])
        K1r = h * dx_dt(t[i], x[i], v[i])
        K2f = h * a(t[i] + 0.5 * h, x[i] + K1f * 0.5, v[i] + K1r * 0.5)
        K2r = h * dx_dt(t[i] + 0.5 * h, x[i] + K1f * 0.5, v[i] + K1r * 0.5)
        K3f = h * a(t[i] + 0.5 * h, x[i] + K2f * 0.5, v[i] + K2r * 0.5)
        K3r = h * dx_dt(t[i] + 0.5 * h, x[i] + K2f * 0.5, v[i] + K2r * 0.5)
        K4f = h * a(t[i] + h, x[i] + K3f, v[i] + K3r)
        K4r = h * dx_dt(t[i] + h, x[i] + K3f, v[i] + K3r)
        x.append(x[i] + (K1r + 2 * K2r + 2 * K3r + K4r) / 6.0)
        v.append(v[i] + (K1f + 2 * K2f + 2 * K3f + K4f) / 6.0)
        k.append(K(i))
    else:
        x.append(0)
        v.append(0)
        k.append(K(i))



subplot(1, 3, 1)
plot(t, x, label="x(t)")
legend()
subplot(1, 3, 2)
plot(t, v, label="v(t)")
legend()
subplot(1, 3, 3)
plot(t, k, label="K(t)")
legend()
show()