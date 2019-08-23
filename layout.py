#!/usr/bin/python3.7
"""
Script for showing my layout on polybar
"""
import i3ipc



def update_layout( i3con ):
    layout = i3.get_tree().find_focused().parent.layout 
    if   layout == "splitv":
        print( "" )
    elif layout == "splith":
        print( "" )
    elif layout == "tabbed":
        print( "" )
    elif layout == "stacked":
        print( "" )
    else:
        print( "#" )
    pass


if __name__ == '__main__':
    i3 = i3ipc.Connection(auto_reconnect=True)

    update_layout( i3 )

