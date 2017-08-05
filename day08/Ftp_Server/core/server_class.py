# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import socketserver

class Ftp_Server(socketserver.BaseRequestHandler):

    def handle(self):
        pass





def create_server():
    HOST, PORT = "localhost", 6512
    server = socketserver.ThreadingTCPServer((HOST, PORT), Ftp_Server)  # 多线程
    server.serve_forever()

if __name__ == '__main__':
    create_server()