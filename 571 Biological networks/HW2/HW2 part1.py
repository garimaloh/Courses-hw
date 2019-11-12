import numpy as np
import matplotlib.pyplot as p
from scipy import integrate


alpha = 0.1
beta = 0.5
K = 3
n = 1
init_x = 0


def model(X, t=0):
    return np.array([beta * (init_x**n/(init_x**n + K**n)) - alpha * X[0]])


t = np.linspace(1, 100, 100)

X0 = np.array([10]) # initial X value

X1 = integrate.odeint(model, X0, t)

p.plot(t, X1.T[0], label='n=1')

p.legend(loc='best')
p.ylabel('X')
p.xlabel('time')
p.show()
