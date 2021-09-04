# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/28
import numpy
import random


class FontGlyph:
    """
    clean and normalize data from all font file xy on.
    """
    __xs = numpy.array([])
    __ys = numpy.array([])
    __on = numpy.array([])
    beta = 8
    gama = 1

    def __init__(self):
        self.x_min = numpy.inf
        self.y_min = numpy.inf
        self.x_max = 0
        self.y_max = 0

    def add(self, x, y, on, sort_key='x'):
        if x < self.x_min:
            self.x_min = x
        if y < self.y_min:
            self.y_min = y
        if x > self.x_max:
            self.x_max = x
        if y > self.y_max:
            self.y_max = y
        self.__xs = numpy.append(self.__xs, x)
        self.__ys = numpy.append(self.__ys, y)
        self.__on = numpy.append(self.__on, on - 0.5)
        if sort_key == 'x':
            sort_idx = numpy.argsort(self.__xs)
        elif sort_key == 'y':
            sort_idx = numpy.argsort(self.__ys)
        else:
            raise TypeError('not support sort key %s' % sort_key)
        self.__xs = self.__xs[sort_idx]
        self.__ys = self.__ys[sort_idx]
        self.__on = self.__on[sort_idx]

    def update(self):
        # found xy middle point
        x_mid = round((self.x_min + self.x_max) / 2)
        y_mid = round((self.y_min + self.y_max) / 2)
        # normalize xy
        self.__xs = self.__xs - x_mid
        self.__ys = self.__ys - y_mid
        # turn 0 to gama value to void gradient disappear
        self.__xs[self.__xs > 0] = self.__xs[self.__xs > 0] + self.gama
        self.__xs[self.__xs < 0] = self.__xs[self.__xs < 0] - self.gama
        self.__ys[self.__ys > 0] = self.__ys[self.__ys > 0] + self.gama
        self.__ys[self.__ys < 0] = self.__ys[self.__ys < 0] - self.gama
        self.__xs[self.__xs == 0] = random.choice([-self.gama, self.gama])
        self.__ys[self.__ys == 0] = random.choice([-self.gama, self.gama])
        w = self.x_max - self.x_min
        h = self.y_max - self.y_min
        # add beta to scale void gradient disappear
        scale = max(w, h) / 2 + self.beta
        # normalize xy to (0, 1)
        self.__xs = self.__xs / scale
        self.__ys = self.__ys / scale
        data = numpy.stack((self.__xs, self.__ys, self.__on), axis=1)
        return numpy.expand_dims(data, axis=0)
