#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import random


# File to save wallpapers
BG_REG_FILE_PATH = "/tmp/current-bg"

def save_bg(bg):
    try:
        bg_reg_file = open(BG_REG_FILE_PATH, "w")
        bg_reg_file.write(bg)

        bg_reg_file.close()
    except:
        print("Couldn't write to file %s" % BG_REG_FILE_PATH)
    pass

def get_bg():
    bg = None
    try:
        bg_reg_file = open(BG_REG_FILE_PATH, "r")
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Error while opening file %s" % BG_REG_FILE_PATH)
        exit(1)
    else:
        bg = bg_reg_file.read() 

        bg_reg_file.close()

    return bg

def set_bg(bg_path):
    subprocess.run(['feh', '--bg-fill', '--no-fehbg', bg_path])

def random_bg():
    bgs = sorted([
        os.path.join(bg_dir, f) for f in os.listdir(bg_dir) \
                if os.path.isfile( os.path.join(bg_dir, f)) and f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ])
    bg_path = get_bg()

    bg_index = bgs.index(bg_path) if bg_path in bgs else -1

    if len(bgs) > 1 and bg_index != -1:
        rand_bg = random.choice(bgs)
        while rand_bg == bgs[bg_index]:
            rand_bg = random.choice(bgs)

        bg = rand_bg
    else:
        bg = bgs[0]

    save_bg(bg)
    set_bg(bg)


def next_bg():
    bgs = sorted([
        os.path.join(bg_dir, f) for f in os.listdir(bg_dir) \
                if os.path.isfile( os.path.join(bg_dir, f)) and f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ])

    bg_path = get_bg()

    bg_index = bgs.index(bg_path) if bg_path in bgs else (len(bgs) - 1)

    bg = bgs[ (bg_index + 1) % len(bgs) ]

    save_bg(bg)
    set_bg(bg)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Traverse wallpapers in directory")
    parser.add_argument('--random', action='store_true', help="Set file as background")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--filename', type=str)
    group.add_argument('dir', nargs='?', help="Wallpaper directory")

    args = parser.parse_args()

    if args.filename:
        if not os.path.isfile(args.filename):
            print("%s file doesn't exist" % args.filename)
            parser.print_help()
            exit(1)
        else:
            bg_path = args.filename

            if bg_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                save_bg(bg_path)
                set_bg(bg_path)
            else:
                print("File must be an image")
                parser.print_help()
                exit(1)
    else:
        bg_dir = args.dir

        if not os.path.isdir(bg_dir):
            print("%s is not a directory" % bg_dir)
            parser.print_help()
            exit(1)

        if args.random:
            random_bg()
        else:
            next_bg()

