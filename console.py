from commands import cmds
import os

def run (line):
    line = line.split()
    if not line: return
    cmd, *args = line
    if not cmd in cmds:
        print(f"Unknown command: " + cmd)
        return

    args = [*map(parse_arg, args)]
    if None in args:
        return
    cmds[cmd](*args)

def parse_arg (arg):
    if not arg.startswith("$"):
        return arg
    env = os.getenv(arg[1:])
    if env: return env
    print("Unknown env variable: " + arg)
    return None

if __name__ == "__main__":
    while True:
        run(input(">>> "))
