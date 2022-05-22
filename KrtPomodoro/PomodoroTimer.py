#!/usr/bin/env python3

from threading import Timer
from Notifiy import Notifications
from socket import socket, AF_INET, SOCK_DGRAM

class PomodoroTimer:
    def __init__(self, config) -> None:
        self.config = config
        self.status = "stopped"
        self.pre_stopped = config.get('Pomodoro', 'before_if_paused_string')
        self.pre_break   = config.get('Pomodoro', 'before_break_string')
        self.pre_pomodoro   = config.get('Pomodoro', 'before_pomodoro_string')
        self.timer_pomodoro = config.get_int('Pomodoro', 'pomodoro_timer')
        self.timer_rest_1 = config.get_int('Pomodoro', 'short_break_timer')
        self.timer_rest_2 = config.get_int('Pomodoro', 'long_break_timer')
        self.pomodoros_per_long_break = config.get_int('Pomodoro', 'pomodoros_before_long_break')
        self.dumps = config.get_boolean('Pomodoro', 'dumps_timer')
        self.dump_stdout = config.get_boolean('Pomodoro', 'dumps_stdout')
        self.dump_filename = config.get('Pomodoro', 'dumps_file')
        self.dump_udp_port = config.get_int('Pomodoro', 'dumps_udp_port')
        self.color = self.pre_stopped
        self.in_pomodoro = True
        self.pomodoros = 0
        self.timer = self.timer_pomodoro

        if self.dump_filename is not None:
            self.dump_fd = open(self.dump_filename, "a")
        else:
            self.dump_fd = 0

        if self.dump_udp_port is not None:
            self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        else:
            self.udp_socket = -1


        self.dump_tick()


    def tick(self):
        self.timer = self.timer - 1
        self.dump()

        if self.timer <= 0:
            if self.in_pomodoro:
                self.pomodoros = self.pomodoros + 1
                self.in_pomodoro = False
                self.timer = self.timer_rest_2 if self.pomodoros % self.pomodoros_per_long_break == 0 else self.timer_rest_1
                Notifications().alert("TIME TO REST!!!")
                self.color = self.pre_break
            else:
                self.in_pomodoro = True
                self.timer = self.timer_pomodoro
                Notifications().message("Click to start pomodoro and focus your task")
                self.stop()

        if self.status == "started":
            Timer(1, self.tick).start()
        elif self.status == "reset":
            self.status = "stopped"
            self.timer = self.timer_pomodoro if self.in_pomodoro else self.timer_rest_1


    def start(self):
        if self.status == "stopped":
            self.status = "started"
            self.color = self.pre_pomodoro if self.in_pomodoro else self.pre_break
            Timer(1, self.tick).start()

    def toggle(self):
        if self.status == "stopped":
            self.start()
        else:
            self.stop()

    def get_timer(self):
        d = "{:02d}:{:02d}".format(int(self.timer/60),self.timer%60)
        return f"{self.color} {d}\n"


    def stop(self):
        self.status = "stopped"
        self.color = self.pre_stopped

    def reset(self):
        self.status = "reset"

    def what(self):
        if self.in_pomodoro:
            return "POMODORO"
        else:
            return "BREAK"

    def dump_tick(self):
        if self.dumps:
            self.dump()
            Timer(1, self.dump_tick).start()


    def dump(self):
        if self.dumps: 
            timer = self.get_timer()

            # Log to file
            if self.dump_filename is not None:
                try:
                    self.dump_fd.write(timer)
                    self.dump_fd.flush()
                except:
                    pass

            # Log to UDP Port
            if self.dump_udp_port > 0: 
                self.udp_socket.sendto(bytes(timer, 'utf-8') ,("localhost", self.dump_udp_port))

            # Log to stdout
            if self.dump_stdout:
                print(timer.strip())

