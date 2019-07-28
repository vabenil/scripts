#!/usr/bin/env python3
import os
import sys
import subprocess
import logging


"""
Switch wallpapers from directory

This scripts requires feh to work
"""

USAGE = "change-background.py [wallpaper directory]"

if len(sys.argv) == 1:
    # File for saving the current wallpaper
    bg_reg_file_path = "/tmp/current-wallpaper"
    # Wallpaper file
    bg_dir = "/home/vabenil/Pictures/wallpapers"
elif len(sys.argv) == 2:
    if type(sys.argv[1]) is str:
        if os.path.isdir( sys.argv[1] ):
            # File for saving the current wallpaper
            bg_reg_file_path = sys.argv[1]
            # Wallpaper file
            bg_dir = sys.argv[1]
        else:
            print( "%s is not a valid directory" % sys.argv[1] )
            exit( 1 )
    else:
        print( "First argument most be a path" )
        print( USAGE )
        exit( 1 )

else:
    print( "To many arguments" )
    print( USAGE )
    exit( 1 )


current_bg_index = -1

backgrounds = [
    f for f in os.listdir(bg_dir) if os.path.isfile(os.path.join(bg_dir, f))
]

# Get current background image
try:
    bg_reg_file = open( bg_reg_file_path, "r" )
except FileNotFoundError:
    pass
except Exception as e:
    logging.error(e)
    print( "Error while opening file %s" % bg_reg_file_path )
    exit( 1 )
else:
    bg = bg_reg_file.read() 

    if bg in backgrounds:
        current_bg_index = backgrounds.index( bg )

    bg_reg_file.close()

next_bg = backgrounds[ current_bg_index + 1 if current_bg_index != len( backgrounds ) - 1 else 0 ]

bg_path = "%s/%s" % (bg_dir, next_bg) 

if not os.path.exists( bg_path ):
    exists( 1 )

# Set Background 
subprocess.run(['feh', '--bg-fill', '--no-fehbg', bg_path])

# Save current background image
try:
    bg_reg_file = open( bg_reg_file_path, "w" )
    bg_reg_file.write( next_bg )

    bg_reg_file.close()
except:
    print( "Couldn't write to file %s" % bg_reg_file_path )


