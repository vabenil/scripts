t=0

toggle() {
    t=$(((t + 1) % 2))
}


trap "toggle" USR1

while true; do
    if [ $t -eq 0 ]; then
        task minimal | sed -n 's/^\([0-9]\+\>\) tasks/\1/p'
    else
        ${HOME}/scripts/task_polybar.sh
    fi
    sleep 10 &
    wait
done
