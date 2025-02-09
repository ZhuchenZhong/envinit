'''
    :brief
        内建命令 / 基础命令
'''
import os
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
    os.system("cls")

def do_cd(line: str):
    '''
    :brief  切换目录
    '''
    try:
        return os.chdir(line)
    except FileNotFoundError:
        print(f"cd: {line}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {line}: Not a directory")
    except PermissionError:
        print(f"cd: {line}: Permission denied")

