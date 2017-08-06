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



if __name__ == '__main__':
    client = Ftp_Client()
