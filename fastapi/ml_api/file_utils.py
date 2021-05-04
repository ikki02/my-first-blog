import os
import shutil
import gc
import string
from random import choice

import pandas as pd

storage = os.path.join(os.path.dirname(__file__), 'data', 'output')


def get_filepath(length=8):
    letters = string.ascii_lowercase
    filename = ''.join(choice(letters) for i in range(length)) + '.csv'
    filepath = os.path.join(storage, 'storage', filename)
    return filepath


def check_csv(df):
    expected = ['item_id', 'sold_price', 'diff_price', 'capital_area', 'status', 'size', 'listing_at_spring']
    if df.columns.tolist() == expected:
        flag = True
    else:
        flag = False
    return flag
    

async def save_csv(df, save_path):
    '''本APIではローカルに保存するが、本番ではGCSなどのストレージに保存することも可能'''
    df.to_csv(save_path, index=False)


async def cleanup(filename, df):
    if os.path.isfile(filename):
        os.remove(filename)
    del df
    gc.collect()


def save_outputs(df, filename):
    filepath = os.path.join(storage, 'predicted', 'predicted_' + filename)
    df.to_csv(filepath)
    return filename


def check_outputs(filename: str):
    filepath = os.path.join(storage, 'predicted', 'predicted_' + filename)
    return os.path.exists(filepath)


async def load_outputs(filename: str):
    filepath = os.path.join(storage, 'predicted', 'predicted_' + filename)
    df = pd.read_csv(filepath)
    preds = df.to_dict(orient='records')
    return preds
