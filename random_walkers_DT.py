
# Simple random walkers in discrete time

from math import *
from random import random as rand
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfinv

# function that plots agents and diagnostics
def showMyScatterPlot(agents, end):

    # scatter plot of agents
    scatt.clear()
    scatt.plot([a.x for a in agents], [a.y for a in agents], 'ms')
    scatt.axis([0,SIZE,0,SIZE])  # axes of the plot
    scatt.set_aspect('equal')  # actual area in which plot appears

    # time series of variance of positions
    var.clear()
    global Nstart
    mean = [0,0]
    for a in agents:
        mean[0] += a.x
        mean[1] += a.y
    mean[0] /= Nstart
    mean[1] /= Nstart
    variance = 0
    for a in agents:
        variance += (a.x - mean[0])**2 + (a.y - mean[1])**2
    variance /= Nstart
    global TIME_VARIANCE
    TIME_VARIANCE.append(variance)
    var.axis([0, TIME_MAX, 0, SIZE])
    var.set_aspect(1.0*TIME_MAX/SIZE)
    var.plot(range(TIME), TIME_VARIANCE, 'r.')

    # the following 3 lines fit a linear regression to variance as a function of time
    Y = TIME_VARIANCE
    X = np.vstack([range(1, TIME+1), np.ones(len(TIME_VARIANCE))]).T
    m, c = np.linalg.lstsq(X, Y)[0]

    var.text(50, 10, "m = %f" % m, fontsize=16)
    var.set_xlabel("time")
    var.set_ylabel("variance")

    plt.subplots_adjust(wspace=0.4)
    plt.draw()
    if end:
        plt.pause(0)  # avoid that plot disappears at the end of the simulation
    else:
        plt.pause(0.1)


# here we define our agents, called "Walker"
class Walker:
    def __init__(self,x,y):
        # agents are characterized by two spatial coordinates
        self.x = x
        self.y = y
    def goToRandomNeighbor(self):
        r = rand()
        if r < 0.5:
            r = rand()
            if r < 0.25:
                self.x = (self.x-1) % SIZE
            elif r < 0.5:
                self.x = (self.x+1) % SIZE
            elif r < 0.75:
                self.y = (self.y-1) % SIZE
            else:
                self.y = (self.y+1) % SIZE



# parameters: spatial domain size, initial number of Walker agents
SIZE = 100
Nstart = 1000

# initialize plots:
# "scatt" for a scatter plot of agent positions
# "var" for the time series of variance of positions
fig, (scatt,var) = plt.subplots(1,2)
TIME_VARIANCE = []  # this list will be filled with position variances for each timestep

# three possible initial conditions here:

# uncomment next line for agents uniformly distributed in domain
#Agents = [Walker(int(rand()*SIZE), int(rand()*SIZE)) for _ in range(Nstart)]

# uncomment next line for agents normally distributed around center of domain
#Agents = [ Walker(50+4*erfinv(2*rand()-1), 50+4*erfinv(2*rand()-1)) for _ in range(Nstart) ]

# uncomment next line for all agents starting in middle of domain
Agents = [Walker(SIZE/2, SIZE/2) for _ in range(Nstart)]

TIME = 0
TIME_MAX = 100

# here the main simulation loop
while TIME < TIME_MAX:
    for a in Agents:
        # each agent does its action
        a.goToRandomNeighbor()
    TIME += 1
    # display state of system
    showMyScatterPlot(Agents, TIME>=TIME_MAX)




