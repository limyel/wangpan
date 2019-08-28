import socket
import time
from threading import Thread

from models.models import User
from utils import b64, md5, proto, supplement
from models.seeion import GetSession


SIZE = 1486


class Server:
    def __init__(self):
        print("start")
        self.recv_size = 0
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
            data = self.recvall(client)
            print(len(data))
            data = proto.unmakeProto(data)
            type = data['type']

            if type == 'uploadfile':
                data = proto.makeProto('uploadfile', data['md5'], data['filemd5'], -1, '')
                client.sendall(data)
                print('ok')
            if type == 'uploadsubfile':
                with GetSession() as session:
                    session.add
                f = open('../subfiles/{}.txt'.format(data['md5']), 'w')
                f.write(data['content'])
                f.close()

    def recvall(self, client):
        size = 0
        data = client.recv(SIZE)
        while True:
            if len(data) != SIZE:
                data = data + client.recv(SIZE - len(data))
            else:
                return data

    def test(self):
        pass


if __name__ == '__main__':
    server = Server()