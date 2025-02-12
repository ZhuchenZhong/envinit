"""
    :author
        k1d(钟助辰)
            :contact
                Mail/cps3362521@gmail.com
                Github/ZhuchenZhong

    :license
        MIT

    :brief
        这是一个基于prompt_toolkit的交互式命令行通用实现模块

    :date
        2025-02-12

    :version
        2.0.0

    :history
        2.0.0
            :date  2025-02-12
            :BREAKING CHANGES
                refactor.
                    在 `1.1.0` 的基础上整体重构
            :changes
                feat.
                    增加了特殊命令的支持
        1.1.0
            :date  2025-02-12
            :BREAKING CHANGES
                refactor.
                    1)  重构了debugmod的逻辑
                            将logging.debug -> logging.info
            :changes
                feat.
                    1)  增加了内建命令的支持(命令参数包含self)
                    2)  增加了命令集的支持
                    3)  增加了路径补全的支持
                fix.
                    1)  优化了mainloop调用逻辑
                    2)  修复了错误提示
        1.0.0-beta
            :date  2025-02-07
            :author
                k1d(钟助辰)
            :changes
                Initial version

    :description
        交互式命令行类
"""

__all__ = [
    "CmdCli",
    "CommandSet"
]

import logging
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.completion import Completer, Completion

from typing import *

class CommandSetMeta(type):
    """
    :brief
        命令集元类
    """

    subclasses: List = []

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if cls.__name__ != "CommandSet":
            CommandSetMeta.subclasses.append(cls)

class CommandSet(metaclass=CommandSetMeta):
    """
    :brief
        命令集基类
    
    :description
        命令以方法的形式实现
        若命令参数包含self, 则为内建命令

        内建命令以 `bti_` 开头
        普通命令以 `cmd_` 开头
    """
