# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os,hashlib

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

    def Dir_List(self):
        list_path = self.cmd_data['path']
        list_res = os.listdir(list_path)
        print('type:',type(list_res),'|',list_res)
        self.request.send(str(len(pickle.dumps(list_res))).encode())
        client_answer = self.request.recv(1024)
        self.request.send(pickle.dumps(list_res))

    def Chk_File(self):
        chk_path = self.cmd_data['path']
        if os.path.isfile(chk_path):
            data = {
                'action':'Chk_File',
                'res':True
            }
        else:
            data = {
                'action': 'Chk_File',
                'res': False
            }
        self.request.send(pickle.dumps(data))


    def Get_HomePath(self):
        username = self.cmd_data['username']
        home_path = os.path.join(path,'home',username)
        try:
            os.path.exists(home_path)
            data = {
                'home_path':True,
                'sep':os.sep,
                'path':home_path
            }
        except FileNotFoundError as e:
            data = {
                'home_path': False,
                'sep': os.sep,
                'path': None
            }
        finally:
            print(data)
            self.request.send(pickle.dumps(data))


    def UpLoad_File(self):
        file_name = self.cmd_data['file_name']
        file_size = self.cmd_data['file_size']
        save_path = self.cmd_data['save_path']
        full_save_path = os.path.join(path,save_path,file_name)
        if os.path.isfile(full_save_path):
            data = {
                'continue':True,
                'recv_size':os.path.getsize(full_save_path),
            }
            need_file_size = file_size - os.path.getsize(full_save_path)
            file = open(full_save_path,'ab')
        else:
            data = {
                'continue': False,
                'recv_size': 0,
            }
            need_file_size = file_size
            file = open(full_save_path,'wb')
        self.request.send(pickle.dumps(data))#发送一个消息防止粘包
        recv_data_size = 0
        while recv_data_size < need_file_size:
            if need_file_size - recv_data_size <1024:
                size = need_file_size - recv_data_size
            else:
                size = 1024
            file_data = self.request.recv(1024)
            recv_data_size += len(file_data)
            md5 = hashlib.md5()
            md5.update(file_data)
            file.write(file_data)
        else:
            data = {"md5":md5.hexdigest()}
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
    # a =os.path.basename(path)
    # print(a)
