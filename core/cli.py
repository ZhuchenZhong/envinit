import os
import time

import colorama

from .cmdcli import CmdCli

from typing import *

############################################################
colorama.init(True)

class EnvMgrCmdCli(CmdCli):
    def preloop(self):
        """
        :brief  循环初始化
        """

        self.builtinCommands = {}

        # 导入内建命令
        for bticmd in dir(self):
            if bticmd.startswith('bti_'):
                self.builtinCommands[bticmd[4:]] = getattr(self, bticmd)
                self.logger.debug(f"Loaded builtin command: {bticmd}")

        self.addCommands(self.builtinCommands)

    def bti_help(self, line: str):
        '''
        :brief  显示帮助信息
        '''
        if not line:
            print("Available commands:")
            for cmd in self.commandList:
                print(f"  {cmd}")
        else:
            if line in self.commandList:
                print(f"Help for {line}:")
                print(self.commandList[line].__doc__)
            else:
                return self.default(line)

    def bti_exitcode(self, line: str):
        '''
        :brief  显示上一个命令的退出码
        '''
        print(self.lastCommandExitCode)

    def updatePrompt(self, endCode):
        """
        'Sun Feb  9 20:03:28 2025'
        > 20:03:30 | 9 Feb, Sunday | C:> WINDOWS>system32
        $ 
        """
        print( \
            f"> " \
            f"{colorama.Fore.CYAN + time.strftime('%H:%M:%S') + colorama.Style.RESET_ALL} | " \
            f"{colorama.Fore.GREEN + time.strftime('%d %b, %A') + colorama.Style.RESET_ALL} | " \
            f"{colorama.Fore.MAGENTA + os.getcwd() + colorama.Style.RESET_ALL}" \
        )
        return "$ "

    def executeCommand(self, command, args):
        '''
        :brief  执行命令

        :attention  重写了父类的方法，增加了内建命令的支持
        '''
        if command in self.builtinCommands:
            return self.builtinCommands[command](args)
        elif command in self.commandList:
            return self.commandList[command](args)
        else:
            return self.default(command)
