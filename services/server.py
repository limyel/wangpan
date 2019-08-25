import socket
import time
from threading import Thread

from models.models import User


MAXSIZE =


class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('127.0.0.1', 2578))
        self.sock.listen(20)
        self.users = []
        while True:
            client, sockname = self.sock.accept()
            print("{}, {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), sockname))
            self.users.append((client, sockname))
            th = Thread(target=self.recv, args={client, sockname})
            th.start()
            th.join()

    def recv(self, client, sockname):
        while True:
            data = client.recv()