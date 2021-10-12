import random
import numpy as np
import cv2
import os
from shutil import move


# gets an img name and returns only the volt
def get_volt_from_img_name(name: str) -> float:
    return float(name.split('_')[-1].replace('.png', ''))


# count number of inputs in the run directory
def dataset_size(runs_path: str) -> int:
    data_size = 0
    for run in os.listdir(runs_path):
        run_images = os.listdir(os.path.join(runs_path, run))
        data_size += len(run_images) - 1
    return data_size


def reshape_for_net(img, resized_width: int = None, resized_height: int = None, crop=None):
    # ensures all images be the same size:
    if resized_height is not None:
        img = img[crop[0][0]:crop[0][1], crop[1][0]:crop[1][1]]
        img = cv2.resize(img, (resized_width, resized_height))
    # tern img to zeros and ones:
    img = img / 255
    _, img = cv2.threshold(img, 0.5 , 1, cv2.THRESH_BINARY)
    # flatten img to a vector
    return img.flatten()

def reshape_for_net_no_flatening(img, resized_width: int = None, resized_height: int = None, crop=None):
    '''crop = [[x start, x end],[y start,y end]]'''
    # ensures all images be the same size:
    if resized_height is not None:
        if crop != None:
            img=img[crop[0][0]:crop[0][1],crop[1][0]:crop[1][1]]
        img = cv2.resize(img, (resized_width, resized_height))
        img = img / 255
        _, img = cv2.threshold(img, 0.5 , 1, cv2.THRESH_BINARY)
        img = np.reshape(img, (resized_width, resized_height, 1))
    return img


def add_volts(reshaped_img, input_volt: float, output_volt: float):
    return np.append(reshaped_img, [input_volt, output_volt, output_volt - input_volt])


def img_to_input(img, input_volt: float, output_volt: float, resized_width: int = None, resized_height: int = None):
    reshaped_img = reshape_for_net(img, resized_width, resized_height)
    return add_volts(reshaped_img, input_volt, output_volt)


def img_from_input(input: np.array, resized_width: int, resized_height: int) -> np.array:
    flattened_img = np.delete(input, [-1, -2, -3])
    return flattened_img.reshape([resized_width, resized_height]) * 255


def img_from_output(output: np.array, resized_width: int, resized_height: int) -> np.array:
    return output.reshape([resized_width, resized_height]) * 255


def next_data(all_runs_path: str, resized_width: int = None, resized_height: int = None, add_voltge:bool=True, just_voltage:bool=False):
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
            reshaped_input = reshape_for_net(cv2.imread(input_img_path, cv2.IMREAD_GRAYSCALE), resized_width,
                                             resized_height)

        except StopIteration:
            break
        while True:
            try:
                output_img_name = next(run_iter).name
                output_volt = get_volt_from_img_name(output_img_name)
                output_img_path = os.path.join(run_path, output_img_name)
                output = reshape_for_net(cv2.imread(output_img_path, cv2.IMREAD_GRAYSCALE), resized_width,
                                         resized_height)

                if add_voltge:
                    data_input = add_volts(reshaped_input, input_volt, output_volt)
                if just_voltage:
                    data_input = np.array([input_volt, output_volt, output_volt - input_volt])
                yield data_input, output
                input_volt = output_volt
                reshaped_input = output
            except StopIteration:
                break                

def data_generator(all_runs_path: str, batchSize: int, train_mode: bool = True,
                   resized_width: int = None, resized_height: int = None, add_voltge:bool=True, 
                   just_voltage:bool=False):
    '''
    :return: a bach of data(input,output) from the all_runs_path dir,
             in the size of batchSize.
    '''
    data_iter = next_data(all_runs_path, resized_width, resized_height, add_voltge, just_voltage)
    while True:
        inputs = [0] * batchSize
        outputs = [0] * batchSize
        for i in range(batchSize):
            try:
                inputs[i], outputs[i] = next(data_iter)
            except StopIteration:
                if train_mode:  # todo: find out if we need to raise Error or yield an empty list
                    data_iter = next_data(all_runs_path, resized_width, resized_height)
                    inputs[i], outputs[i] = next(data_iter)
                else:
                    raise StopIteration
        yield np.array(inputs, dtype='float32'), np.array(outputs, dtype='float32')

def creat_next_data_for_cnn(all_runs_path: str, resized_width: int = None, resized_height: int = None, crop=None):
    '''crop = [[x start, x end],[y start,y end]]'''
    def next_data_for_cnn():
        for run in os.listdir(all_runs_path):
            run_path = os.path.join(all_runs_path, run)
            run_iter = os.scandir(run_path)
            try:
                input_img_name = next(run_iter).name
                input_volt = get_volt_from_img_name(input_img_name)
                input_img_path = os.path.join(run_path, input_img_name)
                reshaped_input = reshape_for_net_no_flatening(cv2.imread(input_img_path, cv2.IMREAD_GRAYSCALE), resized_width,
                                                 resized_height, crop=crop)
            except StopIteration:
                break
            while True:
                try:
                    output_img_name = next(run_iter).name
                    output_volt = get_volt_from_img_name(output_img_name)
                    output_img_path = os.path.join(run_path, output_img_name)
                    output = np.array(reshape_for_net(cv2.imread(output_img_path, cv2.IMREAD_GRAYSCALE), resized_width,
                                             resized_height, crop=crop), dtype='float32')
                    data_input = (np.array(reshaped_input, dtype='float32') ,
                                  np.array([input_volt, output_volt, output_volt-input_volt], dtype='float32'))   
                    yield data_input, output
                    input_volt = output_volt
                    reshaped_input = np.reshape(output, (resized_width, resized_height, 1))
                except StopIteration:
                    break
    return next_data_for_cnn

