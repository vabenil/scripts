#!/usr/bin/python3.7
""" Open new terminal as a new window or as a new tab in tabbed """
import i3ipc
import os
import subprocess


i3 = i3ipc.Connection()
focused = i3.get_tree().find_focused()
win_id = focused.window

TERM = os.environ['TERMINAL']

if focused.window_class == 'tabbed':
    subprocess.run([TERM, "-w", str(win_id)])
else:
    subprocess.run([TERM])
