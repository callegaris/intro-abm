
# a simple implementation of
# Conway's Game of Life

import numpy as np
from random import random as rand
import matplotlib.pyplot as plt

# function that displays the cell grid
def showGrid():

    global SUM  # this so that we can update SUM, defined outside this funcion
    
    ax[0].clear()
    # alive cells will be green, dead will be blue
    ax[0].imshow(GoL.Cells, cmap='winter', interpolation='nearest')
    ax[0].axis('off')
    ax[0].set_aspect('equal')

    oldsum = SUM
    SUM = GoL.Cells.sum()
    ax[1].plot([TIME-1,TIME],[oldsum,SUM],'r-')
    ax[1].axis([0,MAXTIME,0,GoL.SIZE*GoL.SIZE])
    ax[1].set_aspect(1.0*MAXTIME/(GoL.SIZE*GoL.SIZE))
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("alive cells")
    plt.subplots_adjust(wspace=0.4)
    plt.draw()
    plt.pause(0.1)

# the state and behavior of all cells is implemented in this class    
class CellGrid:  # cells can be DEAD (0) or ALIVE (1)
    def __init__(self,SIZE):
        # initialize all cells with equal probability (0.5) of being DEAD or ALIVE
        self.Cells = np.array([[(rand()//0.5) for _ in range(SIZE)] for _ in range(SIZE)])
        self.SIZE = SIZE
    def update(self):
        # remember that CELL UPDATES HAVE TO BE INDEPENDENT from each other!
        # do not change the state of any cell until you have applied
        # behavioral rules to all cells
        # (this can be done by copying the grid to use as reference for behavior)
        oldCells = self.Cells.copy()
        S = self.SIZE
        for i in range(S):
            for j in range(S):
                aliveNeighbors = \
                    oldCells[(i-1)%S][(j-1)%S] + oldCells[(i-1)%S][j] + oldCells[(i-1)%S][(j+1)%S] +\
                    oldCells[i][(j-1)%S] + oldCells[i][(j+1)%S] +\
                    oldCells[(i+1)%S][(j-1)%S] + oldCells[(i+1)%S][j] + oldCells[(i+1)%S][(j+1)%S]
                if self.Cells[i][j] == 0 and aliveNeighbors == 3:
                    self.Cells[i][j] = 1
                elif self.Cells[i][j] == 1 and aliveNeighbors < 2:
                    self.Cells[i][j] = 0
                elif self.Cells[i][j] == 1 and aliveNeighbors > 3:
                    self.Cells[i][j] = 0


# set parameters
SIZE = 100  # size of the grid
MAXTIME = 100  # total simulation in timestep units
SUM = 0  # keep statistics of total number of ALIVE (1) cells
TIME = 0

# initialize two plot panels
# which you will reference as ax[0] and ax[1]
fig, ax = plt.subplots(1,2)

# initialize grid
GoL = CellGrid(SIZE)
showGrid()

for TIME in range(MAXTIME):  # main time loop of the simulation
    # 1. calculate all cell states
    GoL.update()
    # 2. display grid at current time
    showGrid()
