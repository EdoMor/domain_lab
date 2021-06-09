from hashlib import sha512, md5
import os
import PIL as pl
import numpy as np
import pandas as pd
from pandas import option_context

import process_assist
import process_image
import constants
from pprint import pprint
import time


def hashfile(path):
    img = pl.Image.open(path)
    data = np.asarray(img).flatten()
    m = sha512()
    m.update(data.tobytes())
    return m.digest()


def create_table(path):
    files = [os.path.join(root, name) for root, dirs, files in os.walk(constants.RUNFOLDER) for name in files if
             'raw' in os.path.join(root, name)]
    ptable = pd.DataFrame(columns=['hash', 'path', 'name', 'status'])
    for i in range(len(files[1:10])):  # DEBUG ONLY REMOVE [1:10]
        ptable.loc[i] = ([hashfile(files[i]), files[i], files[i].rsplit('\\', 1)[-1], 'unprocessed'])
    ptable.to_pickle(path)
    return (ptable, path)


def open_table(path) -> (pd.DataFrame, str):
    return (pd.read_pickle(path), path)


def add_data(table: (pd.DataFrame, str), data: list) -> (pd.DataFrame, str):
    ptable = table[0]
    path = table[1]
    ptable = ptable.append(pd.DataFrame(data, columns=list(ptable.columns)), ignore_index=True)
    ptable.to_pickle(path)
    return (ptable, path)


def update_table_status(table: (pd.DataFrame, str)) -> (pd.DataFrame, str):
    ptable = table[0]
    path = table[1]
    for i in range(len(ptable)):
        if os.path.exists(ptable['path'][i]):
            pass
        else:
            ptable['status'][i] = 'missing'
    ptable.to_pickle(path)
    return (ptable, path)


def update_table_contence(table: (pd.DataFrame, str)) -> (pd.DataFrame, str):
    ptable = table[0]
    path = table[1]
    files = [os.path.join(root, name) for root, dirs, files in os.walk(constants.RUNFOLDER) for name in files if
             'raw' in os.path.join(root, name)]
    for i in range(len(files)):
        if not files[i] in ptable['name']:
            ptable.loc[i] = ([hashfile(files[i]), files[i], files[i].rsplit('\\', 1)[-1], 'unprocessed'])
    ptable.to_pickle(path)
    return (ptable, path)


def search_table(table: (pd.DataFrame, str), column: str, phrase: str) -> pd.DataFrame or None:
    ptable = table[0]
    path = table[1]
    results = pd.DataFrame(columns=list(ptable.columns))
    for i in range(len(ptable)):
        if ptable[column][i] == phrase:
            results.loc[i] = ptable.loc[i]
    if len(results) == 0:
        return None
    else:
        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):
            print(results)
            return results


def process_table(table: (pd.DataFrame, str)) -> (pd.DataFrame, str):
    ptable = table[0]
    path = table[1]
    for i in range(len(ptable)):
        if ptable['status'].loc[i] == 'unprocessed':
            process_assist.process(ptable['path'].loc[i])
            ptable['status'].loc[i] = 'processed'
    ptable.to_pickle(path)
    return (ptable, path)


def get_size(start_path: str) -> int:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(p)

def main():
    if not os.path.exists('./t1_not_a_virus'):
        create_table('./t1_not_a_virus')
    table = option_context('./t1_not_a_virus')
    table = update_table_contence(table)
    table = update_table_status(table)
    table = process_table(table)
    while 1:
        time.sleep(60 * 5)
        size = get_size(constants.RUNFOLDER)
        if get_size(constants.RUNFOLDER) != size:
            table = update_table_contence(table)
            table = update_table_status(table)
            table = process_table(table)



if __name__ == '__main__':
    main()
