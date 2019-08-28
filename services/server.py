import socket
import time
from threading import Thread
import json

from models.models import *
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
        user = None
        while True:
            data = self.recvall(client)
            print(data)
            print(len(data))
            data = proto.unmakeProto(data)
            type = data['type']
            if type == 'login':
                info = data['content']
                info = info.strip()
                info = json.loads(info)
                with GetSession() as session:
                    user = session.query(User).filter_by(username=info['username'], password=info['password']).one()
                    if not user:
                        pass
            if type == 'uploadfile':
                # 将文件信息存入数据库，返回确认信息
                info = json.loads(data['content'].strip())
                with GetSession() as session:
                    file_md5 = FileMd5(id=data['filemd5'], nums=int(data['no']))
                    session.add(file_md5)
                    session.commit()
                    file = File(filename=info['filename'], size=int(info['filesize']), file_md5_id=file_md5.id, user_id=user.id)
                    session.add(file)
                    session.commit()
                data = proto.makeProto('uploadfile', data['md5'], data['filemd5'], int(data['no']), '')
                client.sendall(data)
            if type == 'uploadsubfile':
                with GetSession() as session:
                    pass
                f = open('../subfiles/{}.txt'.format(data['md5']), 'w')
                f.write(data['content'])
                f.close()

    def recvall(self, client):
        # 一次接收 SIZE 个字节，如果不够则继续接收
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