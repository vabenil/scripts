#!/usr/bin/env python3

""" Focus tiling container if window is floating and U is attempted """

import i3ipc
import sys
import subprocess
import os.path

REG_FILE_PATH = '/tmp/focus-register'

# REQUIRED
# path to this script
I3_SMART_FOCUS = os.path.abspath(__file__)
# Keys to pass to xdotool to focus next|prev tabbed window.
# If you don't use tabbed you can ignore it, or if you use tmux you could modify it to work with tmux.
TABBED_FOCUS_NEXT = 'alt+n'
TABBED_FOCUS_PREV = 'alt+p'

targets = [
        'left',
        'right',
        'down',
        'up',
        'float',
        'parent',
        'child',
        ]

flags = [
        'help',
        'repeat-last',
        'scratchpad-next',
        'fullscreen-next',
        'fullscreen-prev',
        'mark',
        'instance',
        'class'
        ]

usage = ('Usage:\nsmart-focus [flags] [target]\n'
        '\nTargets:\n'
        '    left\n'
        '    right\n'
        '    down\n'
        '    up\n'
        '    float\n'
        '    parent\n'
        '    child\n'
        '\nFlags:\n'
        '    --help\n'
        '    --mark <mark>\n'
        '    --scratchpad-next\n'
        '    --fullscreen-next\n'
        '    --fullscreen-prev\n'
        '    --instance <instance>\n'
        '    --class <class>')

def save_to_reg(command):
    try:
        reg_file = open(REG_FILE_PATH, "w")
        reg_file.write(command)
        reg_file.close()
    except Exception:
        pass

def repeat_last():
    if not os.path.exists(REG_FILE_PATH):
        print("file %s do not exist" % REG_FILE_PATH)
        exit(1)

    try:
        reg_file = open(REG_FILE_PATH, "r")
    except Exception:
        print("Couldn't open file %s" % REG_FILE_PATH)
        exit(1)
    else:
        last_fcommand = reg_file.read().split()
        reg_file.close()

    print(last_fcommand)
    sys.argv = last_fcommand
    exec(open(I3_SMART_FOCUS).read())
    exit(0)


def scratchpad_next():
    # Hide window
    if focused.parent.scratchpad_state != "none":
        i3.command("[con_id=%d] scratchpad show" % focused.id)

    scratch_windows = tree.scratchpad().leaves()

    if focused in scratch_windows:
        current_index = scratch_windows.index(focused)
    else:
        current_index = -1

    next_win = scratch_windows[current_index - 1 if current_index != 0 else len(scratch_windows) - 1]

    command = "[con_id=%d] scratchpad show" % next_win.id

    if is_fullscreen and focused.type != 'workspace':
        command += ", fullscreen toggle"

    i3.command(command)
    save_to_reg( "%s --scratchpad-next" % I3_SMART_FOCUS )

# Focus the first window with x instance
def focus_instance(instance):
    wins = tree.find_instanced(instance)

    if wins:
        if wins[0].parent.scratchpad_state != "none":
            command = "[instance=%s] scratchpad show" % instance
        else:
            command = "[instance=%s] focus" % instance

        if is_fullscreen and focused.type != 'workspace':
            command += ", fullscreen toggle"

        i3.command(command)
        save_to_reg("%s --instance %s" % (I3_SMART_FOCUS, instance))

    else:
        print("Couldn't find any window instanced as %s" % instance)
        exit(1)


def focus_marked(mark):
    marked_windows = tree.find_marked(mark)

    if not marked_windows:
        print("No windows marked as %s" % mark)
        exit(1)

    if marked_windows[0].parent.scratchpad_state != "none":
        command = "[con_mark=%s] scratchpad show" % mark
    else:
        command = "[con_mark=%s] focus" % mark

    if is_fullscreen and focused.type != 'workspace':
        command += ", fullscreen toggle"

    i3.command(command)
    save_to_reg("%s --mark %s" % (I3_SMART_FOCUS, mark))

