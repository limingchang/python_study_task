# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import socket
server = socket.socket()
server.bind(('localhost',25355))#绑定监听端口
server.listen()#监听
print('等待客户端上传文件')

while True:
    conn,address = server.accept()#等待数据
    #conn是客户端链接到服务端，服务端为其生成的一个实例
    print('收到客户端数据:',address)
    while True:
        data = conn.recv(1024)
        if not data:
            print('客户端断开...')
            break
        print('server|recv:',data.decode())
        data = '客户端回复'
        conn.send(data.encode('utf-8'))
server.close()