#!/usr/bin/env python3


from subprocess import Popen
import time

class Notifications:
    def __init__(self):
        pass

    def alert(self, text):
        cmd = f"notify-send -u critical \"{text}\""
        Popen(cmd, shell=True)
        self.sound()

    def message(self, text):
        cmd = f"notify-send \"{text}\""
        Popen(cmd, shell=True)
        self.sound()

    def sound(self):
        cmd = f"paplay sounds/bell.ogg"
        Popen(cmd, shell=True)


if __name__ == "__main__":
    Notifications().alert("Esto es una alerta gorda")
    time.sleep(2)
    Notifications().message("Esto es una alerta chica")
