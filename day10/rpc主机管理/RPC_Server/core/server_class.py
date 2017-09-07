# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import pika,configparser

class RPC_Server(object):
    '''
    rpc服务端，用于分散主机
    '''
    def __init__(self):
        #获取配置信息
        self.Get_Conf()



    def Get_Conf(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(path,'conf','config.ini'))
        self.Host = config['RabbitMQ']['host']
        self.Port = config['RabbitMQ']['port']
        self.Credentials = pika.PlainCredentials(config['RabbitMQ']['user'], config['RabbitMQ']['pwd'])


    def Handler(self):
        self.Conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.Host,
                port=self.Port,
                credentials=self.Credentials
            )
        )
        self.Channel = self.Conn.channel()
        self.Channel.queue_declare(queue='rpc')