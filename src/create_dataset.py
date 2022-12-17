from constants import CODE_TYPES
from create_dataset_csharp import get_all_data as get_csharp
from create_dataset_python import get_all_data as get_python

import pandas as pd

def create_dataset_one_type(code_type):
    if code_type == 'CSHARP':
        return get_csharp()
    return get_python()


def create_dataset():
    dfs = []
    for code_type in CODE_TYPES:
        df = create_dataset_one_type(code_type)
        df['code_type'] = code_type
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


df = create_dataset()
print(df)
df.to_csv('result.csv')