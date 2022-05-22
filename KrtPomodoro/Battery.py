#!/usr/bin/env python3

# BATTERY_STATUS = "/sys/class/power_supply/BAT0/status"
# BATTERY_CAPACITY = "/sys/class/power_supply/BAT0/capacity"
# NOTIFICATION_THRESHOLD = 20

from threading import Timer
import time
from Notifiy import Notifications

class BatteryChecker:
    def __init__(self, config):
        self.config = config
        self.status = ""
        self.capacity = 0
        self.notified = False

        self.battery_status_file = self.config.get('Battery', 'battery_status_file')
        self.battery_capacity_file = self.config.get('Battery', 'battery_capacity_file')
        self.battery_low_threshold = self.config.get_int('Battery', 'battery_low_threshold')

        self.read_battery()

    def read_battery(self):
        with open(self.battery_status_file, "r") as f:
            self.status = f.readline().strip()

        with open(self.battery_capacity_file, "r") as f:
            self.capacity = int(f.readline().strip())

        if self.status == "Discharging" and self.capacity <= self.battery_low_threshold:
            Notifications().alert(f"Battery low: {self.capacity}%")
            self.notified = True
        else:
            self.notified = False

        Timer(30, self.read_battery).start()

    def get(self):
        return f"{self.capacity} {self.status}"

if __name__ == "__main__":
    BatteryChecker()
    time.sleep(200)
