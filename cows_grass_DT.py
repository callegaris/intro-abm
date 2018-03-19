
# Cows and Grass in discrete time
# implementing the grass as an agent

from random import random as rand
import matplotlib.pyplot as plt
import numpy as np


def showMyPlot(end):
    # aerial view of grass density and cows
    air_view.clear()
    air_view.plot([a.x for a in AGENTS], [a.y for a in AGENTS], 'rs')
    air_view.imshow(GRASS.grid, cmap='YlGn',
                    vmin=0, vmax=MAX_GRASS,
                    interpolation='nearest')
    air_view.axis('off')
    air_view.set_aspect('equal')

    # demography
    pop.plot(TIME, len(AGENTS), 'm.')
    pop.axis([0, TIME_MAX, 0, SIZE*SIZE])
    pop.set_aspect(1.0*TIME_MAX/(SIZE*SIZE))
    pop.set_xlabel('time')
    pop.set_ylabel('population size')


    plt.draw()
    if end == False:
        plt.pause(0.1)
    else:
        plt.pause(0)


class Cow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # cow metabolic rate (not actually "basal")
        self.BMR = cow_BMR_to_NPP * NPP
        # action probabilities
        self.PM = cow_move_rate
        self.PB = cow_birth_rate
        self.PF = cow_feed_rate
        # we will use this variable to mark cows
        # who could not eat at feeding stage
        self.alive = True

    def doActions(self):
        if rand() < self.PM:
            self.move()
        if rand() < self.PB:
            self.birth()
        if rand() < self.PF:
            self.feed()
        # all cows survive at this stage
        # they will die at feeding stage
        NEXT_AGENTS.append(self)

    def move(self):
        # random walk:
        # this is a "roulette wheel"
        # with 4 equally probable options
        r = rand()
        if r < 0.25:
            self.x = (self.x-1)%SIZE
        elif r < 0.5:
            self.x = (self.x+1)%SIZE
        elif r < 0.75:
            self.y = (self.y-1)%SIZE
        else:
            self.y = (self.y+1)%SIZE

    def birth(self):
        NEXT_AGENTS.append(Cow(self.x, self.y))

    def feed(self):
        GRASS.add_cow_to_list(self)



# one possible solution to the problem of
# many cows in discrete time trying to eat from the same cell
# is to make the grass an active "agent" in the model
# and put it in charge of distributing food to cows
class GrassGrid:
    def __init__(self, init_value):
        self.grid = np.ones([SIZE, SIZE]) * init_value
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
MAX_GRASS = 10
init_grass = MAX_GRASS
cow_BMR_to_NPP = 5.0
cow_move_rate = 0.5
cow_birth_rate = 0.02
cow_feed_rate = 1.0

# set other simulation parameters
SIZE = 30
Ncows_start = 20
TIME_MAX = 1000

# initialize plot
fig, (air_view, pop) = plt.subplots(1, 2)

# initialize grass (also an object) and cows
GRASS = GrassGrid(init_grass)
AGENTS = [Cow(int(rand()*SIZE), int(rand()*SIZE)) for _ in range(Ncows_start)]

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

    # visualize
    showMyPlot(TIME >= TIME_MAX)


