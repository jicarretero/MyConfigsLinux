#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

#Set your native resolution IF it does not exist in xrandr
#More info in the script
#run $HOME/.config/qtile/scripts/set-screen-resolution-in-virtualbox.sh

#Find out your monitor name with xrandr or arandr (save and you get this line)
#xrandr --output VGA-1 --primary --mode 1360x768 --pos 0x0 --rotate normal
#xrandr --output DP2 --primary --mode 1920x1080 --rate 60.00 --output LVDS1 --off &
#xrandr --output LVDS1 --mode 1366x768 --output DP3 --mode 1920x1080 --right-of LVDS1
#xrandr --output HDMI2 --mode 1920x1080 --pos 1920x0 --rotate normal --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output VIRTUAL1 --off
#autorandr horizontal
# xrandr --output eDP1 --mode 1920x1080 --pos 1920x0 --rotate normal --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output VIRTUAL1 --off
~/.screenlayout/layout.sh

#change your keyboard if you need it
#setxkbmap -layout be

keybLayout=$(setxkbmap -v | awk -F "+" '/symbols/ {print $2}')

if [ $keybLayout = "be" ]; then
  cp $HOME/.config/qtile/config-azerty.py $HOME/.config/qtile/config.py
fi

#autostart ArcoLinux Welcome App
run dex $HOME/.config/autostart/arcolinux-welcome-app.desktop &

#Some ways to set your wallpaper besides variety or nitrogen
# feh --bg-fill /usr/share/backgrounds/arcolinux/arco-wallpaper.jpg &

#start the conky to learn the shortcuts
# (conky -c $HOME/.config/qtile/scripts/system-overview) &

killall -q conky ; sleep 0.3 ;  (LC_TIME=en_GB.UTF-8 conky -c ~/Personal/eleg-weather-conky/something.lua) &


#start sxhkd to replace Qtile native key-bindings
run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &

#starting utility applications at boot time
# run variety &
feh --bg-fill /home/jicg/Pictures/Wallpapers/karate_bow_dark_1.jpg &
# feh --bg-fill ./Pictures/Wallpapers/1_salamanca.jpg &
run nm-applet &
run pamac-tray &
run xfce4-power-manager &
# numlockx on &
blueberry-tray &
# /opt/tuxedo-control-center/tuxedo-control-center &
picom --config $HOME/.config/qtile/scripts/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
# /usr/lib/xfce4/notifyd/xfce4-notifyd &
(dunst) &

# Launch KRT - Pomodoro
/home/jicg/Personal/KrtPomodoro/server_start.sh &


#starting user applications at boot time
# run volumeicon &
#run discord &
#nitrogen --restore &
#run caffeine -a &
#run vivaldi-stable &
#run firefox &
#run thunar &
#run dropbox &
run megasync &
#run insync start &
#run spotify &
#run atom &
#run telegram-desktop &
