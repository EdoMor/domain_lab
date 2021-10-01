from PIL import Image
import numpy as np
import datetime
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import tensorflow as tf
from tensorflow import keras
from datagenerator import *


# constants:
SIZE = 160
RESIZED_WIDTH = SIZE  # temp
RESIZED_HEIGHT = SIZE  # temp
RESIZED_NUM_PIXELS = RESIZED_WIDTH * RESIZED_HEIGHT
SHAPE = RESIZED_NUM_PIXELS + 3
TRAIN_PATH = r'R:\domain_lab\runs_processed\train'  # temp
VALID_PATH = r'R:\domain_lab\runs_processed\validation'  # temp
TEST_PATH = r'R:\domain_lab\runs_processed\test'  # temp
BACH_SIZE = 13 # temp
TRAIN_DATASET_SIZE = dataset_size(TRAIN_PATH)
VALID_DATASET_SIZE = dataset_size(VALID_PATH)
TEST_DATA_SIZE = dataset_size(TEST_PATH)
STEPS_PER_EPOCH = TRAIN_DATASET_SIZE // BACH_SIZE
EPOCHS = 10  # temp
VALIDATION_STEPS = VALID_DATASET_SIZE // BACH_SIZE
TEST_STEPS = TEST_DATA_SIZE // BACH_SIZE


model = tf.keras.Model


def my_fit(train_inputs, train_output, valid_inputs, valid_output, batch_size=32, epochs: int = 1):
    """
    inputs: generator of a list of np.array inputs
    output: generator of a np.array output

    """
    for _ in range(epochs):
        flag = True
        while flag:
            try:
                next_bach_of_training_inputs = next(train_inputs)
                next_bach_of_training_output = next(train_output)
                validation_data = (next(valid_inputs), next(valid_output))
                model.fit(x = next_bach_of_training_inputs,
                          y = next_bach_of_training_output,
                          batch_size = batch_size,
                          use_multiprocessing = True)
            except StopIteration:
                while flag:
                    try:
                        next_bach_of_valid_inputs = next(valid_inputs)
                        next_bach_of_valid_output = next(valid_output)
                        model.evaluate(x = next_bach_of_valid_inputs,
                                       y = next_bach_of_valid_output,
                                       batch_size=batch_size,
                                       use_multiprocessing=True)
                    except StopIteration:
                       flag = False

# #test:
#
# train_input_data = random.sample(range(-100, 100), 1000)
# train_output_data = map(lambda x: x**2, input_data)
#
# valid_input_data = random.sample(range(-100, 100), 1000)
# # valid_output_data = map(lambda x: x**2, input_data)
#
#
# def test_gen_input(input:bool, batch_size):
#     count = 0
#     while True:
#         yield np.array(train_input_data[count:count+batch_size])
#         count += batch_size
#
# def test_gen_output(input:bool, batch_size):
#     count = 0
#     while True:
#         yield np.array(train_output_data[count:count+batch_size])
#         count += batch_size
#
# # model:
# model = tf.keras.Sequential()
# model.add(tf.keras.Input(shape=1,))
# model.add(tf.keras.layers.Dense(5))
# model.add(tf.keras.layers.Dense(1))
#
# # Compile the Model:
# model.compile(optimizer=keras.optimizers.Adam())
#
#
# x_generator = test_gen_input()
# y_generator
#
#
# # Training the Model:
# model.fit(x=train_generator,
#           steps_per_epoch=STEPS_PER_EPOCH,
#           epochs=EPOCHS,
#           validation_data=validation_generator,
#           validation_steps=VALIDATION_STEPS)
#

def my_loss(y_true,y_pred):
    crossentropy_loss = tf.keras.metrics.binary_crossentropy(y_true, y_pred)
    sum_loss = np.abs(np.sum(y_true, 1) - np.sum(y_pred, 1))
    return crossentropy_loss + sum_loss

if __name__ == '__main__':