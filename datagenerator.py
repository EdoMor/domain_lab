from PIL import Image, ImageEnhance
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator


# gets an img name and returns only the volt
def get_volt_from_img_name(name:str)->float:
    return float(name.split('_')[-1].replace('.png',''))


def data_generator(inputDataPath, outputDataPath, batchSize, resized_width=None, resized_height=None):
    '''
    :return: a generator of a bach of data(input,output) from the dataPath dir,
             in the size of batchSize.
             the data will all resize to dim : (resized_width, resized_height),
             then flattend.
             the input is a flattend img + input and output volteges + their subtraction
             the output is is a flattend img
    '''
    a = os.scandir(inputDataPath)
    b = os.scandir(outputDataPath)
    while True:
        input = []
        output = []
        while len(input) < batchSize:
            input_file_name = next(a).name
            output_file_name = next(b).name
            input_img = cv2.imread(os.path.join(inputDataPath,input_file_name), cv2.IMREAD_GRAYSCALE)
            output_img = cv2.imread(os.path.join(outputDataPath,output_file_name), cv2.IMREAD_GRAYSCALE)
            # ensures all images be the same size:
            if resized_height is not None:
                input_img = cv2.resize(input_img, (resized_width, resized_height))
                output_img = cv2.resize(output_img, (resized_width, resized_height))
            input_volt = get_volt_from_img_name(input_file_name)
            output_volt = get_volt_from_img_name(output_file_name)
            # flatten images to vectors, and adds vols to input:
            input.append(np.append(input_img.flatten(),
                            [input_volt, output_volt, output_volt-input_volt]))
            output.append(output_img.flatten())
        yield input, output




if __name__ == '__main__':
    gen = data_generator('./data/train/input', './data/train/output', 2)
    print(next(gen))
    print(next(gen))