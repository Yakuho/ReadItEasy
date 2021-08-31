# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/27
import os
import time

from utils import font
font_type = ['woff', 'ttf']


def export(src, des=''):
    print('ReadItEasy 🚀 XML convert start...')
    files = os.listdir(src)
    found, missing = 0, 0
    for file in files:
        filename, _ = file.split('.')
        if _ in font_type:
            found += 1
        else:
            missing += 1
    if found > 0:
        if not des:
            des = os.path.join(src, 'XML')
        if not os.path.exists(des):
            os.mkdir(des)
        t0 = time.time()
        for file in files:
            filename, _ = file.split('.')
            if _ in font_type:
                font.font2xml(os.path.join(src, file), os.path.join(des, '%s.xml' % filename))
        t1 = time.time()
        try:
            cost = found / (t1 - t0)
        except ZeroDivisionError:
            cost = found
        print('Font file %d converted, %d missing\t[%.2fit/s]' % (found, missing, cost))
        print('items: %d completed in %.3f s.' % (found, t1 - t0))
        print('succeed to export %s' % des)
    else:
        print('Font file %d found, %d missing' % (found, missing))


if __name__ == '__main__':
    export(src='../datasets/fonts', des='')
