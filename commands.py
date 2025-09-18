cmds = {}
def command (f):
    cmds[f.__name__] = f
    return f

@command
def ls (*args):
    print(f"ls {args}")

@command
def cd (*args):
    print(f"cd {args}")

@command
def exit ():
    print("Exiting...")
    quit()
