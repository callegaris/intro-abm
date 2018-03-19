
# Agents with Verhulst death rate in discrete time

from random import random as rand
import matplotlib.pyplot as plt
import numpy as np


def showMyScatterPlot(end):
    scatt.clear()
    # agent numbers can get pretty large
    # so we plot agent density in false colors instead of individual agents
    image = np.zeros([SIZE,SIZE])
    for a in AGENTS:
        image[a.y][a.x] += 1
    scatt.imshow(image, cmap='summer', vmin=0, vmax=AGENTS[0].K, interpolation='nearest')
    scatt.axis('off')
    plt.xlabel('time')
    plt.ylabel('population size')

    pop.plot(TIME, len(AGENTS), 'b.')
    Nmax = SIZE*SIZE*AGENTS[0].K
    pop.axis([0, MAX_TIME + 1, 0, Nmax])
    pop.set_aspect(1.0 * MAX_TIME / Nmax)

    plt.subplots_adjust(wspace=0.4)
    plt.draw()
    if end:
        plt.pause(0)
    else:
        plt.pause(0.1)


class Person:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        # see the course notes at
        # for information on the parameters https://github.com/callegaris/intro-abm
        self.K = 5
        self.PM = 0.5
        self.PB = 0.2
        self.PD = 0.2 * (GRID[self.y][self.x] + 1) / self.K

    def doAction(self):
        if rand() < self.PM:
            self.move()
        if rand() < self.PB:
            self.birth()
        # update death probability according to current density
        self.PD = 0.2 * (GRID[self.y][self.x] + 1) / self.K
        if rand() > self.PD:
            NEXT_AGENTS.append(self)

    def birth(self):
        NEXT_AGENTS.append(Person(self.x, self.y))

    def move(self):
        r = rand()
        if r < 0.25:
            self.x = (self.x-1)%SIZE
        elif r < 0.5:
            self.x = (self.x+1)%SIZE
        elif r < 0.75:
            self.y = (self.y-1)%SIZE
        else:
            self.y = (self.y+1)%SIZE



# initialize plot
fig, (scatt,pop) = plt.subplots(1,2)


# parameters
SIZE = 50  # size of grid for agent density plot
Nstart = 10  # initial number of agents
MAX_TIME = 200
TIME = 0
tshow = 1

# we will use this grid to compute agent densities
# since the death probability is proportional to local density
GRID = np.zeros([SIZE, SIZE])

# initialize agents
AGENTS = [Person(int(rand() * SIZE), int(rand() * SIZE)) for _ in range(Nstart)]
for a in AGENTS:
    GRID[a.y][a.x] += 1

for TIME in range(MAX_TIME+1):

    # create list for next step's agents
    NEXT_AGENTS = []

    # perform actions
    for a in AGENTS:
        a.doAction()

    # udate agents list
    AGENTS = NEXT_AGENTS[:]

    # update agent densities
    GRID = np.zeros([SIZE, SIZE])
    for a in AGENTS:
        GRID[a.y][a.x] += 1

    # visualize
    showMyScatterPlot(TIME == MAX_TIME)
