# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/28
import os
import time
import numpy

from applications import glyph
from data import loader
from utils import font
font_type = ['xml']
label_type = ['txt']


def export(map_path, xml_path, save_path='', class_list_name='classes'):
    print('ReadItEasy 🚀 Label convert start...')
    xml_files = os.listdir(xml_path)
    map_files = os.listdir(map_path)
    found, missing = 0, 0
    candidates = list()
    for file in xml_files:
        filename, _ = file.split('.')
        if _ in font_type:
            if filename + '.txt' in map_files:
                if filename not in candidates:
                    found += 1
                    candidates.append(filename)
            else:
                print('[xml file]: %s miss labels file like %s.txt' % (file, filename))
    for file in map_files:
        filename, _ = file.split('.')
        if _ in label_type:
            if filename + '.xml' in xml_files:
                if filename not in candidates:
                    found += 1
                    candidates.append(filename)
            else:
                print('[map file]: %s miss labels file like %s.xml' % (file, filename))

    if found > 0:
        if not save_path:
            save_path = os.path.join(xml_path, 'labels')
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        classes = list()
        t0 = time.time()
        for file in candidates:
            data = font.xml2info(os.path.join(xml_path, '%s.xml' % file), glyph.FontGlyph)
            maps = loader.maps(os.path.join(map_path, '%s.txt' % file))
            classes.extend(list(maps.values()))
            numpy.savez(os.path.join(save_path, file), **{maps[key]: data[key] for key in data})
        with open(os.path.join(save_path, '%s.txt' % class_list_name), 'w', encoding='utf-8') as f:
            f.write(str(list(set(classes))))
        t1 = time.time()
        try:
            cost = found / (t1 - t0)
        except ZeroDivisionError:
            cost = found
        print('xml file %d converted, %d missing\t[%.2fit/s]' % (found, missing, cost))
        print('items: %d completed in %.3f s.' % (found, t1 - t0))
        print('succeed to export %s' % save_path)
    else:
        print('xml file %d found, %d missing' % (found, missing))


if __name__ == '__main__':
    export(map_path='../datasets/maps', xml_path='../datasets/XML', save_path='')
