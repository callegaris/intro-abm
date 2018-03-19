
# Ant foraging model

from random import random as rand
import matplotlib.pyplot as plt
import numpy as np

def showPlot(end):

    ax.clear()
    ax.imshow(FLOOR.grid, cmap='YlGnBu', vmin=0, vmax=20, interpolation='nearest')
    food_mask = np.ma.masked_where(FLOOR.food < Foodbit, FLOOR.food)
    ax.imshow(food_mask, cmap='gray_r', vmin=0, vmax=1, interpolation='nearest')
    # ax.imshow(FLOOR.food, cmap='gray_r', vmin=0, vmax=1, interpolation='nearest', alpha=0.2)
    ax.scatter([a.x for a in AGENTS], [a.y for a in AGENTS],
               cmap='winter', c=[a.searching for a in AGENTS],
               vmin=0, vmax=1)
    # ax.plot([a.x for a in WALKERS], [a.y for a in WALKERS], 'k.')
    ax.set_aspect(1.0)
    ax.axis('off')

    collect.plot(TIME, HOMEFOOD, 'k.')
    collect.set_xlabel('time')
    collect.set_ylabel('food gathered')
    collect.axis([0, MAX_TIME, 0, Nfood_sources])
    collect.set_aspect(1.0*MAX_TIME/Nfood_sources)

    plt.draw()
    if end:
        plt.pause(0)
    else:
        plt.pause(0.01)


class Environment:
    def __init__(self):
        # self.grid = np.ones([SIZE, SIZE]) * 20  # Deneubourg et al. 1990
        self.grid = np.zeros([SIZE, SIZE])
        self.food = np.array([1.0*int(rand()<1.0*Nfood_sources/(SIZE*SIZE))
                              for _ in range(SIZE*SIZE)]).reshape([SIZE, SIZE])
        # self.food[SIZE-1][SIZE-1] = True  # send ants back if they reach corner
        self.next_grid = np.zeros([SIZE, SIZE])

    def add_pheromone(self, y, x):
        self.next_grid[y][x] += 1

    def update(self):
        self.grid += self.next_grid
        self.grid -= Evaporation
        self.next_grid = np.zeros([SIZE, SIZE])

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.k = 10
        self.n = 2
        self.searching = True

    def do_action(self):
        if FLOOR.food[self.y][self.x] > 0:  # ant has found food
            self.searching = False
            FLOOR.food[self.y][self.x] -= Foodbit
        if self.x == 0 and self.y == 0:  # ant is home
            if not self.searching:
                global HOMEFOOD
                HOMEFOOD += Foodbit
            self.searching = True

        # "tunnelling" to home colony
        elif self.x == 0 and self.y == SIZE - 1:
            self.x = 0
            self.y = 0
        elif self.x == SIZE - 1 and self.y == 0:
            self.x = 0
            self.y = 0
        elif self.x == SIZE - 1 and self.y == SIZE - 1:
            self.x = 0
            self.y = 0
        if Always_depositing or not self.searching:
            FLOOR.add_pheromone(self.y, self.x)
        self.anisotropic_move()

    def anisotropic_move(self):
        # "roulette wheel" algorithm
        weights = np.zeros(2)

        if self.searching:
            weights[0] = (self.k + FLOOR.grid[self.y][min([self.x + 1, SIZE - 1])])**self.n
            weights[1] = weights[0] + (self.k + FLOOR.grid[min([self.y + 1, SIZE - 1])][self.x])**self.n
            weights /= weights[1]
            if rand() < weights[0]:
                self.x = min([self.x + 1, SIZE - 1])
            else:
                self.y = min([self.y + 1, SIZE - 1])
        else:
            weights[0] = (self.k + FLOOR.grid[self.y][max([self.x - 1, 0])])**self.n
            weights[1] = weights[0] + (self.k + FLOOR.grid[max([self.y - 1, 0])][self.x])**self.n
            weights /= weights[1]
            if rand() < weights[0]:
                self.x = max([self.x - 1, 0])
            else:
                self.y = max([self.y - 1, 0])


# class Walker:
#     def __init__(self,x,y):
#         self.x = x
#         self.y = y
#     def goToRandomNeighbor(self):
#         r = rand()
#         if r < 0.5:
#             if self.x < SIZE-1:
#                 self.x = self.x + 1
#         else:
#             if self.y < SIZE-1:
#                 self.y = self.y + 1

fig, (ax, collect) = plt.subplots(1,2)

SIZE = 60
HOMEFOOD = 0

Nstart = 1
Ninject = 1
Nmax = 50
Foodbit = 0.1
Always_depositing = False
AGENTS = [Ant(0,0) for _ in range(Nstart)]
# WALKERS = [Walker(0,0) for _ in range(100)]

Nfood_sources = 50
Evaporation = 0.01
FLOOR = Environment()

MAX_TIME = 1000


for TIME in range(MAX_TIME+1):

    showPlot(TIME >= MAX_TIME)

    np.random.shuffle(AGENTS)

    for a in AGENTS:
        a.do_action()
    # for w in WALKERS:
    #     w.goToRandomNeighbor()

    FLOOR.update()
    if len(AGENTS) < Nmax:
        for _ in range(Ninject):
            # AGENTS = np.append(AGENTS, [Ant(0,0)])
            AGENTS.append(Ant(0,0))













