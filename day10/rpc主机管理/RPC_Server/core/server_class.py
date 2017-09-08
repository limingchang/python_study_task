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
        self.Handler()



    def Get_Conf(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(path,'conf','config.ini'))
        self.Host = config['RabbitMQ']['host']
        self.Port = int(config['RabbitMQ']['port'])
        #获取本机IP函数有问题，只能写入配置文件
        self.MyHost=config['LOCAL']['host']
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
        self.Channel.exchange_declare(
            exchange='rpc',
            exchange_type='direct'
        )
        result = self.Channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        self.Channel.queue_bind(
            exchange='rpc',
            queue=queue_name,
            routing_key=self.MyHost
        )
        self.Channel.basic_consume(
            self.On_Response,
            queue=queue_name,
            no_ack=True
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
        #print('body:',pickle.loads(body))
        cmd = pickle.loads(body)['cmd']
        print('recived command[%s]'%cmd)
        res = self.Run_Command(cmd)
        data = {'res':res}
        self.Channel.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                #标识回复主机和任务ID
                message_id=props.reply_to,
                correlation_id=self.MyHost
            ),
            body=pickle.dumps(data)
        )



    def Run_Command(self,cmd):
        res = os.popen(cmd).read()
        return res


    def Get_Host(self):
        '''
        linux虚拟机多网卡，测试不通过，弃用
        :return:
        '''
        hostname = socket.gethostname()
        #ip = socket.gethostbyname(socket.gethostname())
        ipList = socket.gethostbyname_ex(socket.gethostname())
        print(ipList)
        return hostname

    def Get_Ip(self):
        '''
        linux虚拟机多网卡，测试不通过，弃用
        :return:
        '''
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

