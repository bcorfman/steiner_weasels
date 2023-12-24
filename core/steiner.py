""" Steiner.py: main module for Steiner Weasels """

import math
import random


class Steiner:
    """ Main class for creating the app."""

    def __init__(self):
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.dxmin = 0
        self.dxmax = 0
        self.dymin = 0
        self.dymax = 0
        self.maxgens = 5000
        self.killgens = 1000
        self.maxpop = 1000
        self.death = 100000
        self.mutespergen = 50
        self.mutesperorg = 3
        self.bfactor = 1.5
        self.delay = 1  # ms
        self.rows = 1  # rows of displayed organisms
        self.cols = 1  # cols of displayed organisms
        self.elite = 10  # num kept as-is after Fitness
        self.fixednodes = 5
        self.varbnodes = 4
        self.allocate()
        self.xfixed[0] = 350.0
        self.yfixed[0] = 300.0
        self.xfixed[1] = 650.0
        self.yfixed[1] = 300.0
        self.xfixed[2] = 200.0
        self.yfixed[2] = 560.0
        self.xfixed[3] = 800.0
        self.yfixed[3] = 560.0
        self.xfixed[4] = 500.0
        self.yfixed[4] = 733.3
        self.dxmin = 0.0
        self.dxmax = 1500.0
        self.dymin = 0.0
        self.dymax = 1500.0
        self.running = False
        self.drawon = True
        self.target = False
        self.digitizing = False
        self.pixel_fmt = None
        self.box = None
        self.pop = None
        self.status_report = ""

    def data2pixel(self, xval, yval):
        """ scale plot point to dxmin, dxmax, dymin, dymax """
        x = self.xmin + (self.xmax - self.xmin) * (xval - self.dxmin) / (
            self.dxmax - self.dxmin)
        y = self.ymax + (self.ymin - self.ymax) * (yval - self.dymin) / (
            self.dymax - self.dymin)
        return x, y

    def pixel2data(self, x, y):
        """ scales location to boundaries """
        xval = self.dxmin + (x - self.xmin) * (self.dxmax - self.dxmin) / (
            self.xmax - self.xmin)
        yval = self.dymin + (y - self.ymax) * (self.dymax - self.dymin) / (
            self.ymin - self.ymax)
        return xval, yval

    def report(self, pt):
        """ Reports point location """
        if self.box.pt_in_rect(pt):
            xt, yt = self.pixel2data(pt.x, pt.y)
            xt, yt = math.floor(xt), math.floor(yt)
            self.pixel_fmt = f'{pt.x},{pt.y} (pix)\n{xt}{yt} (pos)'
        else:
            self.pixel_fmt = 'Ready'

    def allocate(self):
        """ Reserving memory when setting up a new session. """
        self.npts = self.fixednodes + self.varbnodes
        # nC2, n things 2 at a time
        self.combs = self.npts * (self.npts - 1) / 2
        self.ndigs = self.varbnodes * 3 * 2  # digits in coord map
        self.ntot = 2 + self.ndigs + self.combs

        self.xfixed = [0.0 for _ in range(self.fixednodes)]
        self.yfixed = [0.0 for _ in range(self.fixednodes)]
        self.xvarb = [0.0 for _ in range(self.varbnodes)]
        self.yvarb = [0.0 for _ in range(self.varbnodes)]

        self.conmap = [False for _ in range(self.combs)]
        self.got = [False for _ in range(self.npts)]
        self.fitness = [self.death for _ in range(self.maxpop)]
        self.sortids = [-1 for _ in range(self.maxpop)]

    def create(self):
        """ Creating a population of weasels. """
        self.pop = [self.create_one() for _ in range(self.maxpop)]
        self.status_report = "Pop created"

    def create_one(self):
        """ Make one weasel only. """
        critter = ''
        x = random.random()
        num = math.floor(self.varbnodes * x)
        num = self.varbnodes
        if num < 10:
            temp = f'{num:01d}'
        else:
            temp = f'{num:2d}'
        critter += temp

        # second, the variable node coords
        for _ in range(self.varbnodes * 3 * 2):
            x = random.random()
