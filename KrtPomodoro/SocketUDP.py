from socket import socket

class PomodoroUDPWriter:
    def __init__(self) -> None:
        self.udp_port = 3333
        self.s = socket.socket(socket.AF_INET,dump_stdout.SOCK_DGRAM)

    def write(self, data):
        self.s.sendto(msg, ("localhost", self.port))
