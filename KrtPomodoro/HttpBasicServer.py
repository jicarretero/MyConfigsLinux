#!/usr/bin/env python3

from flask import Flask 
from flask_restful import Api
from KrtPomodoroTimer import KrtPomodoroTimer as PomodoroTimer
from Battery import BatteryChecker
from KrtConfiguration import KrtConfiguration
import logging
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

app = Flask("KrtPomodoro_server")

config = KrtConfiguration()
timer = PomodoroTimer(config)
battery = BatteryChecker(config)

@app.route("/pomodoro/start", methods=["POST"])
def pomodoro_start():
    timer.start()
    return "", 204

@app.route("/pomodoro/stop", methods=["POST"])
def pomodoro_stop():
    timer.stop()
    return "", 204

@app.route("/pomodoro/reset", methods=["POST"])
def pomodoro_reset():
    timer.reset()
    return "", 204

@app.route("/pomodoro/toggle", methods=["POST"])
def pomodoro_toggle():
    timer.toggle()
    return "", 204

@app.route("/pomodoro/timer", methods=["GET"])
def pomodoro_get_timer():
    return timer.get_timer(), 200

@app.route("/pomodoro/dump", methods=["GET"])
def pomodoro_dump_timer():
    timer.dump()
    return "", 200

@app.route("/pomodoro", methods=["GET"])
def pomodoro_get_all():
    return str(timer.get_clean_timer().strip())  + " " + timer.status + " " + timer.what(), 200

@app.route("/battery", methods=["GET"])
def battery_get():
    return battery.get(), 200


class KrtPomodoroAPP:
    def __init__(self, config):
        self.config = config
        self.port = self.config.get_int('HttpServer', 'port')
        self.api = Api(app)
        app.run(port=self.port)

if __name__ == "__main__":
    server = KrtPomodoroAPP(config)
