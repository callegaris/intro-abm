
# Boids in discrete time

from math import pi, cos, sin, fabs, sqrt, atan2
from random import random as rand
import matplotlib.pyplot as plt
import numpy as np


def showPlot(end):
    ax.clear()
    for a in AGENTS:
        ax.arrow(a.x, a.y, a.v * cos(a.theta), a.v * sin(a.theta),
                 fc='m', ec='m', head_width=a.v, head_length=a.v)
    ax.axis([0, SIZE, 0, SIZE])
    ax.set_aspect(1.0)

    # distance distribution
    # corr.clear()
    # dist_list = np.zeros(len(AGENTS)*(len(AGENTS)-1)/2)
    # idx = 0
    # for i in range(len(AGENTS)):
    #     for j in range(i+1, len(AGENTS)):
    #         a = AGENTS[i]
    #         b = AGENTS[j]
    #         dist_list[idx] = periodic_distance(a, b)
    #         idx += 1
    # corr.hist(dist_list, SIZE / 5, normed=True)
    # corr.axis([0, SIZE, 0, .1])
    # corr.set_aspect(SIZE/0.1)

    global avg_dist
    avg_dist /= Nagents * (Nagents - 1)

    corr.plot(TIME, avg_dist, 'k.')
    corr.axis([0, TIME_MAX, 0, SIZE])
    corr.set_aspect(1.0*TIME_MAX/SIZE)
    corr.set_xlabel("time")
    corr.set_ylabel("average distance")

    plt.subplots_adjust(wspace=0.4)
    plt.draw()
    if end:
        plt.pause(0)
    else:
        plt.pause(0.01)


class Fish:
    def __init__(self, x, y):
        self.v = SPEED
        self.e = ETA
        self.d = PERCEPTION_DISTANCE

        self.x = x
        self.y = y
        self.theta = rand() * 2 * pi - pi

        self.next_x = self.x
        self.next_y = self.y
        self.next_theta = self.theta

    def do_actions(self):
        self.adjust_direction()
        self.move()

    def adjust_direction(self):
        n = 0
        avg_cos = 0
        avg_sin = 0
        for a in AGENTS:
            if a is not self:
                D = periodic_distance(a, self)
                global avg_dist
                avg_dist += D
                if D < self.d:
                    avg_cos += cos(a.theta)
                    avg_sin += sin(a.theta)
                    n += 1
        if n > 0:
            avg_cos /= n
            avg_sin /= n
            self.next_theta = atan2(avg_sin, avg_cos)
            self.next_theta += self.e * (1.0 - 2.0 * rand())
        else:
            self.next_theta = self.theta + self.e * (1.0 - 2.0 * rand())

    def move(self):
        self.next_x = (self.x + self.v * cos(self.theta)) % SIZE
        self.next_y = (self.y + self.v * sin(self.theta)) % SIZE

    def update(self):
        self.x = self.next_x
        self.y = self.next_y
        self.theta = self.next_theta


def periodic_distance(a, b):
    delta_x = fabs(a.x - b.x)
    if delta_x > SIZE/2:
        delta_x = SIZE - delta_x
    delta_y = fabs(a.y - b.y)
    if delta_y > SIZE/2:
        delta_y = SIZE - delta_y
    return sqrt(delta_x**2 + delta_y**2)


fig, (ax, corr) = plt.subplots(1, 2)

SIZE = 100

SPEED = 1
PERCEPTION_DISTANCE = SIZE/20.
ETA = 0.1 * (2 * pi)

Nagents = 100
AGENTS = [Fish(rand()*SIZE, rand()*SIZE) for _ in range(Nagents)]

TIME_MAX = 1000

for TIME in range(TIME_MAX):

    avg_dist = 0  # used for plot

    for a in AGENTS:
        a.do_actions()

    for a in AGENTS:
        a.update()

    showPlot(TIME >= TIME_MAX)
