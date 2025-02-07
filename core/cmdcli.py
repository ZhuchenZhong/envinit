'''
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
        2025-02-07

    :version
        1.0.0-beta

    :history
        1.0.0-beta
            :date  2025-02-07
            :author
                k1d(钟助辰)
            :changes
                Initial version

    :description
        交互式命令行类
'''
__all__ = [
    'CmdCli',
]

import logging
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.completion import WordCompleter

from typing import *

class CmdCli():
    """
    :brief  交互式命令行类

    :details    主循环流程
        preloop()                                                       # 循环初始化
        print(self.intro)                                               # 打印欢迎信息
        while True:
            try:
                rawInput = self.session.prompt(updatePrompt(endCode))   # 获取用户输入
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            command, args = preCommand(rawInput)                        # 处理原始输入行
            lastCommand = command                                       # 记录上一次命令
            endCode = executeCommand(command, args)                     # 执行命令
            postCommand(endCode, command, args)                         # 执行命令后处理
        postloop()                                                      # 循环结束后处理
    """

    def __init__(
        self,
        /,
        intro: str | None = None,
        useMultiLine: bool= False,
        useSuggestions: bool | None = True,
        useHistory: bool | None = True,
        logger: logging.Logger | None = None,
        debugMode: bool = False,
        commandHistoryPath: Union[str, Path] = '',
        forceNoExit: bool = False
    ):
        '''
        :param intro: str | None :None
            欢迎信息
        :param useMultiLine: bool :False
            是否启用多行输入
        :param useSuggestions: bool | None :True
            是否启用自动建议
        :param useHistory: bool | None :True
            是否启用历史记录
        :param logger: logging.Logger | None :None
            日志记录器
        :param debugMode: bool :False
            是否启用调试模式
        :param commandHistoryPath: Union[str, Path] :''
            命令历史记录文件路径
        :param forceNoExit: bool :False
            遇到错误强制继续执行
        '''
        if forceNoExit:
            try:
                self.fuckit = __import__('fuckit')
            except ModuleNotFoundError:
                import warnings, sys
                warnings.warn('Module "fuckit" not found. Please install it to use attr `forceNoExit`.')
                sys.exit(1)
        self.forceNoExit = forceNoExit

        if debugMode and logger:
            self.logger = logger
        elif debugMode and not logger:
            try:
                from rich.logging import RichHandler

                logging.basicConfig(
                    level = "NOTSET",
                    format = "%(message)s",
                    datefmt = "[%X]",
                    handlers = [RichHandler()]
                )
            except ModuleNotFoundError:
                logging.basicConfig(
                    level = "NOTSET",
                    format = "%(message)s",
                    datefmt = "[%X]",
                )

            self.logger = logging.getLogger("CmdCli")

        self.debugMode = debugMode

        self.intro = intro
        self.debugMode = debugMode
        self.commandHistoryPath = commandHistoryPath
        if not self.commandHistoryPath and debugMode:
            self.logger.warning('Command history file not found.')

        # 命令列表
        self.commandList: dict[str, Callable] = {}
        self.lastCommand: str = ''

        # 需要补全的命令列表
        self.completionCommand: list[str] = []
        self.commandCompleter = WordCompleter(self.completionCommand, ignore_case=True)

        self.session = PromptSession(
            multiline=useMultiLine,
            completer=self.commandCompleter,
            auto_suggest=AutoSuggestFromHistory() if useSuggestions else None,
            history=\
                FileHistory(self.commandHistoryPath) \
                if useHistory and self.commandHistoryPath \
                else InMemoryHistory(),
        )

    def preloop(self) -> None:
        """
        :brief  循环初始化
        """

    def updatePrompt(self, endCode: int) -> str:
        '''
        :brief  更新提示符
        '''
        return \
            f'$ '

    def preCommand(self, rawInput: str) -> Tuple[str, list[str] | None]:
        """
        :brief  处理原始输入行
        """
        rawInput = rawInput.strip().split()
        cmd, args = rawInput[0], rawInput[1:]

        return cmd, ' '.join(args)

    def executeCommand(self, command: str, args: List[str] | None) -> int:
        """
        :brief  执行命令

        :return int:    命令执行结果
            -1    : 未找到命令
            0     : 正常执行
            others: 错误
        """
        if command in self.commandList:
            return self.commandList[command](args)
        else:
            return self.default(command)

    def postCommand(self, endCode: int, command: str, args: List[str] | None) -> None:
        """
        :brief  执行命令后处理
        """

    def postloop(self) -> None:
        """
        :brief  循环结束后处理
        """

    def cmdloop(self):
        """
        :brief  主循环
        """
        endCode: int = 0
        self.lastCommand: str = ''

        self.preloop()
        print(self.intro)

        while True:
            try:
                rawInput = self.session.prompt(self.updatePrompt(endCode))
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

            command, args = self.preCommand(rawInput)
            self.lastCommand = command

            if self.forceNoExit:
                with self.fuckit:
                    endCode = self.executeCommand(command, args)
            else:
                try:
                    endCode = self.executeCommand(command, args)
                except Exception as e:
                    self.errCommand(command, rawInput, e)

            self.postCommand(endCode, command, args)

        self.postloop()

    def errCommand(self, command: str, line: str, err: Exception) -> None:
        '''
        :brief  命令执行错误处理
        '''
        if self.debugMode:
            self.logger.error(f'Command "{command} {line}" failed with error: {err}')
        else:
            print(f'Command "{command} {line}" failed with error: {err}')

    def default(self, command: str) -> int:
        '''
        :brief  默认命令

        :return int:    命令执行结果
            **MUST RETURN -1**WW
        '''
        print(f'Command "{command}" not found.')

        return -1

    def addCommand(self, commandName: str, commandFunc: Callable) -> None:
        """
        :brief  添加命令
        """
        self.commandList[commandName] = commandFunc
        self.completionCommand.append(commandName)
    
    def addCommands(self, commandDict: dict[str, Callable]) -> None:
        """
        :brief  添加多个命令
        """
        for commandName, commandFunc in commandDict.items():
            self.commandList[commandName] = commandFunc
            self.completionCommand.append(commandName)

    def delCommand(self, commandName: str) -> None:
        """
        :brief  删除命令
        """
        self.commandList.pop(commandName)
        self.completionCommand.remove(commandName)

    def updateCommand(self) -> None:
        """
        :brief  更新命令
        """
        self.commandCompleter = WordCompleter(self.completionCommand, ignore_case=True)
        self.session.completer = self.commandCompleter
