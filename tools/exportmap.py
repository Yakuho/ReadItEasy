# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/27
from utils import font
NEWLINE = 6


def export(uni, maps, path='export_labels.txt'):
    """
    build mapping between unicode from font file and true char
    :param uni: all unicode type: list
    :param maps: all true char about unicode
    :param path: save path
    :return:
    """
    print('ReadItEasy 🚀 map export start...')
    idx = 1
    text = '{\n'
    for key, value in zip(uni, maps):
        text += '"%s": "%s", ' % (key, value)
        if (idx % NEWLINE) == 0:
            text += '\n'
        idx += 1
    text += '\n}'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('succeed to export %s' % path)


if __name__ == '__main__':
    # --------------------二选一查看字体文件的unicode码--------------------
    # unicode = font.get_labels_by_GlyphNames('../datasets/fonts/MYnum00.woff')
    unicode = font.get_labels_by_glyphID('../datasets/fonts/MYnum00.woff', 12)
    # print(unicode)
    # ------------------------对应unicode码添加标签-------------------------
    m = ' .8023741695'
    export(unicode, m, path='../datasets/maps/MYnum00.txt')
