
# Cows and Grass in discrete time
# implementing the grass as an agent

from math import sqrt, fabs
from random import random as rand
import matplotlib.pyplot as plt
import numpy as np

def showMyPlot(end):
    # aerial view of grass density and cows
    air_view.clear()
    air_view.scatter([a.x for a in AGENTS], [a.y for a  in AGENTS], label='cows', marker='s', color='r')
    air_view.imshow(GRASS.grid, cmap='YlGn',
                    vmin=0, vmax=MAX_GRASS,
                    interpolation='nearest')
    air_view.axis('off')
    air_view.set_aspect('equal')
    air_view.legend(scatterpoints=1)

    # demography
    pop.plot(TIME, len(AGENTS), 'm.')
    pop.axis([0, TIME_MAX, 0, SIZE*SIZE])
    pop.set_aspect(1.0*TIME_MAX/(SIZE*SIZE))
    pop.set_xlabel('time')
    pop.set_ylabel('population size')

    plt.subplots_adjust(wspace=0.4)
    plt.draw()
    if end == False:
        plt.pause(0.1)
    else:
        plt.pause(0)


def periodic_distance(a, b):
    delta_x = fabs(a.x - b.x)
    if delta_x > SIZE/2:
        delta_x = SIZE - delta_x
    delta_y = fabs(a.y - b.y)
    if delta_y > SIZE/2:
        delta_y = SIZE - delta_y
    return sqrt(delta_x**2 + delta_y**2)


class Cow:
    def __init__(self, x, y, alpha):
        self.x = x
        self.y = y
        # cow metabolic rate (not actually "basal")
        self.BMR = cow_BMR_to_NPP * NPP
        # action probabilities
        self.PB = cow_birth_rate
        self.PF = cow_feed_rate
        # we will use this variable to mark cows
        # who could not eat at feeding stage
        self.alive = True
        # weight exponent
        self.alpha = alpha

    def doActions(self):
        if rand() < self.PB:
            self.birth()
        if rand() < self.PF:
            self.feed()
        self.anisotropic_move()
        # all cows survive at this stage
        # they will die at feeding stage
        NEXT_AGENTS.append(self)

    def anisotropic_move(self):
        # "roulette wheel" algorithm
        weights = self.weight_func()
        r = rand()
        if r >= weights[0]:
            if r < weights[1]:
                self.x = (self.x-1) % SIZE
            elif r < weights[2]:
                self.x = (self.x+1) % SIZE
            elif r < weights[3]:
                self.y = (self.y-1) % SIZE
            else:
                self.y = (self.y+1) % SIZE

    def birth(self):
#        baby_alpha = self.alpha * (1 + 0.1 - 0.2*rand())
        baby_alpha = self.alpha
        NEXT_AGENTS.append(Cow(self.x, self.y, baby_alpha))

    def feed(self):
        GRASS.add_cow_to_list(self)

    def weight_func(self):
        x = self.x
        y = self.y
        W = np.zeros(5)
        W[0] = GRASS.grid[y][x]**self.alpha
        W[1] = W[0] + GRASS.grid[y][(x-1) % SIZE]**self.alpha
        W[2] = W[1] + GRASS.grid[y][(x+1) % SIZE]**self.alpha
        W[3] = W[2] + GRASS.grid[(y-1) % SIZE][x]**self.alpha
        W[4] = W[3] + GRASS.grid[(y+1) % SIZE][x]**self.alpha
        W /= W[4]  # normalize total to 1
        return W


# one possible solution to the problem of
# many cows in discrete time trying to eat from the same cell
# is to make the grass an active "agent" in the model
# and put it in charge of distributing food to cows
class GrassGrid:
    def __init__(self, init_value):
        # self.grid = np.ones([SIZE, SIZE]) * init_value
        self.grid = np.array([rand() for _ in range(SIZE*SIZE)]).reshape([SIZE, SIZE]) * init_value

        # create a (size x size) space for lists of cows to be fed
        self.cow_list = [[[] for _ in range(SIZE)] for _ in range(SIZE)]

    def distribute_food(self):
        for y in range(len(self.cow_list)):
            for x in range(len(self.cow_list[y])):
                n_local_cows = len(self.cow_list[y][x])
                # if more than one cow here, distribute randomly
                # and kill cows left without food
                while n_local_cows > 0:
                    # choose a random cow from those remaining to feed in this cell
                    index_chosen_cow = int(rand() * n_local_cows)
                    chosen_cow = self.cow_list[y][x][index_chosen_cow]
                    # feed the chosen cow
                    self.feed_one_cow(chosen_cow)
                    # remove chosen cow from local list of cows to feed
                    self.cow_list[y][x].pop(index_chosen_cow)
                    n_local_cows -= 1
        # empty cow_list
        self.cow_list = [[[] for _ in range(SIZE)] for _ in range(SIZE)]


    def feed_one_cow(self, this_cow):
        if self.grid[this_cow.y][this_cow.x] > this_cow.BMR:
            self.grid[this_cow.y][this_cow.x] -= this_cow.BMR  # assuming timestep=1
        else:
            this_cow.alive = False

    def add_cow_to_list(self, this_cow):
        self.cow_list[this_cow.y][this_cow.x].append(this_cow)

    def grow(self):
        self.grid += NPP  # assuming timestep=1
        indexes_of_overfull_cells = (self.grid > MAX_GRASS)
        self.grid[indexes_of_overfull_cells] = MAX_GRASS



# # # MAIN SIMULATION BODY # # #

# set grass and cow parameters
NPP = 0.1
MAX_GRASS = 100 * NPP
init_grass = MAX_GRASS
cow_BMR_to_NPP = 10
cow_birth_rate = 0.1
# cow_birth_rate = 0.0
cow_feed_rate = 1.0
cow_alpha = 1.0
Ncows_start = 20
# Ncows_start = 400

# set other simulation parameters
SIZE = 40
TIME_MAX = 200

# initialize plot
fig, (air_view, pop) = plt.subplots(1, 2)

# initialize grass (also an object) and cows
GRASS = GrassGrid(init_grass)
AGENTS = [Cow(int(rand()*SIZE), int(rand()*SIZE), cow_alpha) for _ in range(Ncows_start)]

TIME = 0
showMyPlot(TIME >= TIME_MAX-1)

# simulation loop
for TIME in range(TIME_MAX):

    # update grass
    GRASS.grow()

    # create empty list for next step's agents
    NEXT_AGENTS = []

    # loop over all current agents
    for a in AGENTS:
        a.doActions()

    # feed the cows
    GRASS.distribute_food()

    # only keep agents who survived after feeding
    AGENTS = [a for a in NEXT_AGENTS if a.alive]

    showMyPlot(TIME >= TIME_MAX-1)


