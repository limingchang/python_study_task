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
                print('结束会话.')
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
        md5 = hashlib.md5()
        while recv_data_size < need_file_size:
            if need_file_size - recv_data_size <1024:
                size = need_file_size - recv_data_size
            else:
                size = 1024
            file_data = self.request.recv(1024)
            recv_data_size += len(file_data)

            md5.update(file_data)
            file.write(file_data)
        else:
            data = {"md5":md5.hexdigest()}
            self.request.send(pickle.dumps(data))


    def DownLoad_File(self):
        filename = self.cmd_data['path']
        recv_file_size = self.cmd_data['recv_size']
        #回复文件大小
        data = {
            'filesize':os.path.getsize(filename) - recv_file_size
        }
        self.request.send(pickle.dumps(data))
        f = open(filename,'rb')
        f.seek(recv_file_size)#跳转续传位置
        md5 = hashlib.md5()
        for line in f:
            self.request.send(line)
            md5.update(line)
        chk_md5 = pickle.loads(self.request.recv(1024)) #接收MD5校检
        if chk_md5['chk_md5'] == md5.hexdigest():
            data={'chk_md5':True}
        else:
            data={'chk_md5':False}
        self.request.send(pickle.dumps(data))#回复客户端校检结果


    def Chk_Space(self):
        space = self.cmd_data['space']#mb
        up_size = self.cmd_data['up_size']
        username = self.cmd_data['username']
        home_path = os.path.join(path,'home',username)
        uped_size = self.GetPathSize(home_path) + up_size#字节,上传后的大小
        print('上传后大小')
        user_size = space*1024*1024
        print('用户配额：',user_size)
        if uped_size > user_size:
            data ={'chk_space':False}
        else:
            data = {'chk_space': True}

        self.request.send(pickle.dumps(data))


    def GetPathSize(self,strPath):
        if not os.path.exists(strPath):
            return 0
        if os.path.isfile(strPath):
            return os.path.getsize(strPath)
        nTotalSize = 0
        for strRoot, lsDir, lsFiles in os.walk(strPath):
            for strFile in lsFiles:
                nTotalSize = nTotalSize + os.path.getsize(os.path.join(strRoot, strFile))

        return nTotalSize

    def Create_Dir(self):
        will_create_dir = self.cmd_data['will_create_dir']
        dir_name = self.cmd_data['dir_name']
        full_path = os.path.join(path,will_create_dir,dir_name)
        print('创建：',full_path)
        os.mkdir(full_path)
        data = {'res':True}
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
        'space': 10  #mb
    }
    userinfo_file = '%s.dat' % data['username']
    userinfo_file = os.path.join(path, 'db', userinfo_file)
    with open(userinfo_file, 'wb') as f:
        pickle.dump(data, f)
        #os.mkdir(os.path.join(path,'home',data['username']))



if __name__ == '__main__':
    create_server()
    #create_user()
    # a =os.path.basename(path)
    # print(a)
