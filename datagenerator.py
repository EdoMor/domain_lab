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


def reshape_for_net(img, resized_width: int = None, resized_height: int = None):
    # ensures all images be the same size:
    if resized_height is not None:
        img = cv2.resize(img, (resized_width, resized_height))
    # tern img to zeros and ones:
    img = img / 255
    # flatten img to a vector
    return img.flatten()


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


def next_data(all_runs_path: str, resized_width: int = None, resized_height: int = None):
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




if __name__ == '__main__':
   data_path = r'H:\runs_processed'
   split_data_to_train_valid_test(data_path)
