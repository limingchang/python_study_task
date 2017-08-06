# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import socketserver,pickle

class Ftp_Server(socketserver.BaseRequestHandler):

    def handle(self):
        print(self.client_address,'正在连接')
        while True:
            try:
                self.cmd_data = pickle.loads(self.request.recv(1024))
                if hasattr(self,self.cmd_data['action']):
                    func = getattr(self,self.cmd_data['action'])
                    func()
                else:
                    print('命令错误...')
            except ConnectionResetError as e:
                print('[%s]结束会话.'%self.client_address)
                break
            except EOFError as e:
                print('data is none!')
                break


    def Chk_Platform(self):
        self.Platform = os.name
        self.request.send(self.Platform.encode())

    def Auth(self):
        username = self.cmd_data['username']
        password = self.cmd_data['password']
        print('Auth:',username,password)
        userinfo_file = '%s.dat'%username
        userinfo_file = os.path.join(path, 'db', userinfo_file)
        try:
            with open(userinfo_file,'rb') as f:
                info = pickle.load(f)
            if username == info['username'] and password == info['password']:
                data = {
                    'auth':True,
                    'info':info
                }
            else:
                data = {
                    'auth': False,
                    'info':'密码错误！'
                }
        except FileNotFoundError as e:
            data = {
                'auth':False,
                'info':'用户不存在！'
            }
        finally:
            self.request.send(pickle.dumps(data))






    def finish(self):  # 请求结束后的后事
        print('结束会话.')



def create_server():
    HOST, PORT = "0.0.0.0", 6512
    server = socketserver.ThreadingTCPServer((HOST, PORT), Ftp_Server)  # 多线程
    server.serve_forever()


def create_user():
    import hashlib
    password = '123'
    password = hashlib.sha1(password.encode("utf8")).hexdigest()
    data = {
        'username': 'lmc',
        'password': password,
        'space': 838860800  # 100mb
    }
    userinfo_file = '%s.dat' % data['username']
    userinfo_file = os.path.join(path, 'db', userinfo_file)
    with open(userinfo_file, 'wb') as f:
        pickle.dump(data, f)



if __name__ == '__main__':
    create_server()
