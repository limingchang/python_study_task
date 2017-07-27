# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os,pickle

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
#服务端类
import socket,configparser
from core import error_class

class Server_Class(object):
    def __init__(self):
        '''
        创建socket服务端对象并建立连接和监听
        '''
        self.Sep = os.sep
        self.Is_Login = False
        self.Check_Defult_User()
        self.Get_Config()
        self.Conn()
        while True:
            self.Accept()
        self.Close()



    def Conn(self,ip='localhost'):
        '''
        创建连接
        :return:
        '''
        self.Server = socket.socket()
        self.Server.bind((ip, self.Port))  # 绑定监听端口
        self.Server.listen()  # 监听
        print('服务器准备就绪...')




    def Accept(self):
        '''
        等待数据传输
        :return:
        '''
        conn,addr = self.Server.accept()
        #print('客户端【%s】正在连接...'%addr[0])
        while True:
            data = conn.recv(self.Recv_Size)
            if not data:
                print('客户端断开...')
                break
            act = pickle.loads(data)
            #act = data
            #print('server|recv:',act )

            #data = '【%s】发送数据成功'%addr[0]
            data = {
                'errcode':0,
                'errmsg':'ok',
                'address':addr[0],
                'port':addr[1],
                'act':act[0],
                'res':self.Run_Action(act)
            }
            #print(data)
            conn.sendall(pickle.dumps(data))


    def Run_Action(self,order):
        '''
        解析运行指令
        :param order:需要运行的指令
        :return: 运行结果的json
        '''
        self.Order = order
        if order[0] == 'ls':
            res = self.Show_Cloud_Flie()
        elif order[0] == 'download':
            res = self.DownLoad_File()
        elif order[0] == 'upload':
            res = self.Upload_File()
        elif order[0] == 'login':
            res = self.Auth()
        else:
            res = self.Show_Error(-1,self.Order[0])
        return res

    def Auth(self):
        '''
        登录验证
        :return:
        '''
        if len(self.Order) != 3:
            res = self.Show_Error(2,self.Order[0])
        else:
            username = self.Order[1]
            password = self.Order[2]
            user_info_file = os.path.join(path, 'db', 'user_%s.dat'%username)
            if not self.Is_Login:
                if os.path.exists(user_info_file):
                    with open(user_info_file,'rb') as f:
                        info = pickle.load(f)
                    if username == info['username'] and password == info['password']:
                        self.Is_Login = True
                        self.User_Info = info
                        res = self.Show_Error(100,self.Order[0])
                    else:
                        res = self.Show_Error(101,self.Order[0])
                else:
                    res = self.Show_Error(102,self.Order[0])
        return res


    def Check_Defult_User(self):
        '''
        检查缺省用户文件是否存在
        :return:
        '''
        user_info_file=os.path.join(path,'db','user_admin.dat')
        home_path = os.path.join(path, 'home', 'admin')
        if not os.path.exists(user_info_file):
            with open(user_info_file,'wb') as f:
                info = {
                    'username':'admin',
                    'password':'admin'
                }
                pickle.dump(info,f)
        if not os.path.exists(home_path):
            os.makedirs(home_path)


    def Upload_File(self):
        '''
        上传文件服务端处理函数
        :return:
        '''
        if self.Is_Login:
            home_path = os.path.join(path, 'home', self.User_Info['username'])
            filename =os.path.join(home_path,self.Order[2])
            if not os.path.exists(home_path):
                os.makedirs(home_path)
            if len(self.Order[1]) > self.Recv_Size - 100:
                res = self.Show_Error(302,self.Order[0])
            else:
                if os.path.exists(filename):
                    filname_ext = filename.split('.')
                    filename='%s(1)%s'%(filname_ext[0],filname_ext[1])
                with open(filename,'wb') as f:
                    f.write(self.Order[1])
                res = self.Show_Error(0,self.Order[0])
        else:
            print('nologin')
            res = self.Show_Error(1,self.Order[0])
        return res


    def Show_Cloud_Flie(self):
        '''
        返回云端文件列表
        :return:
        '''
        if self.Is_Login:
            home_path = os.path.join(path, 'home', self.User_Info['username'])
            if os.path.exists(home_path):
                res = os.listdir(home_path)
            else:
                os.makedirs(home_path)
                res = os.listdir(home_path)
        else:
            res = self.Show_Error(1,self.Order[0])
        return res


    def DownLoad_File(self):
        '''
        文件下载
        :return:二进制文件数据
        '''
        if self.Is_Login:
            home_path = os.path.join(path, 'home', self.User_Info['username'])
            file_list = os.listdir(home_path)
            if len(self.Order) != 3:
                res = self.Show_Error(2,self.Order[0])
            elif self.Order[1] in file_list:
                filename =os.path.join(home_path,self.Order[1])
                f = open(filename,'rb')
                res = [f.read(),self.Order[2]]
            else:
                res = self.Show_Error(303,self.Order[0])
        else:
            res = self.Show_Error(1,self.Order[0])
        return res



    def Get_Config(self):
        '''
        获取配置信息
        :return:
        '''
        config = configparser.ConfigParser()
        config_path = '{_path}{_sep}config{_sep}config.ini'.format(_path=path, _sep=self.Sep)
        config.read(config_path)
        self.Port = int(config['SERVER']['port'])#获取服务端监听端口
        self.Recv_Size = int(config['SERVER']['recv_size'])#最大接收数据大小，默认10mb


    def Close(self):
        self.Server.close()


    def Show_Error(self,errcode,act):
        try:
            raise error_class.Server_Error(errcode,act)
        except error_class.Server_Error as e:
            return e


if __name__ == '__main__':
    #server = Server_Class()
    home_path =os.path.join(path,'home','admin')
    print(home_path)
