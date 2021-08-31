# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/28
import os


def init_dir(mode, name):
    root1 = './runs'
    root2 = mode
    root3 = 'logs'
    if not os.path.exists(root1):
        os.mkdir(root1)
    if not os.path.exists(os.path.join(root1, root2)):
        os.mkdir(os.path.join(root1, root2))
    files = os.listdir(os.path.join(root1, root2))
    idx = 0
    while True:
        if name + str(idx) in files:
            idx += 1
        else:
            os.mkdir(os.path.join(root1, root2, name + str(idx)))
            os.mkdir(os.path.join(root1, root2, name + str(idx), root3))
            return os.path.join(root1, root2, name + str(idx))
