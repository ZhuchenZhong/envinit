import fuckit
from typing import Callable

def forceRun(func: Callable):
    def wrapper(*args, **kwargs):
        with fuckit:
            func(*args, **kwargs)

    return wrapper

