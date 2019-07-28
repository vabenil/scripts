#!/usr/bin/python3.7

"""
Scroll window title, requires i3 

Created to scroll window title in polybar.

Usage example in a bash script:
    for i in $(seq 1 100);
    do
        script.py 60 $i
    done

 """

import i3ipc
import sys


argc = len(sys.argv)
args = sys.argv

usage = "Usage:\nscript.py <Max length> <N (First char index)>" 
if argc < 3:
    print( "Not enough arguments" )
    print( usage )
    exit( -1 )

try:
    max_len   = int( args[ 1 ] )
    n         = int( args[ 2 ] )
except ValueError:
    print( "First and second arguments must be integers" ) 
    exit ( -1 )

i3 = i3ipc.Connection()
focused = i3.get_tree().find_focused()

title = focused.name
title_len = len( title )

if title_len <= max_len:
    padding = round( 0.5 * ( max_len - title_len ) ) * ' '
    print( "%s%s%s" % (padding, title, padding) )
    exit()

spacing = ' ' * max_len
full_title = title + spacing
full_len = title_len + max_len

n = n if n < full_len else ( ( n % (full_len)) )
last_indx = n + max_len 

full_title += full_title[ 0 : n ]

screen_buffer = full_title[ n : last_indx]

print( screen_buffer )
