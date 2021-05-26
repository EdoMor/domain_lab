import os
import shutil
from typing import *

PATH = './runs/'
COPY_PROCESSED_IMG_FROM_THIS_PATH = './from_raw/'
COPY_RAW_IMG_FROM_THIS_PATH = './lab_images_raw/'

# clean:
# f = open(PATH + 'run_counter.txt', 'w')
# f.write('0')
# f.close()


def make_run_files(run_name: Optional[str] = None):
    f = open(PATH + 'run_counter.txt', 'r').read()
    # print(f)
    count = int(f) + 1
    folder_name = PATH + f'run_{count}' + ('' if run_name is None else f'_{run_name}')
    os.mkdir(folder_name)
    os.mkdir(folder_name+'/pressed')
    os.mkdir(folder_name+'/raw')
    f = open(PATH + 'run_counter.txt', 'w')
    f.write(f'{count}')
    f.close()

    processed_files_name_to_copy = os.listdir(COPY_PROCESSED_IMG_FROM_THIS_PATH)
    raw_files_name_to_copy = os.listdir(COPY_RAW_IMG_FROM_THIS_PATH)


    for f in processed_files_name_to_copy:
        shutil.copy(COPY_PROCESSED_IMG_FROM_THIS_PATH + f, folder_name+'/pressed')
        os.remove(COPY_PROCESSED_IMG_FROM_THIS_PATH + f)
    for f in raw_files_name_to_copy:
        shutil.copy(COPY_RAW_IMG_FROM_THIS_PATH + f, folder_name + '/raw')
        os.remove(COPY_RAW_IMG_FROM_THIS_PATH + f)

    return folder_name

if __name__ == '__main__':
    make_run_files()
