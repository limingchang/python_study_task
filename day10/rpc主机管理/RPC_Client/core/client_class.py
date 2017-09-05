# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import pika,configparser,random

class RPC_Client(object):
    '''
    RPC主机管理客户端
    '''
    def __init__(self):
        '''
        实例化立即创建RabbitMQ连接
        :param ip: RabbitMQ-server地址
        :param port: 端口
        :param user: 用户名
        :param pwd: 密码
        '''
        #获取配置信息
        self.Get_Conf()
        # print(self.__dict__)
        # 创建结果空字典，保存命令结果
        self.Res_Dict = {}

    def Get_Conf(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(path,'conf','config.ini'))
        self.Host = config['RabbitMQ']['host']
        self.Port = config['RabbitMQ']['port']
        self.Credentials = pika.PlainCredentials(config['RabbitMQ']['user'], config['RabbitMQ']['pwd'])

    def Handler(self):
        '''
        创建RabbitMQ连接和信道
        :return:
        '''
        self.Conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.Host,
                port=self.Port,
                credentials=self.Credentials
            )
        )
        self.Channel = self.Conn.channel()


    def Command_Parse(self):
        '''
        命令输入和解析
        :return:
        '''
        while True:
            act = input('>>:').strip()
            act_list = act.split('"')
            if act.startswith('run'):
                if len(act_list) == 3:
                    cmd = act_list[1]
                    host_str = act_list[2].strip()
                    host_grop = host_str.split(' ')
                    host_list = []
                    for i in range(1,len(host_grop)):
                        host_list.append(host_grop[i])
                    self.Run(cmd,host_list)
                else:
                    print('\033[1;31;1mCommand Error!\033[0m')
                    self.Help()
            elif act.startswith('check_task'):
                if len(act_list) == 2:
                    task_id = act_list[1]
                    self.Get_Result(task_id)
                else:
                    print('\033[1;31;1mCommand Error!\033[0m')
                    self.Help()
            elif act == 'quit':
                exit()
            else:
                print('\033[1;31;1mCommand Error!\033[0m')
                self.Help()



    def Help(self):
        '''
        显示帮助信息
        :return:
        '''
        print('\033[1;36;1mrun shell: run "command" [--host hostname]')
        print('you must add " at command start and end or it will be error')
        print('get result: check_task task_id')
        print('input quit to exit\033[0m')

    def Run(self,cmd,host_list):
        '''
        发送命令给主机执行
        :param cmd: 要执行的命令
        :param host_list: 主机列表
        :return:
        '''
        print(cmd)
        print(host_list)

    def Create_TaskID(self):
        '''
        生成taskid,递归防止重复
        :return: 返回生成5位整数的ID
        '''
        task_id = ''
        for i in range(5):
            current = random.randrange(0, 9)
            task_id += str(current)
        task_id = int(task_id)
        if task_id in self.Res_Dict:
            self.Create_TaskID()
        else:
            self.Res_Dict[task_id]=''
        return task_id

    def Get_Result(self,id):
        '''
        结果获取
        :param id:task_id
        :return: 返回取到的结果
        '''
        pass



if __name__ == "__main__":
    rpc_cli = RPC_Client()
    #rpc_cli.Command_Parse()
    a = rpc_cli.Create_TaskID()
    print(a)