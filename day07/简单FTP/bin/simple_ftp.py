# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import subprocess
import threading
from multiprocessing import Process
from core import client_class,server_class




def run_server():
    server = server_class.Server_Class()


def run_client():
    client = client_class.Client_Class()

if __name__ =='__main__':
    # threads =[]#创建子线程数组
    # server_thread = threading.Thread(target=run_server)#创建server子线程
    # server_thread.setDaemon(True)#设置线程为后台线程
    # threads.append(server_thread)
    # # client_thread = threading.Thread(target=run_client)
    # # threads.append(client_thread)
    # threads[0].start()
    server_process = Process(target=run_server)#创建进程
    server_process.daemon = True
    server_process.start()
    client = client_class.Client_Class()
