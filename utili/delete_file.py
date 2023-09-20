import os
import pathlib


def delete_all(path):
    for path in pathlib.Path(path).iterdir():
        if path.is_file() and not path.stem.startswith('.'):
            os.remove(path)

def delete_one(path):
    os.remove(path)