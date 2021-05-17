import os
import shutil
from typing import *

PATH = './runs/'
COPY_IMG_FROM_THIS_PATH = './from_raw/'


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
    f = open(PATH + 'run_counter.txt', 'w')
    f.write(f'{count}')
    f.close()

    files_name_to_copy = os.listdir(COPY_IMG_FROM_THIS_PATH)

    for f in files_name_to_copy:
        shutil.copy(COPY_IMG_FROM_THIS_PATH + f, folder_name)
        os.remove(COPY_IMG_FROM_THIS_PATH + f)


if __name__ == '__main__':
    make_run_files()
