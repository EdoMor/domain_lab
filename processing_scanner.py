from hashlib import sha512, md5
import os
import typing
import PIL as pl
import numpy as np
import pandas as pd
from pandas import option_context
import imagehash
import process_assist
import process_image
import constants
from pprint import pprint
import time
import keyboard

KEY_COMBO='ctrl+i'


def keyboard_interrupt(table_file):
    print('interrupt mode[try typing help]:\n')
    from processing_scanner import search_table
    table,_=open_table(table_file)
    while 1:
        uinput=input('>>> ')
        if uinput=='help':
            print ('''type help to print this
            search_table(table_file, column: str, phrase: str): search the table (obviosly)
            get_size(start_path: str): -> size(int): get number of files in folder
            table,_ = open_table(table_file) -> (pd.DataFrame, str): then use [table] to see whats inside
            break(): to stop just break(), u know?''')
        elif uinput=='break':
            print('continuing')
            break
        try:
            eval(uinput)
        except:
            print('invalid command')


def hashfile(path):
    img = pl.Image.open(path)
    m = imagehash.dhash(img).hash.flatten()
    return int(''.join(list(m.astype(int).astype(str))), 2)


def create_table(path):
    p=1
    print('creating table...')
    files = [os.path.join(root, name) for root, dirs, files in os.walk(constants.RUNFOLDER) for name in files if
             ((not 'processed' in os.path.join(root, name)) and name.endswith('.png'))]
    print('mapped files')
    ptable = pd.DataFrame(np.zeros([len(files),4]),columns=['hash', 'path', 'name', 'status'])
    for i in range(len(files)):
        ptable.loc[i] = ([hashfile(files[i]), files[i], files[i].rsplit('\\', 1)[-1], 'unprocessed'])
        if (i%500==0 or p!=int(100*(i+1)/len(files))) and i>100:
            print('added {} images thats {}%'.format(i+1,int(100*(i+1)/len(files))))
            p=int(100*(i+1)/len(files))
    ptable.to_pickle(path)
    print('done creating table')
    return (ptable, path)


def open_table(path) -> typing.Tuple[pd.DataFrame, str]:
    print('opened table: ', path)
    return (pd.read_pickle(path), path)


def add_data(table: typing.Tuple[pd.DataFrame, str], data: list) -> typing.Tuple[pd.DataFrame, str]:
    ptable = table[0]
    path = table[1]
    ptable = ptable.append(pd.DataFrame(data, columns=list(ptable.columns)), ignore_index=True)
    print('added data: ', pd.DataFrame(data, columns=list(ptable.columns)))
    ptable.to_pickle(path)
    return (ptable, path)


def update_table_status(table: typing.Tuple[pd.DataFrame, str]) -> typing.Tuple[pd.DataFrame, str]:
    print('updating table status...')
    ptable = table[0]
    path = table[1]
    for i in range(len(ptable)):
        if os.path.exists(ptable['path'][i]):
            pass
        else:
            ptable['status'][i] = 'missing'
    ptable.to_pickle(path)
    return (ptable, path)


def update_table_contence(table: typing.Tuple[pd.DataFrame, str]) -> typing.Tuple[pd.DataFrame, str]:
    print('updating table...')
    ptable = table[0]
    path = table[1]
    files = [os.path.join(root, name) for root, dirs, files in os.walk(constants.RUNFOLDER) for name in files if
             ((not 'processed' in os.path.join(root, name)) and name.endswith('.png'))]
    for i in range(len(files)):
        if not files[i] in list(ptable['path'].values):
            ptable.loc[i] = ([hashfile(files[i]), files[i], files[i].rsplit('\\', 1)[-1], 'unprocessed'])
            ptable.to_pickle(path)
            if keyboard.is_pressed(KEY_COMBO):
                keyboard_interrupt(path)
    return (ptable, path)


def search_table(table: typing.Tuple[pd.DataFrame, str], column: str, phrase: str) -> pd.DataFrame or None:
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


def process_table(table: typing.Tuple[pd.DataFrame, str]) -> typing.Tuple[pd.DataFrame, str]:
    p=1
    print('processing...')
    ptable = table[0]
    path = table[1]
    for i in range(len(ptable)):
        if ptable['status'].loc[i] == 'unprocessed':
            process_assist.image_process(ptable['path'].loc[i])
            ptable['status'].loc[i] = 'processed'
        ptable.to_pickle(path)
        if (i%500==0 or p!=int(100*(i+1)/len(ptable))) and i>100:
            print('processed {} images thats {}%'.format(i+1,int(100*(i+1)/len(ptable))))
            p=int(100*(i+1)/len(ptable))
        if keyboard.is_pressed(KEY_COMBO):
            keyboard_interrupt(path)
    print('done processing')
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
    table_file='./ptable'
    if not os.path.exists(table_file):
        create_table(table_file)
    table = open_table(table_file)
    table = update_table_contence(table)
    table = update_table_status(table)
    table = process_table(table)
    while 1:
        size = get_size(constants.RUNFOLDER)
        start=time.time()
        while time.time()-start<=(60 * 5):
            if keyboard.is_pressed(KEY_COMBO):
                keyboard_interrupt(table_file)
        if get_size(constants.RUNFOLDER) != size:
            table = update_table_contence(table)
            table = update_table_status(table)
            table = process_table(table)



if __name__ == '__main__':
    main()

