from os import close
from threading import Thread, Lock
from queue import Queue
import os
import fcntl



class FileNotification:
    def __init__(self, filename):
        self.q = Queue()
        self.filename = filename
        self.fd = None
        self.lock = Lock()

        self.open()
        
    def open(self):
        self.fd = open(self.filename, "a")
        fd = self.fd.fileno()
        flag = fcntl.fcntl(fd, fcntl.F_GETFD)
        fcntl.fcntl(fd, fcntl.F_SETFL, flag | os.O_NONBLOCK)


    def close(self):
        try:
            close(self.fd)
        except:
            pass

    def start(self):
        Thread(None, self.read).start()

    def read(self):
        while True:
            d = self.q.get()
            
            # Log to file
            try:
                self.fd.write(d)
                print("Writen:",d)
                self.fd.flush()
            except:
                self.close()
                self.open()


    def send(self,d):
        self.lock.acquire()
        if not self.q.empty():
            self.q.get()
        self.q.put(d)
        self.lock.release()


