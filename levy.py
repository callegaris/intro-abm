
# Random walkers in continuous time

from math import log, cos, sin, pi
from random import random as rand
import matplotlib.pyplot as plt


class Forager:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.nextTime = inverse_cumulant(rand())
    def flight(self):
        # this assumes that agents can travel at any speed they like
        distance = Levy_L * (rand()**(-1./Levy_d))
        angle = 2 * pi * rand()
        self.x += distance * cos(angle)
        self.y += distance * sin(angle)
        self.x = self.x % SIZE
        self.y = self.y % SIZE

def showPlot(end):
    ax.clear()
    ax.plot([a.x for a in Agents], [a.y for a in Agents], 'b^')
    ax.text(SIZE/20, SIZE/20, "t=%f" % TIME, fontsize=14)
    ax.axis([0, SIZE, 0, SIZE])
    ax.set_aspect('equal')
    plt.draw()
    if end:
        plt.pause(0)
    else:
        plt.pause(0.1)


def inverse_cumulant(u):
    return -log(u)/MOVE_RATE


# plot initialization
fig, ax = plt.subplots(1,1)

# parameters
SIZE = 1000
Nstart = 10
MOVE_RATE = 1
Levy_d = 2
Levy_L = 1.

# crate walkers
# Agents = [Walker(int(rand()*SIZE), int(rand()*SIZE)) for i in range(Nstart)]
Agents = [Forager(SIZE/2, SIZE/2) for i in range(Nstart)]

TIME = 0
tview = 0
TIME_MAX = 10000
while TIME < TIME_MAX:
    # find agent who is scheduled for next action
    Agents.sort(key = lambda x: x.nextTime)

    # update simulation time
    TIME = Agents[0].nextTime

    # perform action
    Agents[0].flight()

    # update agent's time to next action
    # (this can be done inside the goToRandomNeighbor() function)
    Agents[0].nextTime = TIME + inverse_cumulant(rand())

    # visualize if needed
    if TIME > tview:
        showPlot(TIME>TIME_MAX)
        tview += 1




