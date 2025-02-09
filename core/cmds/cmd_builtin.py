'''
    :brief
        内建命令 / 基础命令
'''
from os import system
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

def do_clear(line: str):
    '''
    :brief  清屏
    '''
    system("cls")


