import socket
import time
from threading import Thread

from models.models import User
from utils import b64, md5, proto, supplement


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
            print("{}, {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), sockname))
            self.users.append((client, sockname))
            th = Thread(target=self.recv, args=(client, sockname))
            th.setDaemon(True)
            th.start()

    def recv(self, client, sockname):
        while True:
            data = client.recv(SIZE)
            data = proto.unmakeProto(data)
            print(data)

            if not data['type']:
                client.close()
                return
            if data['type'] == 'uploadsubfile':
                f = open('../subfiles/{}.txt'.format(data['md5']), 'w')
                f.write(data['content'])
                f.close()

    def test(self):
        pass


if __name__ == '__main__':
    server = Server()