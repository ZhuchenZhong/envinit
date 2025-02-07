'''
    :author
        k1d(钟助辰)
        Python 2.7.11
    
    :brief
        获取用户目录

    :date
        2025-02-07
    
    :version
        2.0.1
    
    :history
        2.0.1
            :date  2025-02-07
            :author
                k1d(钟助辰)
            :changes
                Remove unused code
        1.0.0
            :date  2023-12-10
            :author
                Copied from Python Standard Library 2.7.11/user.py
            :changes
                Initial version
'''

import os
from pathlib import Path

home = os.curdir
if "HOME" in os.environ:
    home = os.environ["HOME"]
elif os.name == "posix":
    home = os.path.expanduser("~/")
elif os.name == "nt":
    if "HOMEPATH" in os.environ:
        if "HOMEDRIVE" in os.environ:
            home = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"]
        else:
            home = os.environ["HOMEPATH"]


def get(app: str | None = None) -> Path:
    """
    :param app(str): 配置名称
    :return Path   : home/.{app}
    """
    return Path(home, "." + app if app else "")
