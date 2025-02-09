"""
    :author
        k1d(钟助辰)
            :contact
                Mail/cps3362521@gmail.com
                Github/ZhuchenZhong
    
    :license
        Mozilla Public License 2.0
    
    :brief
        管理环境工具
    
    :github
        https://github.com/ZhuchenZhong/envinit
    
    :date
        2025-02-05

    :version
        0.0.1
    
    :history
        0.0.1
            :date  2025-02-05
            :author
                k1d(钟助辰)
            :changes
                Initial version
    
    :description
        对Windows下开发/运行环境进行管理
"""
__version__ = "0.0.1"
__author__ = "k1d(钟助辰)"

# import PyInstaller

import asyncio
import logging

import colorama

from rich.logging import RichHandler

import core

from typing import *

############################################################

colorama.init(True)

asyncio.get_event_loop().set_debug(False)
logging.getLogger("asyncio").setLevel(logging.INFO)

logging.basicConfig(
    level = "NOTSET",
    format = "%(message)s",
    datefmt = "[%X]",
    handlers = [RichHandler()]
)
logger = logging.getLogger("envinit")
logger.setLevel(logging.DEBUG)

root = core.user.get("envinit")
# root.mkdir(exist_ok = True)

__systemInfo = __import__("platform").uname()
__cmdcliIntro = (
    f"ENVINIT {colorama.Fore.GREEN + __version__ + colorama.Style.RESET_ALL}"
    + f" | {colorama.Fore.CYAN + __import__('time').asctime() + colorama.Style.RESET_ALL}\n"
    + f"@ {colorama.Fore.BLUE + __systemInfo.system + __systemInfo.version + colorama.Style.RESET_ALL}"
    + f" / {colorama.Fore.WHITE + __systemInfo.node + colorama.Style.RESET_ALL}\n"
)

############################################################

if not (core.init()):
    pass

cli = core.cli.EnvMgrCmdCli(
    intro = __cmdcliIntro,
    logger = logger,
    debugMode = True,
)

logger.debug(f"Cli Cmd Loaded {core.cmds.commands}")
cli.addCommands(core.cmds.commands)

## 添加内建命令(需要在主程序中添加的)
# version       显示版本信息
cli.addCommand("version", lambda line: print(__cmdcliIntro))

try:
    cli.cmdloop()
except Exception as e:
    logger.error(e)
    logger.error("An error occurred. Please check the error message above.")
    logger.error("If you can't solve the problem, please submit an issue on GitHub.")
    logger.error("GitHub: https://github.com/ZhuchenZhong/envinit")
