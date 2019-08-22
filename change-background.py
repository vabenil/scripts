#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess


# File to save wallpapers
BG_REG_FILE_PATH = "/tmp/current-bg"

def save_bg( bg ):
    try:
        bg_reg_file = open( BG_REG_FILE_PATH, "w" )
        bg_reg_file.write( bg )

        bg_reg_file.close()
    except:
        print( "Couldn't write to file %s" % BG_REG_FILE_PATH )
    pass

def get_current_bg():
    bg = None
    try:
        bg_reg_file = open( BG_REG_FILE_PATH, "r" )
    except FileNotFoundError:
        pass
    except Exception as e:
        print( "Error while opening file %s" % BG_REG_FILE_PATH )
        exit( 1 )
    else:
        bg = bg_reg_file.read() 

        bg_reg_file.close()

    return bg

def set_bg( bg_path ):
    subprocess.run(['feh', '--bg-fill', '--no-fehbg', bg_path])




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Traverse wallpapers in directory")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--filename', type=str,
            help="Set file as background" )
    group.add_argument('dir', nargs='?',
            help="Wallpaper directory")

    args = parser.parse_args()

    if args.filename:
        if not os.path.isfile(args.filename):
            print("%s file doesn't exist" % args.filename)
            parser.print_help()
            exit( 1 )
        else:
            bg_path = args.filename

            if bg_path.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                save_bg( bg_path )
                set_bg( bg_path )
            else:
                print( "File must be an image" )
                parser.print_help()
                exit( 1 )
    else:
        bg_dir = args.dir

        if not os.path.isdir(bg_dir):
            print( "%s is not a directory" % bg_dir )
            parser.print_help()
            exit( 1 )


        backgrounds = sorted([
            os.path.join(bg_dir, f) for f in os.listdir(bg_dir) \
                    if os.path.isfile( os.path.join(bg_dir, f)) and f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))
        ])

        current_bg_path = get_current_bg()

        current_bg_index = backgrounds.index(current_bg_path) if current_bg_path in backgrounds else (len(backgrounds) - 1)
        
        next_bg = backgrounds[ (current_bg_index + 1) % len( backgrounds ) ]
        
        save_bg( next_bg )
        set_bg( next_bg )
