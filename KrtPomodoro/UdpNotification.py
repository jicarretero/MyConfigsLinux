from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from queue import Queue


class UDPNotification:
    def __init__(self, port):
        self.port = port
        self.q = Queue()
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)

    def start(self):
        Thread(None, self.read).start()

    def read(self):
        while True:
            d = self.q.get()
            self.udp_socket.sendto(bytes(d, 'utf-8') ,("localhost", self.port))

    def send(self,d):
        self.q.put(d)


