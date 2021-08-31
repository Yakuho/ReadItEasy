# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/27
from fontTools.ttLib import TTFont
from xml.dom.minidom import parse


def get_labels_by_GlyphNames(file):
    """
    get unicode from font file by glyph names
    :param file: path of woff/ttf file
    :return:
    """
    font = TTFont(file)
    return font.getGlyphNames()


def get_labels_by_glyphID(file, total_glyphID):
    """
    get unicode from font file by glyph ID
    :param file: path of woff/ttf file
    :param total_glyphID: the summation of all char
    :return:
    """
    font = TTFont(file)
    return [font.getGlyphName(glyphID=glyphID) for glyphID in range(total_glyphID)]


def font2xml(src, des):
    """
    export font information to xml
    :param src: src file path
    :param des: des file path
    :return:
    """
    font = TTFont(src)
    font.saveXML(des)


def xml2info(path, glyph):
    """
    read xml file to information like {'...': {...}}
    :param path: xml path
    :param glyph: class font glyph to normalize offset
    :return:
    """
    collection = parse(path).documentElement
    items = collection.getElementsByTagName("TTGlyph")
    # get all contour
    data = dict()
    for item in items:
        clusters = item.getElementsByTagName("contour")
        unicode = item.getAttribute("name")
        if len(clusters) == 0:
            # except empty
            continue
        # all xy each char
        font_glyph = glyph()
        for cluster in clusters:
            points = cluster.getElementsByTagName("pt")
            for point in points:
                on = int(point.getAttribute("on"))
                x = int(point.getAttribute("x"))
                y = int(point.getAttribute("y"))
                font_glyph.add(x, y, on)
        else:
            data[unicode] = font_glyph.update()
    return data
