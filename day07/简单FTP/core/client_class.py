# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os,pickle

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import socket,configparser
from core import error_class

class Client_Class(object):
    def __init__(self):
        '''
        创建客户端socket对象
        '''
        self.Sep = os.sep#路径分隔符
        self.Get_Config()
        self.Conn()
        self.Send_Data()
        self.Close()



    def Conn(self,ip='localhost'):
        self.client = socket.socket()
        self.client.connect((ip,self.Port))#创建客户端连接
        print('客户端准备就绪...')


    def Send_Data(self):
        while True:
            # data = '客户端发中文'#所有数据发送和接收必须使用byte格式
            data = input('请输入指令(输入help显示帮助）：')
            if len(data) == 0: continue
            data = data.strip().lower()
            if data == 'help':
                self.Help()
                continue
            else:
                data = data.split(' ')
                act = []
                for i in range(len(data)):
                    data[i] = data[i].strip()
                    if data[i] != '':act.append(data[i])
                if act[0] == 'upload':
                    res = self.Upload_Flie(act)
                    if res['msg']:
                        act[1] = res['data']
                        #print(act)
                        self.client.sendall(pickle.dumps(act))
                    else:
                        print(res['data'])
                        continue
                else:
                    self.client.send(pickle.dumps(act))
                #接收服务器返回
                data = self.client.recv(self.Send_Size)
                self.Recv(data)

    def Upload_Flie(self,act):
        '''
        上传文件
        :return: [act,data]=>[操作标识，二进制文件数据]
        '''
        res = {'msg':False}
        if len(act) != 3:
            res['data'] = self.Show_Error(2,act[0])
        else:
            filename = act[1]
            if os.path.exists(filename):
                f = open(filename,'rb')
                data = f.read()
                if len(data) > self.Send_Size - 100:
                    res['data'] = self.Show_Error(302,act[0])
                else:
                    res = {
                        'msg':True,
                        'data':data
                    }
                f.close()
            else:
                res['data'] = self.Show_Error(301,act[0])
        return res


    def Recv(self,data):
        print('服务器回复：'.center(60,'-'))
        info = pickle.loads(data)
        #print('type:', type(info['res']))
        #print(info)
        if info['act'] == 'download':
            if isinstance(info['res'],error_class.Server_Error):
                print(info['res'])
            else:
                msg = self.DownLoad_File(info['res'])
                print(msg)
        else:
            print('当前客户端[%s]:%s'%(info['address'],info['port']))
            print(info['res'])


    def Help(self):
        str = '\033[1;36;1m简单FTP指令帮助\033[0m'.center(60,'*') + '\n'
        str = '%shelp -显示帮助\n'%str
        str = '%supload [filename][cloud_filename] -上传文件，filename=完整的本地路径，cloud_filename=云端文件名\n'%str
        str = '%sls -显示云端个人目录下文件列表\n'%str
        str = '%slogin [username] [password] -用户登录\n'%str
        str = '%sdownload [filename] [local_filename] -下载云端文件，filename=云端文件名,local_filename=本地文件名'%str
        print(str)


    def Get_Config(self):
        '''
        获取配置信息
        :return:
        '''
        config = configparser.ConfigParser()
        config_path = '{_path}{_sep}config{_sep}config.ini'.format(_path=path,_sep=self.Sep)
        config.read(config_path)
        self.Port = int(config['CLIENT']['port'])#获取客户端链接端口
        self.Send_Size = int(config['CLIENT']['send_size'])#最大发送数据大小，默认10mb


    def DownLoad_File(self,data):
        '''
        下载文件-》客户端
        :param data: [data,filename]下载的二进制文件数据
        :return:
        '''
        filename = data[1]
        filedata = data[0]
        if os.path.exists(filename):
            filname_ext = filename.split('.')
            filename='%s(1)%s'%(filname_ext[0],filname_ext[1])#文件存在则重命名
        with open(filename,'wb') as f:
            f.write(filedata)
        res = self.Show_Error(0,'download')
        return res


    def Close(self):
        self.client.close()

    def Show_Error(self,errcode,act):
        try:
            raise error_class.Client_Error(errcode,act)
        except error_class.Client_Error as e:
            return e


if __name__ == '__main__':
    client = Client_Class()