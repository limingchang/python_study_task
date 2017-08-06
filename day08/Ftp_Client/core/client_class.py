# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import socket,pickle

class Ftp_Client(object):
    def __init__(self):
        self.client = socket.socket()
        self.connection('localhost',6512)
        #self.handle()

    def connection(self,ip,port):
        '''
        连接服务端
        :param ip: 服务端ip
        :param port: 服务端端口
        :return:
        '''
        self.client.connect((ip,port))


    def handle(self):
        data={'action':'Chk_Platform'}
        self.client.send(pickle.dumps(data))
        self.Chk_Platform = self.client.recv(1024).decode()
        self.client.close()
        #print(self.Chk_Platform.decode())

    def Auth(self,username,password):
        data={
            'action':'Auth',
            'username':username,
            'password':password
        }
        self.client.send(pickle.dumps(data))
        auth_res = pickle.loads(self.client.recv(1024))
        return auth_res


    def Dir_List(self,list_path):
        data = {
            'action':'Dir_List',
            'path':list_path
        }
        self.client.send(pickle.dumps(data))
        total_data_size = self.client.recv(1024).decode()
        print('total:',total_data_size)
        total_data_size = int(total_data_size)
        self.client.send(b'ok')
        recv_data_size = 0
        recv_data = b''
        while recv_data_size < total_data_size:
            if total_data_size - recv_data_size <1024:
                size = total_data_size - recv_data_size
            else:
                size = 1024
            tmp_data = self.client.recv(size)
            recv_data += tmp_data
            recv_data_size += len(tmp_data)
        else:
            list_res = pickle.loads(recv_data)
        return list_res


    def Chk_File(self,chk_path):
        '''
        检查云端路径是文件还是目录
        :return: True文件，False目录
        '''
        data = {
            'action':'Chk_File',
            'path':chk_path
        }
        self.client.send(pickle.dumps(data))
        chk_res = pickle.loads(self.client.recv(1024))
        return chk_res['res']


    def Get_HomePath(self,username):
        '''
        获取云端个人目录
        :return:
        '''
        data = {
            'action':'Get_HomePath',
            'username':username
        }
        self.client.send(pickle.dumps(data))
        home_path = pickle.loads(self.client.recv(1024))
        return home_path['path']






if __name__ == '__main__':
    client = Ftp_Client()
