import os
import pandas as pd


def import_csv_file(path_to_file, index=False, column_names=False):
    if not os.path.exists(path_to_file):
        return None

    if index:
        index = 0
    else:
        index = None

    if column_names:
        column_names = 0
    else:
        column_names = None
    return pd.read_csv(path_to_file, index_col=index, header=column_names)
