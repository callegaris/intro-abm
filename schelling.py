
import matplotlib.pyplot as plt
from random import random as rand
import numpy as np


def showPlot(end):

    ax.clear()
    # ax.scatter([p.x for p in POP], [p.y for p in POP],
    #            cmap='hot', c=[p.group for p in POP], s=80, vmin=0, vmax=3)
    ax.imshow(HOUSES, cmap='hot', interpolation='nearest', vmin=0, vmax=3)
    ax.axis('off')
    ax.set_aspect(1)
    plt.title("intolerance = %0.2f, ratio = %0.2f, empty = %0.2f" % (INTOLERANCE, RATIO, 1-FULL))

    plt.draw()
    if end:
        plt.pause(0)
    else:
        plt.pause(0.001)


class Person:
    def __init__(self, x, y, group):
        self.x = x
        self.y = y
        self.group = group  # can be 1 or 2

    def do_action(self):
        x = self.x
        y = self.y
        occupied_neighbors = 0
        similar_neighbors = 0

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor = HOUSES[(y + dy) % SIZE][(x + dx) % SIZE]
                if neighbor > 0:
                    occupied_neighbors += 1
                    if neighbor == self.group:
                        similar_neighbors += 1
        occupied_neighbors -= 1  # remove person itself
        similar_neighbors -= 1  # remove person itself

        if similar_neighbors < occupied_neighbors * INTOLERANCE:
            HOUSES[self.y][self.x] = 0
            avail_y, avail_x = np.where(HOUSES == 0)
            choice = int(rand() * len(avail_x))
            self.x = avail_x[choice]
            self.y = avail_y[choice]
            HOUSES[self.y][self.x] = self.group


fig, ax = plt.subplots(1,1)

SIZE = 32
HOUSES = np.zeros([SIZE, SIZE])

FULL = 0.7
NP = int(SIZE * SIZE * FULL)
INTOLERANCE = 0.3
RATIO = 0.25
start_house = range(SIZE*SIZE)
np.random.shuffle(start_house)

POP = [Person(start_house[i] % SIZE, start_house[i] // SIZE, 1+int(rand()<RATIO)) for i in range(NP)]

for p in POP:
    HOUSES[p.y][p.x] = p.group

MAX_TIME = 100000
VIEW_STEP = 100
for TIME in range(MAX_TIME):

    active = int(rand() * NP)

    POP[active].do_action()

    if TIME % VIEW_STEP == 0:
        showPlot(TIME == MAX_TIME-1)



