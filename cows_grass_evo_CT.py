
# Cows and Grass in continuous time

from math import log
from random import random as rand
import matplotlib.pyplot as plt
import numpy as np


def showMyPlot(end):
    # aerial view of grass density and cows
    air_view.clear()
    air_view.plot([a.x for a in Agents], [a.y for a in Agents], 'rs')
    air_view.imshow(Grass, cmap='Greens',
                    vmin=0, vmax=maxGrass,
                    interpolation='nearest')
    air_view.axis('off')
    air_view.set_aspect('equal')

    # demography
    pop.plot(t, len(Agents), 'm.')
    pop.axis([0, tmax, 0, SIZE*SIZE])
    pop.set_aspect(1.0*tmax/(SIZE*SIZE))
    pop.set_xlabel('time')
    pop.set_ylabel('population size')

    # evolving movement rate
    rates = np.array([a.PM for a in Agents])
    stats.plot(t, rates.mean(), 'g.')
    stats.axis([0, tmax, 0, 1])
    stats.set_aspect(1.0*tmax)
    stats.set_xlabel('time')
    stats.set_ylabel('mean movement rate')

    plt.draw()
    if end == False:
        plt.pause(0.1)
    else:
        plt.pause(0)


class Cow:
    def __init__(self, x, y, move_rate):
        self.x = x
        self.y = y
        # cow metabolic rate (not actually "basal")
        self.BMR = cow_BMR_to_NPP * NPP
        # action rates
        self.PM = move_rate
        self.PB = cow_birth_rate
        self.PF = cow_feed_rate
        # waiting times
        self.TM = t - log(rand())/self.PM
        self.TB = t - log(rand())/self.PB
        self.TF = t - log(rand())/self.PF
        # this is needed to accumulate energy requirement
        self.time_of_last_meal = t

    def tellMinWaitTime(self):
        return min([self.TM, self.TB, self.TF])

    def doActions(self):
        if t == self.TM:
            self.move()
        elif t == self.TB:
            self.birth()
        else:
            self.feed()

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
        self.TM = t - log(1-rand())/self.PM

    def birth(self):
        # baby's movement rate is equal to
        # mother's plus a number between -cow_variation and +cow_variation
        baby_move_rate = max([min([self.PM - cow_variation + 2*cow_variation*rand(), 1.0]), 1.e-6])
        Agents.append(Cow(self.x, self.y, baby_move_rate))
        self.TB = t - log(1-rand())/self.PB

    def feed(self):
        delta_t = t - self.time_of_last_meal
        energy_need = self.BMR * delta_t
        if Grass[self.y][self.x] >= energy_need:
            Grass[self.y][self.x] -= energy_need
            self.time_of_last_meal = t
            self.TF = t - log(1-rand())/self.PF
        else:
            self.death()

    def death(self):
        del Agents[0]



# # # MAIN SIMULATION BODY # # #

# set grass and cow parameters
NPP = 0.1
maxGrass = 10
cow_BMR_to_NPP = 5.0
cow_move_rate = 0.5
cow_birth_rate = 0.05
cow_feed_rate = 1.0
cow_variation = 0.2

# set other simulation parameters
SIZE = 30
Ncows_start = 20
t = 0
tmax = 1000
tshow = 1
time_of_last_grass_growth = t

# initialize plot
fig, (air_view, pop, stats) = plt.subplots(1, 3)

# initialize grass and cows
Grass = np.ones([SIZE, SIZE]) * maxGrass
Agents = [Cow(int(rand()*SIZE), int(rand()*SIZE), cow_move_rate) for _ in range(Ncows_start)]

# simulation loop
while t < tmax and len(Agents) > 0:

    # find first agent scheduled for action
    # by using method tellMinWaitTime
    # as custom sorting key
    Agents.sort(key = lambda x: x.tellMinWaitTime())

    # update actual simulation time
    t = Agents[0].tellMinWaitTime()

    # do action
    Agents[0].doActions()

    # update grass
    delta_t_grass = t - time_of_last_grass_growth
    Grass = Grass + NPP * delta_t_grass
    indexes_of_overfull_cells = (Grass > maxGrass) # "True" where condition is verified
    Grass[indexes_of_overfull_cells] = maxGrass
    time_of_last_grass_growth = t

    # visualize if needed
    if t > tshow:
        showMyPlot(t >= tmax)
        tshow += 1


