import re

import pandas as pd
from utils import get_files

def get_methods(lines):
    functions = []
    in_function = False
    step = 0
    for line in lines:
        if re.search(r'[^\s]', line).span()[0] <= step:
            in_function = False
        if in_function:
            functions[-1] += '\n' + line
            continue
        if 'def' in line:
            in_function = True
            functions.append(line)
            step = line.find('def')
    return functions


def get_all_data():
    files = get_files('.py')
    methods = []
    filenames = []
    for file in files:
        with file.open('r') as f:
            lines = f.read()
        lines = lines.split('\n')
        lines = [line for line in lines if len(line) > 0]
        plus = get_methods(lines)
        methods += plus
        filenames += [str(file)] * len(plus)
    return pd.DataFrame({'filename': filenames, 'method': methods})

def print_hello_world():
    print("Hello world!")

def print_hello_world_many_times(n):
    for i in range(n):
        print("Hello world")