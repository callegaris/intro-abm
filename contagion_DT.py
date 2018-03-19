
# Agent-based S-I-R contagion model in discrete time

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from random import random as rand
import numpy as np
import scipy.integrate
from math import fabs

fig, (view, demog) = plt.subplots(1,2)
fig.canvas.manager.window.attributes('-topmost', 1)
label_added = False

def diff_eqs(IN,t):
    Y = np.zeros(3)
    Y[0] = - BETA * IN[0] * IN[1] / NAGENTS
    Y[1] = BETA * IN[0] * IN[1] / NAGENTS - GAMMA * IN[1]
    Y[2] = GAMMA * IN[1]
    return Y


def showPlot(end):

    view.clear()
    view.scatter([a.x for a in AGENTS], [a.y for a in AGENTS],
                 s=40, cmap='brg', c=[a.status for a in AGENTS],
                 vmin=0, vmax=2)
    view.set_aspect(1)
    view.axis([0, SIZE, 0, SIZE])

    S = len([a for a in AGENTS if a.status == 0])
    I = len([a for a in AGENTS if a.status == 1])
    R = len([a for a in AGENTS if a.status == 2])

    global label_added
    if label_added:
        demog.plot(TIME, S, 'b.')
        demog.plot(TIME, I, 'r.')
        demog.plot(TIME, R, 'g.')
    else:
        demog.plot(TIME, S, 'b.', label="S")
        demog.plot(TIME, I, 'r.', label="I")
        demog.plot(TIME, R, 'g.', label="R")
        label_added = True
    demog.axis([0, MAX_TIME, 0, NAGENTS])
    demog.set_aspect(1.0*MAX_TIME/NAGENTS)

    if end:
        trange = np.arange(0, MAX_TIME, 0.01)
        ode_result = scipy.integrate.odeint(diff_eqs, IN, trange)
        demog.plot(trange, ode_result[:, 0], 'b-')
        demog.plot(trange, ode_result[:, 1], 'r-')
        demog.plot(trange, NAGENTS - (ode_result[:, 0] + ode_result[:, 1]), 'g-')

    plt.draw()
    if end:
        plt.pause(0)
    else:
        plt.pause(0.01)

class Patient:
    def __init__(self, x, y, input_status):
        self.status = input_status  # 0 = S, 1 = I, 2 = R
        self.x = x
        self.y = y
        self.next_status = input_status
        self.next_x = x
        self.next_y = y

    def do_actions(self):
        self.move()
        if self.status == 1:
            self.infect()
            r = rand()
            if r < GAMMA:
                self.recover()

    def recover(self):
        self.next_status = 2

    def infect(self):
        for target in AGENTS:
            if target.status == 0 and \
                            fabs(target.x - self.x) <= I_RADIUS and \
                            fabs(target.y - self.y) <= I_RADIUS:
                r = rand()
                if r < BETA:
                    target.next_status = 1  # 1 = I

    def move(self):
        r = rand()
        if r < MOVE:
            r = rand()
            if r < 0.25:
                self.next_x = (self.x - 1) % SIZE
            elif r < 0.5:
                self.next_x = (self.x + 1) % SIZE
            elif r < 0.75:
                self.next_y = (self.y - 1) % SIZE
            else:
                self.next_y = (self.y + 1) % SIZE

    def update(self):
        self.x = self.next_x
        self.y = self.next_y
        self.status = self.next_status


BETA = 0.20
GAMMA = 0.01
MOVE = 0.75
SIZE = 80
I0 = 0.1
I_RADIUS = 2
NAGENTS = 200
AGENTS = [Patient(int(rand()*SIZE), int(rand()*SIZE), int(rand()<I0)) for _ in range(NAGENTS)]

N_S = len([a for a in AGENTS if a.status == 0])
N_I = len([a for a in AGENTS if a.status == 1])
IN = [N_S, N_I]

MAX_TIME = 200
for TIME in range(MAX_TIME):

    showPlot(TIME >= MAX_TIME-1)

    for a in AGENTS:
        a.do_actions()

    for a in AGENTS:
        a.update()









