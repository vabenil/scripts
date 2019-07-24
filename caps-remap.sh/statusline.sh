#!/bin/sh

# send header to use JSON
echo ' { "version": 1 }'



# begin the endless array
echo '['

# We send a empy first arry of blocks to make the loop simpler:
echo '[]'

# Now send blocks wit information forever:
count=0
while :;
do 
    network_name=$(iwgetid -r)
    [ -z $network_name ] && network_name="Not Connected"
     
    if [ $(iwgetid | sed -ne 's/^\(.\{2\}\).*/\1/p') = "wl" ];
    then
        network_icon=""
    else
        wireless_conection=$(ethtool eno1 | tail -n1 | grep -e "yes" -o)
        if [ $wireless_conection = "yes" ]; then 
            network_icon="  " 
        else
            echo ${wireless_conection} > /home/vabenil/log.txt
            network_icon=""
        fi
    fi

    touchpad_state=$( [ $(touchpad_state) -eq 1 ] && echo "Disabled" || echo "Enabled" )

    volume=$(amixer -c 1 -M -D pulse get Master | grep -o -E [[:digit:]]+% | head -n1) 
    volume=${volume%?}

    amixer_state=`amixer get Master | egrep 'Playback.*?\[o' | egrep -o '\[o.+\]'`

    scroll=${HOME}/.config/i3/scripts/scroll.py
    
    title=`$scroll 70 $count`

    xscreen_size=$(xdpyinfo | sed -n 's/dimensions:\s\+\(\<[0-9]\+\)x.*/\1/p')

    if [ $volume -gt 0 ]; then
        if [ $volume -le 30 ]; then
            volume_icon=""
        else
            volume_icon=""
        fi
    else
        volume_icon=""
    fi

    echo ","
    jq --null-input --slurp --color-output -M \
        --arg title "$title" \
        --arg title_minwidth "$(for i in $(seq 1 100); do echo -n A; done)" \
        --arg touchpad_state " : $touchpad_state " \
        --arg network " $network_icon $network_name " \
        --arg volume " $volume_icon $volume%" \
        --arg date "   $(date '+%a,%d.%m.%Y') " \
        --arg time "   $(date '+%r') " \
        --arg BLUE1 "#378486" \
        --arg BLUE2 "#00FFFF" \
        --arg RED1 "#863937" \
        --arg BLACK "#000000" \
        --arg BACKGROUND "#212121" \
        --arg WHITE "#FFFFFF" \
        --arg LIGHT "#E8E8E8" \
        --arg GREY_BLUEISH "#333838" \
        --arg GREY1 "#5E5E5E" \
        '
            [
            {
                "name":"Title",
                "full_text":$title,
                "min_width":$title_minwidth,
                "align":"center",
                "background":$BACKGROUND,
                "color":$WHITE,
                "separator": false,
                "separator_block_width": 0
            },
        {
            "name":"Touchpad_State",
            "full_text":$touchpad_state,
            "background":$BLUE1,
            "color":$LIGHT,
            "separator": false,
            "separator_block_width": 0
        },
    {
        "name":"Network",
        "full_text":$network,
        "background":$GREY_BLUEISH,
        "separator": false,
        "separator_block_width": 0
    },
{
    "name":"Volume",
    "full_text":$volume,
    "min_width":"   100% ",
    "align":"center",
    "background":$BLUE1,
    "color":$LIGHT,
    "separator": false,
    "separator_block_width": 0
},
{
    "name":"date",
    "full_text":$date,
    "background":$GREY_BLUEISH,
    "separator": false,
    "separator_block_width": 0
},
{
    "name":"time",
    "full_text":$time,
    "background":$BLUE1,
    "color":$WHITE,
    "separator": false,
    "separator_block_width": 0
}
]
'
    count=$(( $count + 1 ))
    sleep 0.3
done

