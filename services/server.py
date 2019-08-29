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
        # 备份次数
        self.times = 0
        self.users = []
        self.user_index = 0
        self.recv_size = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('192.168.31.203', 52578))
        self.sock.listen(20)
        # self.askTh = Thread(target=self.askAlive)
        # self.askTh.setDaemon(True)
        # self.askTh.start()

        while True:
            client, sockname = self.sock.accept()
            print("{}, {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), sockname))
            th = Thread(target=self.recv, args=(client, ))
            th.setDaemon(True)
            th.start()

    def recv(self, client):
        user = None
        while True:
            data = self.recvall(client)
            send_data = data
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
                    # 将登录的用户添加到用户列表中
                    self.users.append({'user': user, 'client': client})
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
                send_data = proto.makeProto('uploadfile', data['md5'], data['filemd5'], int(data['no']), '')
                client.sendall(send_data)
            if type == 'uploadsubfile':
                with GetSession() as session:
                    subfile = Subfile(id=data['md5'], file_md5_id=data['filemd5'], num=int(data['no']))
                    session.add(subfile)
                    session.commit()
                if self.user_index == len(self.users):
                    self.user_index = 0
                # send_user 注意与上面的 user 相区别
                send_user = self.users[self.user_index]
                try:
                    send_user['client'].sendall(send_data)
                except Exception as e:
                    self.users.remove(send_user)
                    continue
                else:
                    self.times += 1
                with GetSession() as session:
                    subfile_path = SubfilePath()
                self.user_index += 1

    def recvall(self, client):
        # 一次接收 SIZE 个字节，如果不够则继续接收
        data = client.recv(SIZE)
        while True:
            if len(data) != SIZE:
                try:
                    data = data + client.recv(SIZE - len(data))
                except Exception as e:
                    client.close()
            else:
                return data

    def askAlive(self):
        while True:
            for user in self.users:
                try:
                    user['client'].send(b'ok')
                except Exception as e:
                    user['client'].close()
                    self.users.remove(user)
            time.sleep(10)
            print(self.users)

    def test(self):
        pass


if __name__ == '__main__':
    server = Server()