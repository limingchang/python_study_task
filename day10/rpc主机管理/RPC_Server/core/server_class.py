# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import pika,configparser,pickle
import socket

class RPC_Server(object):
    '''
    rpc服务端，用于分散主机
    '''
    def __init__(self):
        #获取配置信息
        self.Get_Conf()
        #创建连接和信道,并接收客户端消息
        #self.Handler()



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
        self.Channel.basic_consume(
            self.On_Response,
            queue='rpc'
        )
        self.Channel.start_consuming()



    def On_Response(self,ch,method,props,body):
        '''
        处理接收到的消息的回调函数
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        '''
        cmd = pickle.loads(body)['cmd']
        host_list = pickle.loads(body)['host_list']
        myip = self.Get_Ip()
        #如果本机ip在ip列表中，执行命令并返回
        if myip in host_list:
            res = self.Run_Command(cmd)
            data = {
                'host':myip,
                'res':res
            }
            self.Channel.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=props.correlation_id
                ),
                body=pickle.dumps(data)
            )
            self.Channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print('recv cmd ,but it not give me!')


    def Run_Command(self,cmd):
        pass


    def Get_Host(self):
        '''
        获取本机IP
        :return:
        '''
        hostname = socket.gethostname()
        #ip = socket.gethostbyname(socket.gethostname())
        ipList = socket.gethostbyname_ex(socket.gethostname())
        print(ipList)
        return hostname



    def Get_Ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


if __name__ == '__main__':
    RPC_S = RPC_Server()
    print(RPC_S.Get_Host())
    #print(get_ip2())

