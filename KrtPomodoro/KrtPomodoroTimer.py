#!/usr/bin/env python3

from threading import Timer
from Notifiy import Notifications
from socket import socket, AF_INET, SOCK_DGRAM

from UdpNotification import UDPNotification
from StdoutNotification import StdoutNotification
from FileNotification import FileNotification


class KrtPomodoroTimer:
    def __init__(self, config) -> None:
        self.config = config
        self.status = "stopped"
        self.pre_stopped = config.get('Pomodoro', 'before_if_paused_string', "")
        self.pre_break   = config.get('Pomodoro', 'before_break_string', "")
        self.pre_pomodoro   = config.get('Pomodoro', 'before_pomodoro_string', "")
        self.timer_pomodoro = config.get_int('Pomodoro', 'pomodoro_timer')
        self.timer_rest_1 = config.get_int('Pomodoro', 'short_break_timer')
        self.timer_rest_2 = config.get_int('Pomodoro', 'long_break_timer')
        self.pomodoros_per_long_break = config.get_int('Pomodoro', 'pomodoros_before_long_break')
        self.color = self.pre_stopped
        self.in_pomodoro = True
        self.pomodoros = 0
        self.timer = self.timer_pomodoro

        self.dumps_q = [ ]

        self.dumps = config.get_boolean('Pomodoro', 'dumps_timer')

        if self.dumps:
            self.config_dumps_q()

        self.tick()


    def config_dumps_q(self):
        dump_stdout = self.config.get_boolean('Pomodoro', 'dumps_stdout')
        if dump_stdout:
            n = StdoutNotification()
            n.start()
            self.dumps_q.append(n)


        dump_udp_port = self.config.get_int('Pomodoro', 'dumps_udp_port')
        if dump_udp_port >1:
            n = UDPNotification(dump_udp_port)
            n.start()
            self.dumps_q.append(n)


        dump_filename = self.config.get('Pomodoro', 'dumps_file')
        if dump_filename is not None:
            n = FileNotification(dump_filename)
            n.start()
            self.dumps_q.append(n)

        self.dump()


    def tick(self):
        Timer(1, self.tick).start()
        self.eval_pomodoro()
        self.dump()


    def eval_pomodoro(self):
        if self.status == "stopped":
            pass

        elif self.status == "reset":
            tr = self.timer_rest_2 if self.pomodoros % self.pomodoros_per_long_break == 0 else self.timer_rest_1
            self.timer = self.timer_pomodoro if self.in_pomodoro else tr
            self.stop()

        elif self.status == "started":
            self.timer = self.timer - 1

            if self.timer < 0:
                if self.in_pomodoro:
                    self.pomodoros = self.pomodoros + 1
                    self.timer = self.timer_rest_2 if self.pomodoros % self.pomodoros_per_long_break == 0 else self.timer_rest_1
                    Notifications().alert("TIME TO REST!!!!")
                    self.color = self.pre_break
                else:
                    self.timer = self.timer_pomodoro
                    Notifications().message("Click to estart pomodoro and focus on your task")
                    self.stop()
                self.in_pomodoro = not self.in_pomodoro


    def start(self):
        if self.status == "stopped":
            self.status = "started"
            self.color = self.pre_pomodoro if self.in_pomodoro else self.pre_break

    def toggle(self):
        if self.status == "stopped":
            self.start()
        else:
            self.stop()

    def get_timer(self):
        d = "{:02d}:{:02d}".format(int(self.timer/60),self.timer%60)
        return f"{self.color} {d}\n"

    def get_clean_timer(self):
        d = "{:02d}:{:02d}".format(int(self.timer/60),self.timer%60)
        return f"{d}"
        


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

    def dump(self):
        for n in self.dumps_q:
            n.send(self.get_timer())

