import scipy.sparse as sparse
import numpy as np
import os,inspect
from pathlib import Path

def save_sparse_matrix(filename, x):
    x_coo = x.tocoo()
    row = x_coo.row
    col = x_coo.col
    data = x_coo.data
    shape = x_coo.shape
    np.savez(filename, row=row, col=col, data=data, shape=shape)

def load_sparse_matrix(filename):
    y = np.load(filename)
    z = sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])
    return z.tolil()

def create_or_load_sparse_matrix(relative_path,function_to_exec):
    abs_file_name=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+relative_path
    my_file = Path(abs_file_name)
    os.makedirs(os.path.dirname(my_file), exist_ok=True)
    my_file = Path(abs_file_name)
    if my_file.is_file():
        print("Loading from file...")
        with open(my_file, 'rb') as handle:
            to_return = load_sparse_matrix(handle)
    else:
        with open(my_file, 'wb') as handle:
            to_return=function_to_exec()
            print("Dumping to the returned value to file")
            save_sparse_matrix(handle,to_return)