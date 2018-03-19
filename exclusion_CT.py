
# Agents who don't want to stay together in continuous time
# just another way to have an emerging "carrying capacity"

from math import log
from random import random as rand
import matplotlib.pyplot as plt
import numpy as np


def showMyScatterPlot(end):
    scatt.clear()
    scatt.imshow(GRID, cmap='bwr', interpolation='nearest')
    scatt.axis('off')
    scatt.set_aspect('equal')

    pop.plot(TIME, len(Agents), 'b.')
    
    # here is an estimate for the total carrying capacity of the model
    Nmax = SIZE*SIZE/(1 + Agents[0].PD)
    pop.axis([0, MAX_TIME, 0, Nmax])
    pop.set_aspect(1. * MAX_TIME / Nmax)

    plt.draw()
    if end:
        plt.pause(0)
    else:
        plt.pause(0.1)


class Walker:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.PM = 0.01
        self.PB = 0.2
        self.PD = 0.1
        self.TM = TIME - log(rand()) / self.PM
        self.TB = TIME - log(rand()) / self.PB
        self.TD = TIME - log(rand()) / self.PD

    def tellMinTime(self):
        return min([self.TM, self.TB, self.TD])

    def doAction(self):
        if TIME == self.TM:
            self.goToEmptyNeighbor()
            self.TM = TIME - log(rand()) / self.PM
        elif TIME == self.TB:
            self.birth()
            self.TB = TIME - log(rand()) / self.PB
        else:
            self.death()

    def birth(self):
        y, x = self.findEmptyNeighbor()
        if x != -1 and y != -1:
            Agents.append(Walker(x, y))
            GRID[y][x] = 1
            # this can be done also with try/except

    def death(self):
        GRID[self.y][self.x] = 0
        del Agents[0]

    def goToEmptyNeighbor(self):
        # note that because of how matrices are indexed
        # y and x are in "reverse order" when looking into GRID
        # alternatively, you need to transpose GRID before visualizing it
        y, x = self.findEmptyNeighbor()
        if x != -1 and y != -1:
            GRID[self.y][self.x] = 0
            GRID[y][x] = 1
            self.x, self.y = x, y

    def findEmptyNeighbor(self):
        # create empty list in which to save possible movement directions
        emptyNeighbors = []
        # find available locations
        x = self.x
        y = self.y
        if GRID[(y-1)%SIZE][x] == 0:
            emptyNeighbors.append([-1,0])
        if GRID[(y+1)%SIZE][x] == 0:
            emptyNeighbors.append([+1,0])
        if GRID[y][(x-1)%SIZE] == 0:
            emptyNeighbors.append([0,-1])
        if GRID[y][(x+1)%SIZE] == 0:
            emptyNeighbors.append([0,+1])
        n_available = len(emptyNeighbors)
        if n_available > 0:
            # choose a random empty neighbor
            choice = int(rand() * n_available)
            return (y + emptyNeighbors[choice][0])%SIZE, (x + emptyNeighbors[choice][1])%SIZE
        else:
            return -1, -1



# initialize plot
fig, (scatt,pop) = plt.subplots(1,2)

# parameters
SIZE = 25
Nstart = 10
MAX_TIME = 200
TIME = 0
tshow = 1

# create initial agents
Agents = [Walker(int(rand()*SIZE), int(rand()*SIZE)) for _ in range(Nstart)]

# if two or more agents are in the same cell,
# eliminate all except one of them
bad = [False for _ in range(Nstart)]
for i in range(Nstart):
    for j in range(i+1,Nstart):
        if Agents[i].x == Agents[j].x and Agents[i].y == Agents[j].y:
            bad[i] = True
Agents = [Agents[i] for i in range(Nstart) if not bad[i]]

# initialize grid for agent counting
GRID = np.zeros([SIZE, SIZE], dtype='int32')
for a in Agents:
    GRID[a.y][a.x] += 1

while TIME < MAX_TIME and len(Agents)>0:
    Agents.sort(key=lambda x: x.tellMinTime())
    TIME = Agents[0].tellMinTime()
    Agents[0].doAction()
    if TIME > tshow and len(Agents)>0:
        showMyScatterPlot(TIME > MAX_TIME)
        tshow += 1
