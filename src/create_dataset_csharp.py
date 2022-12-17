import pandas as pd
from utils import get_files

def get_class_body(lines):
    in_class = False
    brackets = 0
    good_lines = []
    for line in lines:
        if 'class' in line: in_class = True
        if not in_class:
            continue
        if '}' in line: brackets -= 1
        if brackets > 0:
            good_lines.append(line)
        if '{' in line: brackets += 1
    return good_lines

def get_methods(lines):
    functions = []
    in_function = False
    brackets = 0
    for line in lines:
        tokens = line.split(' ')
        if tokens[0] in ['public', 'protected', 'private']:
            if '(' in line:
                in_function = True
                functions.append('')
                brackets = -1
        if not in_function:
            continue
        if '{' in line:
            brackets = 1 if brackets == -1 else brackets + 1
        if '}' in line:
            brackets -= 1
        functions[-1] += '\n' + line
        if brackets == 0:
            in_function = False
    return functions


def get_all_data():
    files = get_files('.cs')
    methods = []
    filenames = []
    for file in files:
        with file.open('r') as f:
            lines = f.read()
        lines = lines.split('\n')
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if len(line) > 0]
        plus = get_methods(get_class_body(lines))
        methods += plus
        filenames += [str(file)] * len(plus)
    return pd.DataFrame({'filename': filenames, 'method': methods})