#!/usr/bin/python3.7
import argparse

"""
Simple text scroller
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple text scroller")

    required = parser.add_argument_group('required named arguments')

    required.add_argument('-m', '--maxlen', type=int, required=True, help="The amount of characters to show")
    required.add_argument('-i', '--index', type=int, required=True, help="The first character index")

    exclusive_group = required.add_mutually_exclusive_group(required=True)

    exclusive_group.add_argument('-t', '--text', type=str, help="The full text")
    exclusive_group.add_argument('--read-from-stdin', action='store_true', help="The full text")

    args = parser.parse_args()


    maxlen = args.maxlen
    indx = args.index

    if args.read_from_stdin:
        from sys import stdin

        text = ''.join( [ line.rstrip() for line in stdin ] )
    else:
        text = args.text

    text_len = len( text )


    if text_len <= maxlen:
        padding = round( 0.5 * ( maxlen - text_len ) ) * ' '
        print( "%s%s%s" % (padding, text, padding) )
        exit()

    spacing = ' ' * maxlen

    full_text = text + spacing
    full_len = text_len + maxlen

    indx = indx if indx < full_len else ( ( indx % (full_len)) )
    last_indx = indx + maxlen 

    full_text += text[ 0 : indx ]

    screen_buffer = full_text[ indx : last_indx]

    print( screen_buffer )
