commands = {}

from . import cmd_builtin

for cmds in dir():
    if not cmds.startswith('cmd_'):
        continue

    for cmd in dir(eval(cmds)):
        if cmd.startswith('do_'):
            commands[cmd[3:]] = eval(f'{cmds}.{cmd}')

