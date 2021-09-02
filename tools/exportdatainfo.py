# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/9/2
import os
import numpy


def export(path, save_path=''):
    train_files = os.listdir(os.path.join(path, 'train'))
    valid_files = os.listdir(os.path.join(path, 'valid'))
    if len(train_files) and len(valid_files):
        classes = list()
        train_steps = 0
        valid_steps = 0
        while train_files:
            file = train_files.pop()
            data = numpy.load(os.path.join(path, 'train', file))
            chars = list(data)
            classes.extend(chars)
            train_steps += len(chars)
        while valid_files:
            file = valid_files.pop()
            data = numpy.load(os.path.join(path, 'valid', file))
            chars = list(data)
            classes.extend(chars)
            valid_steps += len(chars)
        classes = list(set(classes))
        if not save_path:
            save_path = path
        with open(os.path.join(save_path, 'classes.txt'), 'w', encoding='utf-8') as f:
            f.write('%d %d %d\n' % (train_steps, valid_steps, len(classes)))
            f.write(str(classes))
    else:
        print('empty dir by path: %s' % path)


if __name__ == '__main__':
    export('../datasets/MaoYan/labels')
