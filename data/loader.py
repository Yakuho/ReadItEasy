# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/27
import os
import json
import numpy
import random


def config(path):
    """
    load config file from json
    :param path: json path
    """
    with open(path, 'r') as f:
        context = json.loads(f.read().strip())
    return context


def maps(path):
    """
        load maps file from txt
        :param path: txt path
        """
    with open(path, 'r', encoding='utf-8') as f:
        context = eval(f.read().strip())
    return context


def class_list(path):
    """
    load classes list from txt when train model will get it
    :param path: txt path
    """
    with open(path, 'r', encoding='utf-8') as f:
        classes = eval(f.read().strip())
    return classes


def generator(path, classes):
    """
    load xy from npz file to tensor
    generate X Y for each char, due to each char size is different
    example : "1" -> (63, 3), "8" -> (102, 3)
    :param path: json path
    :param classes: class list about model output set
    """
    while True:
        # dir about data
        files = os.listdir(path)
        random.shuffle(files)
        while files:
            filename = files.pop()
            # get {'1': tensor([..., 3])} from npz file
            data = numpy.load(os.path.join(path, filename))
            chars = list(data)
            random.shuffle(chars)
            while chars:
                char = chars.pop()
                char_one_hot = numpy.zeros((1, len(classes)))
                char_one_hot[..., classes.index(char)] = 1
                yield data[char], char_one_hot
