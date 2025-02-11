from pathlib import Path

from typing import *


def get_fileContent(
        file: Union[str, Path],
        mode: str = 'r',
        encoding: str = 'utf-8',
    ):
    with open(file, mode, encoding=encoding) as f:
        return f.read()

