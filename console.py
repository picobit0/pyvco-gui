from commands import cmds
from argparse import ArgumentParser, ArgumentError
import os
import sys

def get_args ():
    parser = ArgumentParser(add_help=False, exit_on_error=False)
    parser.add_argument("-v", "--vfs-path")
    parser.add_argument("-s", "--script")
    argv, unknown = parser.parse_known_args()
    if unknown:
        print("Unknown arguments: " + " ".join(unknown))
        pause()
        exit()
    return argv

def pause ():
    print("Press enter to continue")
    input()

def parse_cmd_line (line):
    line = line.split()
    if not line: return None, None
    cmd, *args = line
    if cmd.startswith("$"):
        env = os.getenv(cmd[1:])
        if env: cmd = env
    return cmd, args

def run (cmd, args):
    if not cmd in cmds:
        print(f"Unknown command: " + cmd)
        return

    args = [*map(parse_cmd_arg, args)]
    if None in args:
        return
    cmds[cmd](*args)

def parse_cmd_arg (arg):
    if not arg.startswith("$"):
        return arg
    env = os.getenv(arg[1:])
    if env: return env
    print("Unknown env variable: " + arg)
    return None

if __name__ == "__main__":
    try:
        argv = get_args()
        defaultStdin = sys.stdin
        runsScript = False
        if argv.vfs_path:
            path = argv.vfs_path
            open(path).close()
        if argv.script:
            path = argv.script 
            sys.stdin = open(path)
            runsScript = True
    except ArgumentError as err:
        print(err)
        pause()
        exit()
    except FileNotFoundError:
        print("Can't access file:", path)
        pause()
        exit()
    while True:
        try:
            if runsScript:
                inp = input()
                cmd, args = parse_cmd_line(inp)
                if not cmd in cmds:
                    continue
                print(">>> " + inp)
            else:
                cmd, args = parse_cmd_line(input(">>> "))
            run(cmd, args)
        except EOFError:
            runsScript = False
            sys.stdin = defaultStdin
