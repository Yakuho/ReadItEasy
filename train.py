# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2021/8/28
import os
import numpy

from data import loader
from utils import makedir
from nets.ReadItEasy import ReadItEasy

from solvers.optimizers import optimizers
from solvers.losses import losses
from solvers.metrics import metrics
from solvers.callbacks import callbacks

from tensorflow.python.training.checkpoint_management import latest_checkpoint

config = loader.config('config.json')
solver = loader.config('solvers/config.json')
class_list = loader.class_list(config['datasets']['class_list'])
train_data = loader.generator(config['datasets']['train']['path'], class_list)
valid_data = loader.generator(config['datasets']['valid']['path'], class_list)

save_path = makedir.init_dir('train', config['save']['root_path'])

model = ReadItEasy(config['datasets']['class_num'])
if config['model']['restore']:
    checkpoint = latest_checkpoint(config['model']['checkpoint'])
    model.load_weights(checkpoint)
if config['model']['pre-training']:
    model.load_weights(config['model']['weights'])
model.compile(
    optimizer=eval(solver['compile']['optimizer'])(**solver['hyper-parameter']['optimizer']),
    loss=eval(solver['compile']['loss'])(**solver['hyper-parameter']['loss']),
    metrics=[eval(metric)(**solver['compile']['metric'][metric]) for metric in solver['compile']['metric']]
)
model.fit(
    train_data, steps_per_epoch=config['datasets']['train']['steps'],
    validation_data=valid_data, validation_steps=config['datasets']['valid']['steps'],
    validation_freq=config['datasets']['valid']['freq'],
    epochs=config['datasets']['epochs'], verbose=1, workers=1, initial_epoch=0,
    callbacks=[
        callbacks.ModelCheckpoint(filepath=os.path.join(save_path, 'checkpoint'),
                                  save_weights_only=True,
                                  save_best_only=True,
                                  period=config['save']['ckpt_freq']),
        callbacks.TensorBoard(log_dir=os.path.join(save_path, 'logs'), write_graph=True, write_images=False,
                              update_freq='epoch', histogram_freq=1)
    ].extend([eval(callback)(**config['callbacks'][callback]) for callback in config['callbacks']])
)
model.save_weights(os.path.join(save_path, config['save']['model_name']))