import numpy as np
def data_generator_for_cnn(all_runs_path: str, batchSize: int, train_mode: bool = True,
                   resized_width: int = None, resized_height: int = None, add_voltge:bool=True, 
                   just_voltage:bool=False, crop=None, noise=0):
    '''
    crop = [[x start, x end],[y start,y end]]

    :return: a bach of data(input,output) from the all_runs_path dir,
             in the size of batchSize.
    '''
    data_iter = creat_next_data_for_cnn(all_runs_path, resized_width, resized_height, crop=crop)()
    while True:
        inputs1 = [0] * batchSize
        inputs2 = [0] * batchSize
        outputs = [0] * batchSize

        for i in range(batchSize):

            try:
                my_2_inputs , outputs[i] = next(data_iter)
                noise = np.random.normal(np.average(outputs), 1, len(outputs[i])) * noise

                outputs[i] += noise
                inputs1[i] = my_2_inputs[0]
                inputs2[i] = my_2_inputs[1]
            except StopIteration:
                if train_mode:  # todo: find out if we need to raise Error or yield an empty list
                    data_iter = creat_next_data_for_cnn(all_runs_path, resized_width, resized_height, crop=crop)()
                    my_2_inputs , outputs[i] = next(data_iter)
                    noise = np.random.normal(np.average(outputs), 1, len(outputs[i])) * noise

                    outputs[i] += noise

                    inputs1[i] = my_2_inputs[0]
                    inputs2[i] = my_2_inputs[1]
                else:
                    raise StopIteration
        a = np.array(inputs1, dtype='float32')
        b = np.array(inputs2, dtype='float32')
        c = np.array(outputs , dtype='float32')
        yield [a, b], c
        
def data_generator_for_cnn2(all_runs_path: str, batchSize: int, train_mode: bool = True,
                   resized_width: int = None, resized_height: int = None, add_voltge:bool=True, 
                   just_voltage:bool=False):
    '''
    :return: a bach of data(input,output) from the all_runs_path dir,
             in the size of batchSize.
    '''
    data_iter = creat_next_data_for_cnn(all_runs_path, resized_width, resized_height)()
    while True:
        inputs = [0] * batchSize
        outputs = [0] * batchSize
        for i in range(batchSize):
            try:
                inputs[i], outputs[i] = next(data_iter)
            except StopIteration:
                if train_mode:  # todo: find out if we need to raise Error or yield an empty list
                    data_iter = creat_next_data_for_cnn(all_runs_path, resized_width, resized_height)()
                    inputs[i], outputs[i] = next(data_iter)
                else:
                    raise StopIteration
        yield inputs, np.array(outputs , dtype='float32')

    
        
def my_fit(model, train_inputs_and_output_gen, valid_inputs_and_output_gen, batch_size=32, epochs: int = 1):
    """
    inputs_and_output_gen: a generator of: ([input1, input2], output)

    """
    for _ in range(epochs):
        flag = True
        while flag:
            try:
                # [array(images), array(size3)], array(images)
                next_bach_of_training_data = next(train_inputs_and_output_gen)
                
                model.fit(x = next_bach_of_training_data[0],
                          y = next_bach_of_training_data[1],
                          batch_size = batch_size,
                          use_multiprocessing = True,
                         )
            except StopIteration:
                while flag:
                    try:
                        next_bach_of_valid_data = next(valid_inputs_and_output_gen)
                        model.evaluate(x = next_bach_of_valid_data[0],
                                       y = next_bach_of_valid_data[1],
                                       batch_size=batch_size,
                                       use_multiprocessing=True)
                    except StopIteration:
                       flag = False


        
def split_data_to_train_valid_test(data_path, train_percent: float = 0.8,
                                   test_percent: float = 0.1):
    join = os.path.join
    from_to = lambda file, folder: move(join(data_path, file), join(data_path, folder, file))
    if train_percent + test_percent >= 1:
        raise Exception('in-valid percentages. percentages need to be in range 0 to 1 and add up to *less* than 1.')
    runs = os.listdir(data_path)
    random.shuffle(runs)
    length = len(runs)
    train_index = int(length * train_percent)
    test_index = int(length * test_percent)
    for name in 'train', 'test', 'validation':
        os.mkdir(join(data_path, name))

    for run in runs[:train_index]:
        from_to(run, 'train')
    for run in runs[train_index:train_index+test_index]:
        from_to(run, 'test')
    for run in runs[train_index+test_index:]:
        from_to(run, 'validation')

def revers_split_data_to_train_valid_test(data_path: str, dest_path: str):
    join = os.path.join
    for folder in os.listdir(data_path):
        for run in os.listdir(join(data_path, folder)):
            move(join(data_path, folder, run), join(dest_path, run))

