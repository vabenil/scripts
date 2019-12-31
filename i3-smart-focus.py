#!/usr/bin/env python3

import i3ipc
import sys
import argparse
import os.path

REG_FILE_PATH = '/tmp/i3-smart-focus-command-register'

# REQUIRED
# path to this script
I3_SMART_FOCUS = os.path.abspath(__file__)

targets = ('left', 'right', 'down', 'up')

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

    # print(last_fcommand)
    sys.argv = last_fcommand
    exec(open(I3_SMART_FOCUS).read())


def scratchpad_next(save=False):
    scratch_windows = tree.scratchpad().leaves()

    if focused in scratch_windows:
        current_index = scratch_windows.index(focused)
    else:
        current_index = -1

    next_win = scratch_windows[current_index + 1 if current_index != 0 else len(scratch_windows) - 1]

    command = "[con_id=%d] scratchpad show" % next_win.id

    if is_fullscreen and focused.type != 'workspace':
        command += ", fullscreen toggle"

    i3.command(command)

    # Hide previously focuse window
    if focused.parent.scratchpad_state != "none":
        i3.command("[con_id=%d] scratchpad show" % focused.id)

    if save:
        save_to_reg("%s --scratchpad-next" % I3_SMART_FOCUS)

# Focus the first window with x instance
def focus_instance(instance, save=True):
    wins = tree.find_instanced(instance)

    if wins:
        if wins[0].parent.scratchpad_state != "none":
            command = "[instance=%s] scratchpad show" % instance
        else:
            command = "[instance=%s] focus" % instance

        if is_fullscreen and focused.type != 'workspace':
            command += ", fullscreen toggle"

        i3.command(command)
        if save:
            save_to_reg("%s --instance %s" % (I3_SMART_FOCUS, instance))

    else:
        print("Couldn't find any window instanced as %s" % instance)
        exit(1)


def focus_marked(mark, save=True):
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
    if save:
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

def focus_left():
    if is_fullscreen:
        focus_fullscreen( forward=False )
    elif is_floating:
        i3.command('focus left')
    else:
        i3.command('focus left')

def focus_right():
    if is_fullscreen:
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
    parser = argparse.ArgumentParser(prog="i3-smart-focus",
                                     description="Smartly focus windows in i3")
    parser.add_argument('--no-save', action='store_true',
                        help="Do not save save %(prog)s command")

    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument('-t', '--target', type=str,
                                 choices=targets,
                                 help="The TARGET to focus")
    exclusive_group.add_argument('--repeat-last', action='store_true',
                                 help="Repeat last %(prog)s command")
    exclusive_group.add_argument('--scratchpad-next', action='store_true',
                                 help="Focus next window in the scratchpad")
    exclusive_group.add_argument('--scratchpad-prev', action='store_true',
                                 help="Focus prev window in the scratchpad")
    exclusive_group.add_argument('--fullscreen-next', action='store_true',
                                 help="Focus next window without exiting\
                                 fullscreen mode")
    exclusive_group.add_argument('--fullscreen-prev', action='store_true',
                                 help="Focus prev window without exiting\
                                 fullscreen mode")
    exclusive_group.add_argument('-m', '--mark', type=str,
                                 help="Focus mark MARK")
    exclusive_group.add_argument('-i', '--instance', type=str,
                                 help="Focus instance INSTANCE")
    exclusive_group.add_argument('-c', '--class', type=str,
                                 help="Focus class CLASS")
    exclusive_group.add_argument('--read-from-stdin', action='store_true',
                                 help="The full text")

    args = parser.parse_args()


    i3 = i3ipc.Connection()
    tree = i3.get_tree()
    focused = tree.find_focused()

    is_floating = focused.floating == "auto_on" or focused.floating == "user_on"
    # If the windows if floating and using tabbed
    is_fterm = focused.window_class == "tabbed" and is_floating
    is_fullscreen = focused.fullscreen_mode

    if args.repeat_last:
        repeat_last()
        exit(0)

    if args.scratchpad_next:
        scratchpad_next(not args.no_save)
    elif args.target != None:
        if args.target == "left":
            focus_left()
        elif args.target == "right":
            focus_right()
        elif args.target == "up":
            focus_up()
        else:
            focus_down()
    elif args.instance != None:
        focus_instance(args.instance, not args.no_save)
    elif args.mark != None:
        focus_marked(args.mark, not args.no_save)