def focus_fullscreen(forward=True):
    workspace = focused.workspace()
    windows = sorted([win.id for win in workspace.leaves()])
    win_num = len(windows)

    if focused.id in windows:
        win_index = windows.index(focused.id)

        if forward:
            next_win = windows[win_index + 1 if win_index != win_num - 1 else 0]
        else:
            next_win = windows[win_index - 1 if win_index != 0 else win_num - 1]

        command = "[con_id=%d] focus, fullscreen toggle" % next_win
        i3.command(command)
    else:
        print("Unexpected error")


def focus_class():
    pass

def focus_floating():
    i3.command('focus mode_toggle')

def focus_parent():
    i3.command('focus parent')

def focus_child():
    i3.command('focus child')

def focus_left():
    win_id = focused.window
    if is_fterm:
        subprocess.run(['xdotool', 'key', '-window', str(win_id), TABBED_FOCUS_PREV]) 
    elif is_fullscreen:
        focus_fullscreen( forward=False )
    elif is_floating:
        i3.command('focus left')
    else:
        i3.command('focus left')

def focus_right():
    win_id = focused.window
    if is_fterm:
        subprocess.run(['xdotool', 'key', '-window', str(win_id), TABBED_FOCUS_NEXT]) 
    elif is_fullscreen:
        focus_fullscreen()
    elif is_floating:
        i3.command('focus right')
    else:
        i3.command('focus right')

def focus_down():
    if is_fullscreen:
        focus_fullscreen(forward=False)
    elif is_floating:
        i3.command('focus right')
    else:
        i3.command('focus down')

def focus_up():
    if is_fullscreen:
        focus_fullscreen()
    elif is_floating:
        i3.command('focus left')
    else:
        i3.command('focus up')



if __name__ == '__main__':
    # No need for the argparse library here
    if len(sys.argv) < 2:
        print("Not enough arguments")
        print(usage)
        exit()
    elif len(sys.argv) == 2:
        if sys.argv[1][0:2] == "--":
            flag = sys.argv[1][2:]
            target = ''

            if flag not in flags:
                print("'%s' is not a valid flag" % flag )
                print(usage)
                exit(1)
            elif flag == 'help':
                print(usage)
                exit(0)
            elif flag == 'repeat-last':
                pass
            elif flag[-4:] != 'next' and flag[-4:] != 'prev':
                print("Not enough arguments")
                print(usage)
                exit(1)
        else:
            flag = ''
            target = sys.argv[1]

            if target not in targets:
                print("'%s' is not a valid target" % target)
                print(usage)
                exit(1)
    elif len(sys.argv) == 3:
        if sys.argv[1][0:2] == "--":
            flag = sys.argv[1][2:]
            target = sys.argv[2]

            if flag not in flags:
                print( "'%s' is not a valid flag" % flag)
                print( usage )
                exit()
        else:
            print("flags must have '--' as prefix")
            print(usage)
            exit()
    else:
        print("To many arguments")
        print(usage)
        exit(1)

    i3 = i3ipc.Connection()
    tree = i3.get_tree()
    focused = tree.find_focused()

    is_floating = focused.floating == "auto_on" or focused.floating == "user_on"
    # If the windows if floating and using tabbed
    is_fterm = focused.window_class == "tabbed" and is_floating
    is_fullscreen = focused.fullscreen_mode

    if flag:
        if flag == "repeat-last":
            repeat_last()
        elif flag == "fullscreen-next":
            focus_fullscreen()
        elif flag == 'scratchpad-next':
            scratchpad_next()
        elif flag == 'mark':
            focus_marked( target )
        elif flag == 'instance':
            focus_instance( target )
        elif flag == 'class':
            focus_class( target )
    else:
        if target == 'float':
            focus_floating()
        elif target == 'parent':
            focus_parent()
        elif target == 'child':
            focus_child()
        elif target == 'left':
            focus_left()
        elif target == 'right':
            focus_right()
        elif target == 'down':
            focus_down()
        elif target == 'up':
            focus_up()


