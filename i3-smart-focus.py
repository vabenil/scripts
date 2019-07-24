#!/usr/bin/env python3

""" Focus tiling container if window is floating and U is attempted """

import i3ipc
import sys
import subprocess
import os.path

REG_FILE_PATH = "/tmp/focus-register"

targets = [
    "left",
    "right",
    "down",
    "up",
    "float",
    "parent",
    "child",
    "last"
]

flags = [
    'repeat-last',
    'scratchpad-next',
    'fullscreen-next',
    'fullscreen-prev',
     'mark',
    'instance',
    'class'
]

usage = ("Usage:\nsmart-focus [flags] [target]\n"
        "\nTarget:\n"
        "    left\n"
        "    right\n"
        "    down\n"
        "    up\n"
        "    float\n"
        "    parent\n"
        "    child\n"
        "    last\n"
        "\nFlags:\n"
        "    --mark <mark>\n"
        "    --scratchpad-next\n"
        "    --fullscreen-next\n"
        "    --fullscreen-prev\n"
        "    --instance <instance>\n"
        "    --class <class>")

def save_to_reg( command ):
    try:
        reg_file = open( REG_FILE_PATH, "w" )
        reg_file.write( command )
        reg_file.close()
    except Exception:
        pass

def repeat_last():
    if not os.path.exists( REG_FILE_PATH ):
        print( "file %s do not exist" )
        exit( 1 )

    try:
        reg_file = open( REG_FILE_PATH, "r" )
    except Exception:
        print( "Couldn't open file %s" % REG_FILE_PATH )
        exit( 1 )
    else:
        last_fcommand = reg_file.read().split()
        reg_file.close()
    
    print( last_fcommand )
    subprocess.run( last_fcommand )
    exit( 0 )


def scratch_next():
    focused = tree.find_focused()

    # Hide window
    if focused.parent.scratchpad_state != "none":
        i3.command("[con_id=%d] scratchpad show" % focused.id)

    scratch_windows = tree.scratchpad().leaves()

    if focused in scratch_windows:
        current_index = scratch_windows.index( focused )
    else:
        current_index = -1

    next_win = scratch_windows[ current_index - 1 if current_index != 0 else len(scratch_windows) - 1 ]

    command = "[con_id=%d] scratchpad show" % next_win.id

    if focused.fullscreen_mode:
        command += ", fullscreen toggle"

    i3.command(command)
    save_to_reg( "i3-smart-focus --scratchpad-next" )

# Focus the first window with x instance
def focus_instance( instance ):
    instanced = tree.find_instanced( instance )[0]
    
    if instanced.parent.scratchpad_state != "none":
        command = "[instance=%s] scratchpad show" % instance
    else:
        command = "[instance=%s] focus" % instance

    if focused.fullscreen_mode:
        command += ", fullscreen toggle"

    i3.command(command)
    save_to_reg( "i3-smart-focus --instance %s" % instance )

def focus_marked( mark ):
        marked_windows = tree.find_marked(mark)

        if not marked_windows:
            print( "No windows marked as %s" % mark )
            exit( 1 )

        if marked_windows[0].parent.scratchpad_state != "none":
            command = "[con_mark=%s] scratchpad show" % mark
        else:
            command = "[con_mark=%s] focus" % mark

        if focused.fullscreen_mode:
            command += ", fullscreen toggle"

        i3.command(command)
        save_to_reg( "i3-smart-focus --mark %s" % mark )

def focus_fullscreen( forward=True ):
    workspace = focused.workspace()
    windows = workspace.leaves()
    win_num = len( windows )

    if focused in windows:
        win_index = windows.index( focused )
        
        if forward:
            next_win = windows[ win_index + 1 if win_index != win_num - 1 else 0 ]
        else:
            next_win = windows[ win_index - 1 if win_index != 0 else win_num - 1 ]

        command = "[con_id=%d] focus, fullscreen toggle" % next_win.id
        i3.command( command )
    else:
        print( "Unexpected error" )


def focus_class():
    pass

def focus_floating():
    i3.command('focus mode_toggle')

def focus_parent():
    i3.command('focus parent')

def focus_child():
    i3.command('focus child')

def focus_last():
    subprocess.run(['i3-focus-last', '--switch'])

def focus_left():
    win_id = focused.id
    if is_fullscreen:
        focus_fullscreen( forward=False )
    elif is_fterm:
        subprocess.run(['xdotool', 'key', '-window', str(win_id), 'alt+p']) 
    elif is_floating:
        i3.command('focus left')
    else:
        i3.command('focus left')

def focus_right():
    if is_fullscreen:
        focus_fullscreen()
    elif is_fterm:
        subprocess.run(['xdotool', 'key', '-window', str(win_id), 'alt+n']) 
    elif is_floating:
        i3.command('focus right')
    else:
        i3.command('focus right')

def focus_down():
    if is_fullscreen:
        focus_fullscreen( forward=False )
    elif is_fterm:
        subprocess.run(['xdotool', 'key', '-window', str(win_id), 'alt+n']) 
    elif is_floating:
        i3.command('focus down')
    else:
        i3.command('focus down')

def focus_up():
    if is_fullscreen:
        focus_fullscreen()
    elif is_fterm:
        subprocess.run(['xdotool', 'key', '-window', str(win_id), 'alt+n']) 
    elif is_floating:
        i3.command('focus up')
    else:
        i3.command('focus up')



if __name__ == '__main__':
    # I do not know why I didn't use a argument parser
    # but I already wrote all this so whatever
    if len(sys.argv) < 2:
        print( "Not enough arguments" )
        print( usage )
        exit()
    elif len(sys.argv) == 2:
        if sys.argv[1][0:2] == "--":
            flag = sys.argv[1][2:]
            target = ''
            
            if flag not in flags:
                print( "'%s' is not a valid flag" % flag  )
                print( usage )
                exit( 1 )
            elif flag == 'repeat-last':
                repeat_last()
            elif flag[-4:] != 'next' and flag[-4:] != 'prev':
                print( "Not enough arguments" )
                print( usage )
                exit( 1 )
        else:
            flag = ''
            target = sys.argv[1]

            if target not in targets:
                print( "'%s' is not a valid target" )
                print( usage )
                exit( 1 )
    elif len(sys.argv) == 3:
        if sys.argv[1][0:2] == "--":
            flag = sys.argv[1][2:]
            target = sys.argv[2]

            if flag not in flags:
                print( "'%s' is not a valid flag" % flag)
                print( usage )
                exit()
        else:
            print( "flags must have '--' as prefix" )
            print( usage )
            exit()
    else:
        print( "To many arguments" )
        print( usage )
        exit( 1 )

    i3 = i3ipc.Connection()
    tree = i3.get_tree()
    focused = i3.get_tree().find_focused()

    is_fterm = True if focused.window_instance == "floating_term" else False
    is_floating = True if (focused.floating == "auto_on" or focused.floating == "user_on") else False
    is_fullscreen = focused.fullscreen_mode


    if flag:
        if flag == 'scratchpad-next':
            scratch_next()
        elif flag == 'mark':
            focus_marked( target )
        elif flag == 'instance':
            focus_instance( target )
        elif flag == 'class':
            focus_class( target )
    else:
        if   target == 'float':
            focus_floating()
        elif target == 'parent':
            focus_parent()
        elif target == 'child':
            focus_child()
        elif target == 'last':
            focus_last()
        elif target == 'left':
            focus_left()
        elif target == 'right':
            focus_right()
        elif target == 'down':
            focus_down()
        elif target == 'up':
            focus_up()


