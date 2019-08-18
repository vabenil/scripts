#!/bin/sh

if [ -z "$1" ];
then
    exit 1
fi

while true;
do
    wait-next-second
    date "$1"
done
