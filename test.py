import socket
import time
from threading import Thread

from models.models import User


SIZE = 1455


class Server:
    def __init__(self):
        print("start")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('192.168.31.203', 52578))
        self.sock.listen(20)
        self.users = []
        while True:
            client, sockname = self.sock.accept()
            print(client, sockname)
            print("{}, {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), sockname))
            self.users.append((client, sockname))
            th = Thread(target=self.recv, args=(client, sockname))
            th.start()
            th.join()

    def recv(self, client, sockname):
        while True:
            data = client.recv(SIZE)
            print(data)


if __name__ == '__main__':
    server = Server()