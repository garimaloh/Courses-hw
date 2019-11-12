import numpy as np
import matplotlib.pyplot as p
from scipy import integrate


alpha = 0.1
beta = 0.5
K = 3
n = 1
init_x = 4


def model(X, t=0):
    return np.array([beta * (init_x**n/(init_x**n + K**n)) - alpha * X[0]])


t = np.linspace(1, 100, 100)

X0 = np.array([0]) # initial X value

X1 = integrate.odeint(model, X0, t)
n = 2
X2 = integrate.odeint(model, X0, t)
n = 3
X3 = integrate.odeint(model, X0, t)
n = 4
X4 = integrate.odeint(model, X0, t)

p.plot(t, X1.T[0], label='n=1')
p.plot(t, X2.T[0], label='n=2')
p.plot(t, X3.T[0], label='n=3')
p.plot(t, X4.T[0], label='n=4')
p.legend(loc='best')
p.ylabel('X')
p.xlabel('time')
p.show()
