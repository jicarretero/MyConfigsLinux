#!/usr/bin/env python3

from configparser import ConfigParser

class KrtConfiguration:
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read('config.ini')

    def get(self, section, variable, default=None):
        try:
            return self.parser[section][variable]
        except KeyError:
            return default

    def get_int(self, section, variable):
        sn = self.get(section, variable)
        
        return int(sn) if sn is not None else -1

    def get_boolean(self, section, variable):
        sn = self.get(section, variable)
        
        return bool(sn) if sn is not None else False


if __name__ == "__main__":
    c = KrtConfiguration()
    print(c.get('Pomodoro', 'pomodoro_time'))
    print(c.get_int('Pomodoro', 'pomodoro_time'))
