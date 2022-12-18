from constants import SOURCE_CODE_PATH
import os

def get_files(format):
    files = []
    folders = []
    if SOURCE_CODE_PATH.is_dir():
        folders.append(SOURCE_CODE_PATH)
    elif SOURCE_CODE_PATH.suffix == format:
        files.append(SOURCE_CODE_PATH)
    while len(folders) != 0:
        folder = folders.pop()
        content = [folder / file for file in os.listdir(folder)]
        files += [elem for elem in content if elem.suffix == format]
        folders += [elem for elem in content if elem.is_dir()]
    return files