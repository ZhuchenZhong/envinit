'''
    :brief
        内建命令 / 基础命令
'''

from sys import exit

from .utils import forceRun

from typing import *


def do_exit(line: str):
    '''
    :brief  退出程序
    '''
    try:
        exit(int(line))
    except:
        exit(0)


