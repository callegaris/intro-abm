
# Simple random walkers in continuous time

from math import log
from random import random as rand
import matplotlib.pyplot as plt


class Walker:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        # waiting time for the first action of this agent
        self.nextTime = inverse_cumulant(rand())
    def goToRandomNeighbor(self):
        r = rand()
        if r < 0.25:
            self.x = (self.x-1) % SIZE
        elif r < 0.5:
            self.x = (self.x+1) % SIZE
        elif r < 0.75:
            self.y = (self.y-1) % SIZE
        else:
            self.y = (self.y+1) % SIZE

def showMyScatterPlot(end):
    ax.clear()
    ax.plot([a.x for a in Agents], [a.y for a in Agents], 'b^')
    ax.text(SIZE/20, SIZE*104/100, "time: %f" % TIME, fontsize=14)
    ax.axis([0,SIZE,0,SIZE])  # axes of the plot
    ax.set_aspect('equal')  # actual area in which plot appears
    plt.draw()
    if end:
        plt.pause(0)
    else:
        plt.pause(0.1)

# this function is needed for the Gillespie algorithm (see notes)
def inverse_cumulant(u):
    return -log(1-u)/MOVE_RATE


# plot initialization
fig, ax = plt.subplots(1,1)

# parameters
SIZE = 100
Nstart = 100
MOVE_RATE = 1 # how often do agents move?

# crate walkers
Agents = [Walker(int(rand()*SIZE), int(rand()*SIZE)) for i in range(Nstart)]

TIME = 0
tview = 0  # you can set this to be >0 if you don't want to visualize each action
TIME_MAX = 10000
while TIME < TIME_MAX:
    # find agent who is scheduled for next action
    # by sorting the agents according to which one has the lowest time of next action
    Agents.sort(key = lambda x: x.nextTime)

    # update simulation time
    TIME = Agents[0].nextTime

    # perform action
    Agents[0].goToRandomNeighbor()

    # update agent's time to next action
    # (this can be done inside the goToRandomNeighbor() function if you like)
    Agents[0].nextTime = TIME + inverse_cumulant(rand())

    # visualize if needed
    if TIME > tview:
        showMyScatterPlot(TIME>TIME_MAX)
        tview += 1




