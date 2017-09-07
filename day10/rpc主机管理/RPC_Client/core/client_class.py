# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import pika,configparser,random,pickle

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
        #创建任务ID空列表
        self.Task_List = []


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
                    if '--host' not in host_str:
                        print('Parameter Error!')
                    else:
                        host_grop = host_str.split(' ')
                        host_list = []
                        for i in range(1,len(host_grop)):
                            host_list.append(host_grop[i])
                        #这里创建多线程
                        self.Run(cmd,host_list)
                else:
                    print('\033[1;31;1mCommand Error!\033[0m')
                    self.Help()
                continue
            elif act.startswith('check_task'):
                if len(act_list) == 2:
                    task_id = act_list[1]
                    self.Get_Result(task_id)
                else:
                    print('\033[1;31;1mCommand Error!\033[0m')
                    self.Help()
                continue
            elif act == 'quit':
                break
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
        self.Handler()
        result = self.Channel.queue_declare(exclusive=True)
        self.Response_Queue = result.method.queue#创建随机queue
        #创建接收端消费者，用于接收返回结果
        self.Channel.basic_consume(
            self.On_Response,#callback
            no_ack=True,
            queue=self.Response_Queue
        )


    def Send_Cmd(self,cmd,host_list):
        task_id = self.Create_TaskID()
        #self.Res_Dict[task_id] = None
        #将返回结果初始化为空
        for host in host_list:
            self.Res_Dict[task_id][host] = None
        #构建消息数据
        data = {
            'cmd':cmd,
            'host_list':host_list
        }
        #加入任务ID列表
        self.Task_List.append(task_id)
        #self.corr_id = str(task_id)
        #创建发送端
        self.Channel.basic_publish(
            exchange='',
            routing_key='rpc',
            properties=pika.BasicProperties(
                #标识返回queue
                reply_to=self.Response_Queue,
                #标识命令任务ID
                correlation_id=str(task_id)
            ),
            body=pickle.dumps(data)
        )
        #循环接收结果
        for host in host_list:
            while self.Res_Dict[task_id][host] is None:
                self.Conn.process_data_events()
            print('收到主机【%s】返回消息'%host)
        print('命令【%s】=>'%cmd,host_list,'执行完毕！')
        print('请使用check_task命令获取结果')


    def On_Response(self,ch,method,props,body):
        '''
        处理返回结果的函数
        :return:
        '''
        task_id = props.correlation_id
        res_data = pickle.loads(body)
        #返回为字典{host:res}
        self.Res_Dict[task_id][res_data['host']] = res_data['res']



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
            self.Res_Dict[task_id] = None
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
    rpc_cli.Command_Parse()
    #a = rpc_cli.Create_TaskID()
    #print(a)