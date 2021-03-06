# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/28
import tensorflow as tf


class ReadItEasy(tf.keras.models.Model):
    def __init__(self, class_num, *args, **kwargs):
        super(ReadItEasy, self).__init__(*args, **kwargs)
        self.lstm1 = tf.keras.layers.LSTM(16)

        self.dense1 = tf.keras.layers.Dense(32, activation='relu')

        self.dense2 = tf.keras.layers.Dense(class_num, activation='softmax')

    def call(self, x, training=None, mask=None):
        h = self.lstm1(x)

        h = self.dense1(h)

        h = self.dense2(h)

        return h


class ReadItEasyS(tf.keras.models.Model):
    def __init__(self, class_num, *args, **kwargs):
        super(ReadItEasyS, self).__init__(*args, **kwargs)
        self.conv = tf.keras.layers.Conv1D(32, 3, 2, activation='relu', padding='valid')

        self.lstm = tf.keras.layers.LSTM(8)

        self.dense1 = tf.keras.layers.Dense(32, activation='relu')

        self.dense2 = tf.keras.layers.Dense(class_num, activation='softmax')

    def call(self, x, training=None, mask=None):
        h = self.conv(x)

        h = self.lstm(h)

        h = self.dense1(h)

        h = self.dense2(h)

        return h
