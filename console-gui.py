import tkinter as tk
from async_backend import AsyncBackend
import sys
from time import time

backend = "py console.py"

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
    
window = tk.Tk()
window.title("console - " + sys.argv[0])
icons = [(tk.PhotoImage(file=path), dur) for path, dur in icons]

field = tk.Text(window, **theme)
field.pack(fill="both", expand=True)
field.bind("<<Modified>>", on_modified)
parsedText = ""
prevText = ""
nextTime = time()
iconIdx = 0

back = AsyncBackend(backend)
back.start()
try:
    while back:
        line = back.try_get()
        if line: write(line)
        update_icon()
        window.update()
    window.destroy()
except tk._tkinter.TclError:
    pass
finally:
    back.stop()
