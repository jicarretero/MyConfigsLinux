#!/bin/bash

pkill -9 polybar
pkill -9 socat
ps -ef | awk '/pavolume.sh/ {print $2}' | xargs kill

bar0=black
bar=${bar0}

sleep 0.3
for m in $(xrandr --query | awk '/ connected / {print $1}' | sort -r); do
  MONITOR=$m polybar --reload ${bar} -c ~/.config/polybar/krtconfig_i3 &
  bar=${bar0}-foo
done
