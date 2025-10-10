import tkinter as tk
from async_backend import AsyncBackend
from time import time
from argparse import ArgumentParser, ArgumentError
import sys
import os

backend = f"py {sys.path[0]}\\console.py"

theme = {
    "background": "#222222",
    "foreground": "white",
    "insertbackground": "white",
    "selectbackground": "#777777",    
}

icons = (
    ("assets/icon-frame1.png", 0.6),
    ("assets/icon-frame2.png", 0.3)    
)

def get_args ():
    parser = ArgumentParser(add_help=False, exit_on_error=False)
    parser.add_argument("-v", "--vfs-path")
    argv, unknown = parser.parse_known_args()
    return argv

def get_end (text):
    line = text.count("\n")
    idx = text.rfind("\n")
    return line + 1, len(text) - idx - 1

def on_modified (event):
    global prevText, parsedText
    text = field.get("1.0", "end")[:-1]
    field.edit_modified(False)
    if not text.startswith(parsedText):
        field.replace("1.0", "end", prevText)
        line, char = get_end(prevText)
        field.mark_set("insert", f"{line}.{char}")
        field.see(f"{line}.{char}")
    else:
        prevText = text
        new = text[len(parsedText):].split("\n")[:-1]
        for line in new:
            back.send(line + "\n")
            parsedText += line + "\n"
        

def write (s):
    global parsedText
    s = s.replace("\r\n", "\n")
    text = field.get("1.0", "end")[:-1]
    parsedText += s
    field.replace("1.0", "end", parsedText)
    prevText = parsedText
    line, char = get_end(prevText)
    field.mark_set("insert", f"{line}.{char}")
    field.see(f"{line}.{char}")
    field.edit_modified(False)

def update_icon():
    global nextTime, iconIdx
    icon = None
    while time() > nextTime:
        iconIdx += 1
        icon, dur = icons[iconIdx % len(icons)]
        nextTime += dur
    if (icon): window.wm_iconphoto(False, icon)

def on_destroy():
    global destroyed
    destroyed = True

defaultDir = os.getcwd()
os.chdir(sys.path[0])
destroyed = False
window = tk.Tk()
window.protocol("WM_DELETE_WINDOW", on_destroy)

vfs_path = "*default vfs*"
try:
    args = get_args()
    if args.vfs_path:
        vfs_path = '"' + args.vfs_path + '"'
except ArgumentError:
    vfs_path = "*vfs error*"
    
window.title("console - " + vfs_path)

icons = [(tk.PhotoImage(file=path), dur) for path, dur in icons]

field = tk.Text(window, **theme)
field.pack(fill="both", expand=True)
field.bind("<<Modified>>", on_modified)
parsedText = ""
prevText = ""
nextTime = time()
iconIdx = 0

os.chdir(defaultDir)
args = " ".join(sys.argv[1:])
back = AsyncBackend(backend + " " + args)
back.start()
try:
    while back:
        line = back.try_get()
        if line: write(line)
        if destroyed:
            back.send("exit\n")
            break
        update_icon()
        window.update()
    window.destroy()
finally:
    back.stop()
