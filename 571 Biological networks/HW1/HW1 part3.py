from numpy import *
import matplotlib.pyplot as p
from scipy import integrate


def model(X, t=0):
    return array([r1 * X[0] * (1 - ((X[1] + X[0]) / k1)), r2 * X[1] * (1 - ((X[1] + X[0]) / k2))])


t = linspace(0, 50,  100)
X0 = array([10, 10])                     # initials conditions: 10 species 1 and 10 species 2

r1_list = [0.55, 0.98, 0.33, 0.16, 0.78, 0.98]
r2_list = [0.17, 0.67, 0.78, 0.56, 0.78, 0.98]
k1_list = [7.23, 1.39, 4.76, 6.54, 2.93, 5.23]
k2_list = [6.54, 3.87, 3.26, 7.23, 4.78, 1.69]

X_res_list = []
for i in range(6):
    r1 = r1_list[i]
    r2 = r2_list[i]
    k1 = k1_list[i]
    k2 = k2_list[i]
    X_res_list.append(integrate.odeint(model, X0, t))


species1, species2 = X_res_list[0].T
fig, ax = p.subplots(2, 3, sharex='col', sharey='row')
count = 0;
for i in range(2):
    for j in range(3):
        species1, species2 = X_res_list[count].T
        ax[i, j].plot(t, species1, 'r-', label='Species 1')
        ax[i, j].plot(t, species2, 'b-', label='Species 2')
        ax[i,j].set_xlabel('time')
        ax[i,j].set_ylabel('population')
        ax[i, j].grid()
        ax[i, j].set_title('Evolution of Species 1 and Species 2 populations')
        ax[i, j].legend(loc='best')
        str_val = 'r1='+str(r1_list[count])+';r2='+str(r2_list[count])+';k1='+str(k1_list[count])+';k2='+str(k2_list[
                                                                                                             count])
        ax[i, j].text(25, 1.5, str_val, fontsize=12, ha='center')
        count = count + 1


p.show()
"""
p.plot(t, species1, 'r-', label='Species 1')
p.plot(t, species2, 'b-', label='Species 2')
p.grid()
p.legend(loc='best')
p.xlabel('time')
p.ylabel('population')
p.title('Evolution of Species 1 and Species 2 populations')
p.show()
"""
