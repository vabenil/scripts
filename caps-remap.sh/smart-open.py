#!/usr/bin/python3.7


import i3ipc
import subprocess


i3 = i3ipc.Connection()
focused = i3.get_tree().find_focused()
win_id = focused.window

if focused.window_instance == 'floating_term':
    subprocess.run(["xdotool", "key", "-window", str(win_id), "alt+Return"])
else:
    subprocess.run(['st'])
