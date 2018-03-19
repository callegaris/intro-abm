import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate

def diff_eqs(IN,t):
    Y = np.zeros(3)
    Y[0] = - beta * IN[0] * IN[1] / Ntot
    Y[1] = beta * IN[0] * IN[1] / Ntot - gamma * IN[1]
    Y[2] = gamma * IN[1]
    return Y

beta = 0.2
gamma = 0.01
fig, ax = plt.subplots(1,1)
IN = [90, 10]
Ntot = 100.
trange = np.arange(0, 100, 0.01)
ode_result = scipy.integrate.odeint(diff_eqs, IN, trange)
ax.plot(trange, ode_result[:, 0], 'b-', label='Susceptible')
ax.plot(trange, ode_result[:, 1], 'r-', label='Infected')
ax.plot(trange, 1-(ode_result[:, 0] + ode_result[:, 1]), 'g-', label='Recovered')
plt.legend()
plt.show()
