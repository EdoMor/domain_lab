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


def data_generator(inputDataPath:str, outputDataPath:str, batchSize:int, train_mode:bool=True,  resized_width:int=None, resized_height:int=None):
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
        input = [0]*batchSize
        output = [0]*batchSize
        for i in range(batchSize):
            try:
                input_file_name = next(a).name
                output_file_name = next(b).name
            except StopIteration:
                if train_mode:
                    a = os.scandir(inputDataPath)
                    b = os.scandir(outputDataPath)
                    input_file_name = next(a).name
                    output_file_name = next(b).name
                else:
                    raise StopIteration

            input_img = cv2.imread(os.path.join(inputDataPath,input_file_name), cv2.IMREAD_GRAYSCALE)
            output_img = cv2.imread(os.path.join(outputDataPath,output_file_name), cv2.IMREAD_GRAYSCALE)
            # ensures all images be the same size:
            if resized_height is not None:
                input_img = cv2.resize(input_img, (resized_width, resized_height))
                output_img = cv2.resize(output_img, (resized_width, resized_height))
            input_volt = get_volt_from_img_name(input_file_name)
            output_volt = get_volt_from_img_name(output_file_name)
            # flatten images to vectors, and adds vols to input:
            input[i] = np.append(input_img.flatten(),
                            [input_volt, output_volt, output_volt-input_volt])
            output[i] = output_img.flatten()
        yield input, output


if __name__ == '__main__':
    for i,j in enumerate(data_generator('./data/train/input', './data/train/output', 2)):
        print(j)
        break
    # print(next(gen))
    # print(next(gen))