# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/30
import tensorflow as tf


def predict2accuracy(y):
    denominator = tf.reduce_sum(tf.exp(y))
    numerator = tf.exp(y)
    confidences = numerator / denominator
    return confidences

