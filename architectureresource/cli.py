# -*- coding: utf-8 -*-

import click
import logging
import sys
import logging
import tensorflow as tf
from proton_decay_study.models.vgg16 import VGG16
from proton_decay_study.generators.multi_file import MultiFileDataGenerator
from proton_decay_study.generators.threaded_multi_file import ThreadedMultiFileDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
import signal
import sys


@click.command()
@click.argument('file_list', nargs=-1)
def print_images(file_list):
  logging.basicConfig(level=logging.DEBUG)
  from architectureresource.image_writer import ImageWriter
  for _file in file_list:
    writer = ImageWriter(_file)
    writer.get_all_particle_images()


@click.command()
def get_resource_for_network():
  logging.basicConfig(level=logging.DEBUG)
  from architectureresource.resource import NetworkAnalyzer
  





@click.command()
@click.argument('file_list', nargs=-1)
def standard_vgg_training(file_list):
  """
    Standard VGG Training is aimed at 
  """
  logging.basicConfig(level=logging.DEBUG)
  logger = logging.getLogger()
  sess = tf.Session()


  generator = MultiFileDataGenerator(file_list, 'image/wires','label/type', batch_size=1)
  model = VGG16(generator)
  training_output = model.fit_generator(generator, steps_per_epoch = 1000, 
                                      epochs=1000)
  model.save("trained_weights.h5")
  open('history.json','w').write({'loss':training_output.history['loss'], 
                                  'accuracy':training_output['accuracy']})
  logger.info("Done.")

_model = None
def signal_handler(signal, frame):
  global _model
  logging.info("SigINT was called. Saving Model")
  if _model is not None:
    _model.save('interrupted_output.h5')
    logging.info('Model Weights saved to interrupted_output.h5')
  sys.exit(0)


if __name__ == "__main__":
    main()