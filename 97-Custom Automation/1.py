import psutil as ps
import os

os.system('notify-send -u critical "test"')


def read_cpu_temp():
    return ps.sensors_temperatures()["k10temp"][0].current


if read_cpu_temp() >= 93:
    os.system('notify-send -u critical "CPU temp critical"')
    os.system("alacritty -e systemctl poweroff")