#!/bin/sh

echo '{ "version": 1 }'

echo '['

echo '[]'

# This is only works with this specific font at this specific size.
# font pango: Hermit Regular 11px | Actual font widt = 7px
xscreen_size=$(xdpyinfo | sed -n 's/dimensions:\s\+\(\<[0-9]\+\)x.*/\1/p')
nchars=$(($xscreen_size / 7))

while :;
do
    echo ',['
    for i in $(seq 1 $nchars);
    do
        echo "
{
    \"name\":\"name$i\",
    \"full_text\": \"-\",
    \"separator\": false,
    \"separator_block_width\": 0
}$(if [ $i -ne $nchars ]; then echo ','; fi)"
           
    done
    echo ']'
    sleep 1
done
