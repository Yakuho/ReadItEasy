# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/29
import os
import shutil
import random


def split_data(path, proportion=0.7):
    print('ReadItEasy 🚀 datasets split start...')
    files = os.listdir(path)
    num = len(files)
    if num > 0:
        mid = round(num * proportion)
        random.shuffle(files)
        if not os.path.exists(os.path.join(path, 'train')):
            os.mkdir(os.path.join(path, 'train'))
        if not os.path.exists(os.path.join(path, 'valid')):
            os.mkdir(os.path.join(path, 'valid'))
        for file in files[: mid]:
            shutil.move(os.path.join(path, file), os.path.join(path, 'train', file))
        for file in files[mid:]:
            shutil.move(os.path.join(path, file), os.path.join(path, 'valid', file))
    else:
        print('path %s is empty dir' % path)


if __name__ == '__main__':
    split_data('../datasets/labels', 0.8)
