from threading import Thread
from queue import Queue


class StdoutNotification:
    def __init__(self):
        self.q = Queue()

    def start(self):
        Thread(None, self.read).start()

    def read(self):
        while True:
            d = self.q.get()
            print(d.strip())

    def send(self,d):
        self.q.put(d)


