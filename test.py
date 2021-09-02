# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/28
import os
import numpy
import time

from applications import Crossentropy2Accuracy
from applications import glyph
from data import loader
from utils import font
from nets import ReadItEasy


class Terminal:
    def __init__(self, weights, class_list):
        """

        :param weights: model weights file path
        :param class_list: class list file path
        """
        train_steps, valid_steps, classes_num, classes_list = loader.class_list(class_list)
        self.class_list = class_list
        self.model = ReadItEasy.ReadItEasy(classes_num)
        self.model(numpy.zeros((1, 3, 3)))
        self.model.load_weights(weights)
        self.model.summary()

    def predict(self, font_file):
        """

        :param font_file: the font path file like woff/ttf
        """
        path, file = os.path.split(font_file)[: -1], os.path.split(font_file)[-1]
        filename, _ = file.split('.')
        font.font2xml(os.path.join(*path, file), os.path.join(*path, '%s.xml' % filename))
        data = font.xml2info(os.path.join(*path, '%s.xml' % filename), glyph.FontGlyph)
        os.remove(os.path.join(*path, '%s.xml' % filename))
        t0 = time.time()
        for unicode in data.keys():
            y = self.model(data[unicode])
            # predict_confidences = Crossentropy2Accuracy.predict2accuracy(y)
            item = {'unicode': unicode, 'char': self.class_list[numpy.argmax(y)],
                    'confidences': y[0, numpy.argmax(y)].numpy()}
            print(item)
        t1 = time.time()
        print('Inference finished cost %.3fms' % ((t1 - t0) * 1e3))


if __name__ == '__main__':
    m = Terminal(classes_num=12, weights='./weights/MaoYan.h5', class_list='./datasets/labels/classes.txt')
    m.predict(font_file='./evaluate/test.woff')
