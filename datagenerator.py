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


def reshape_for_net(img, resized_width:int=None, resized_height:int=None):
    # ensures all images be the same size:
    if resized_height is not None:
        img = cv2.resize(img, (resized_width, resized_height))
    # tern img to zeros and ones:
    img = img / 255
    # flatten img to a vector
    return img.flatten()


def add_volts(reshaped_img, input_volt:float, output_volt:float):
    return np.append(reshaped_img, [input_volt, output_volt, output_volt - input_volt])


def img_to_input(img, input_volt:float, output_volt:float, resized_width:int=None, resized_height:int=None):
    reshaped_img = reshape_for_net(img, resized_width, resized_height)
    return add_volts(reshaped_img, input_volt, output_volt)


def img_from_input(input:np.array, resized_width:int, resized_height:int) -> np.array:
    flattened_img = np.delete(input, [-1, -2, -3])
    return flattened_img.reshape([resized_width, resized_height])*255


def img_from_output(output:np.array, resized_width:int, resized_height:int) -> np.array:
    return output.reshape([resized_width, resized_height])*255


def next_data(all_runs_path:str, resized_width:int=None, resized_height:int=None):
    """
    :return: the next data pair: (input, output)
             the data will all resize to dim : (resized_width, resized_height),
             then flatten.
             the input is a flattend img + input and output volteges + their subtraction
             the output is is a flattend img
    """
    for run in os.listdir(all_runs_path):
        run_path = os.path.join(all_runs_path, run)
        run_iter = os.scandir(run_path)
        try:
            input_img_name = next(run_iter).name
            input_volt = get_volt_from_img_name(input_img_name)
            input_img_path = os.path.join(run_path, input_img_name)
            reshaped_input = reshape_for_net(cv2.imread(input_img_path, cv2.IMREAD_GRAYSCALE), resized_width, resized_height)
        except StopIteration:
            break
        while True:
            try:
                output_img_name = next(run_iter).name
                output_volt = get_volt_from_img_name(output_img_name)
                output_img_path = os.path.join(run_path, output_img_name)
                output = reshape_for_net(cv2.imread(output_img_path, cv2.IMREAD_GRAYSCALE), resized_width,
                                                    resized_height)
                input = add_volts(reshaped_input, input_volt, output_volt)
                yield input, output
                input_volt = output_volt
                reshaped_input = output
            except StopIteration:
                break


def data_generator(all_runs_path: str, batchSize: int, train_mode: bool = True,
                   resized_width: int = None, resized_height: int = None):
    '''
    :return: a bach of data(input,output) from the all_runs_path dir,
             in the size of batchSize.
    '''
    data_iter = next_data(all_runs_path, resized_width, resized_height)
    while True:
        inputs = [0]*batchSize
        outputs = [0]*batchSize
        for i in range(batchSize):
            try:
                inputs[i], outputs[i] = next(data_iter)
            except StopIteration:
                if train_mode:  #todo: find out if we need to raise Error or yield an empty list
                    data_iter = next_data(all_runs_path, resized_width, resized_height)
                    inputs[i], outputs[i] = next(data_iter)
                else:
                    raise StopIteration
        yield inputs, outputs


if __name__ == '__main__':
    all_runs_path = r'C:\Users\hadar\Desktop\Advanced_Lab\run_1_data\test_generater'
    resized_width = 10**3
    resized_height = 10**3
    iter = data_generator(all_runs_path, 3, True, resized_width, resized_height)
    while True:
        input("Press Enter to continue...")
        my_inputs, outputs = next(iter)
        print(f'{len(my_inputs)=}\n{len(outputs)=}')
        for i in range(len(outputs)):
            input_img = img_from_input(my_inputs[i], resized_width, resized_height)
            output_img = img_from_output(outputs[i], resized_width, resized_height)
            plt.clf()
            plt.imshow(input_img)
            plt.show()
            plt.imshow(output_img)
            plt.show()







