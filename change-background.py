#!/usr/bin/env python3
import os.path
import subprocess
import logging

bg_reg_file_path = "/tmp/current-wallpaper"

current_bg_index = -1

bg_dir = "/home/vabenil/wallpapers"

if not os.path.isdir( bg_dir ):
    print( "Wallpaper directory does not exist" )
    exit( 1 )

backgrounds = [
    "2_the_long_dark.jpg",
    "wallpaperPRo.jpg",
    "scrapping_metal.jpg",
    "wallpaper_sky_dreams.jpg",
    "gameboy_anaglyph_3d_102604_1366x768.jpg",
    "tree_horizon_minimalism_128903_1366x768.jpg",
    "tree_light_dark_82372_1366x768.jpg",
    "watching_from_below.jpg",
    "landscape_art_moon_127187_1366x768.jpg",
    "wallpaperOPEN.jpeg"
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


