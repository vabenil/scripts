#!/usr/bin/env python3
import re
import subprocess

""""
Switch between layouts
"""

# Layouts to switch to
layouts = [ "us", "ru" ]

layout_query = subprocess.run(['setxkbmap', '-query'], stdout=subprocess.PIPE)\
        .stdout.decode('utf-8')

layout = re.search('layout:\s+(\w+)', layout_query).group(1) 

layout_indx = layouts.index( layout ) if layout in layouts else -1

isLast = True if layout_indx == len(layouts)-1 else False


if layout_indx != -1:
    next_layout = layouts[ 0 if isLast else (layout_indx + 1) ]
    variant = "phonetic" if next_layout == "ru" else ''

    subprocess.run(['setxkbmap', next_layout, variant]) 
else:
    next_layout = "us"
    print("%s" % (next_layout))
    subprocess.run(['setxkbmap', next_layout]) 




