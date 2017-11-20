import inspect
import os
import pickle
from pathlib import Path


def load_or_create(relative_path,function_to_exec):
    """
    return saved version or generates and returns
    example:a=load_or_create("/Matrix/UIDToLikes.matrix",create_matrix_user_likes)
    :param relative_path: relative path in / format where last string will be filename
    :param function_to_exec: a function which generates what to store
    :return: return the result of the saved version
    """
    abs_file_name=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+relative_path
    my_file = Path(abs_file_name)
    os.makedirs(os.path.dirname(my_file), exist_ok=True)
    my_file = Path(abs_file_name)
    if my_file.is_file():
        print("Loading from file...")
        with open(my_file, 'rb') as handle:
            to_return = pickle.load(handle)
    else:
        with open(my_file, 'wb') as handle:
            to_return=function_to_exec()
            pickle.dump(to_return, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return to_return
