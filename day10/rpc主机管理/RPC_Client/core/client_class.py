# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import pika,configparser,random,pickle
import time,threading

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
        self.Port = int(config['RabbitMQ']['port'])
        self.Time_Out = int(config['RabbitMQ']['timeout'])#设置超时时间
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
                        #生成任务ID
                        task_id = self.Create_TaskID()
                        #创建主机列表
                        for i in range(1,len(host_grop)):
                            host_list.append(host_grop[i])
                        #这里创建多线程
                        thread = threading.Thread(
                            target=self.Run,
                            args=(task_id,cmd,host_list)
                        )
                        thread.start()
                        continue
                        #self.Run(cmd,host_list)
                else:
                    print('\033[1;31;1mCommand Error!\033[0m')
                    self.Help()
                continue
            elif act.startswith('check_task'):
                act_list = act.split()
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

    def Run(self,task_id,cmd,host_list):
        '''
        发送命令给主机执行
        :param task_id: 任务id
        :param cmd: 要执行的命令
        :param host_list: 主机列表
        :return:
        '''
        #print(cmd)
        #print(host_list)
        self.Handler()
        #result = self.Channel.queue_declare(exclusive=True)
        #self.Response_Queue = result.method.queue#创建随机queue
        #创建接收端消费者，用于接收返回结果
        self.Channel.queue_declare(queue=task_id)
        self.Channel.basic_consume(
            self.On_Response,#callback
            queue=task_id
        )
        self.Send_Cmd(task_id,cmd,host_list)


    def Send_Cmd(self,task_id,cmd,host_list):
        #task_id = self.Create_TaskID()
        #self.Res_Dict[task_id] = None
        #将返回结果初始化为空
        for host in host_list:
            self.Res_Dict[task_id][host] = ''
        #构建消息数据
        data = { 'cmd':cmd}
        #self.corr_id = str(task_id)
        #循环创建发送端，绑定转发器RPC，指定routing_key为hostip
        self.Channel.exchange_declare(
            exchange='rpc',
            exchange_type='direct'
        )
        for host in host_list:
            self.Channel.basic_publish(
                exchange='rpc',
                routing_key=host,
                properties=pika.BasicProperties(
                    #标识返回queue
                    reply_to=task_id,
                ),
                body=pickle.dumps(data)
            )
        #循环接收结果
        for host in host_list:
            count = 0
            while self.Res_Dict[task_id][host] == '':
                self.Conn.process_data_events()
                time.sleep(0.1)
                count +=1
                if count > self.Time_Out*10:
                    print('host[%s] connection timeout.'%host)
                    break
        print('Command[%s]=>'%cmd,host_list,'completed！')
        print('Please use [check_task] get result.')


    def On_Response(self,ch,method,props,body):
        '''
        处理返回结果的函数
        :return:
        '''
        task_id = props.message_id
        res = pickle.loads(body)['res']
        host = props.correlation_id
        #返回为字典{host:res}
        print('recived host[%s] response message.' %host)
        self.Res_Dict[task_id][host] = res
        #告知已收到
        self.Channel.basic_ack(delivery_tag=method.delivery_tag)


    def Create_TaskID(self):
        '''
        生成taskid,递归防止重复
        :return: 返回生成5位整数的ID
        '''
        task_id = ''
        for i in range(5):
            current = random.randrange(0, 9)
            task_id += str(current)
        #task_id = int(task_id)
        if task_id in self.Res_Dict:
            self.Create_TaskID()
        else:
            self.Res_Dict[task_id] = {}
        print('task_id:',task_id)
        return task_id

    def Get_Result(self,id):
        '''
        结果获取
        :param id:task_id
        :return: 返回取到的结果
        '''
        for host in self.Res_Dict[id]:
            print(('From host %s'%host).center(50,'-'))
            print(self.Res_Dict[id][host])
        #提取结果就删除

        del self.Res_Dict[id]

        #print(self.Res_Dict[id])



if __name__ == "__main__":
    rpc_cli = RPC_Client()
    rpc_cli.Command_Parse()
    #a = rpc_cli.Create_TaskID()
    #print(a)