# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)


import socket
import selectors
import logging,configparser,pickle


class Ftp_Server(object):
    '''
    selectors版FTP，IO多路复用
    '''
    def __init__(self):
        self.Sel = selectors.DefaultSelector()
        self.Action = {}#存储每个连接的命令，以conn作为标识
        self.File_Obj = {}#存储每个连接的FTP文件信息，以conn作为标识

        #获取配置文件
        self.Get_Conf()
        #创建socket
        self.Handle()


    def Handle(self):
        sock = socket.socket()
        sock.bind((self.IP,self.Port))
        sock.listen()
        sock.setblocking(False)#默认不阻塞
        #注册selector事件
        self.Sel.register(sock,selectors.EVENT_READ,self.Accept)
        while True:
            events = self.Sel.select()
            for key , mask in events:
                #print('活动IO：',key.fileobj)
                #print('回调：',key.data)
                callback = key.data
                callback(key.fileobj,mask)
            #break



    def Get_Conf(self):
        '''
        获取配置信息
        :return:
        '''
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.IP = conf['SERVER']['ip']
        self.Port = int(conf['SERVER']['port'])




    def Accept(self,sock,mask):
        conn,addr = sock.accept()
        print('客户端接入:',addr)
        conn.setblocking(False)#设置不阻塞
        self.Sel.register(conn,selectors.EVENT_READ,self.Read)


        pass

    def Read(self,conn,mask):
        '''
        读取客户端过来的命令
        :return:
        '''
        try:
            cmd = conn.recv(1024)
            if cmd:
                #print(pickle.loads(cmd))
                cmd_dict = pickle.loads(cmd)
                if cmd_dict['act'] == 'upload':
                    conn.send(b'ready')  # 发送确认信息防止粘包 up:1
                    self.Action[conn] = cmd_dict#参数存储进字典
                    #重新注册事件，以更换回调函数，进入接收文件大小
                    self.Sel.unregister(conn)
                    self.Sel.register(conn,selectors.EVENT_READ,self.UpLoad_Get_FileSize)
                    print(self.Action[conn])
                elif cmd_dict['act'] == 'download':
                    conn.send(b'ready')# 发送确认信息防止粘包 down:1
                    self.Action[conn] = cmd_dict
                    # 重新注册事件，以更换回调函数，进入发送文件大小
                    self.Sel.unregister(conn)
                    self.Sel.register(conn,selectors.EVENT_READ,self.DownLoad_Send_FileSize)


            else:
                self.Sel.unregister(conn)
                conn.close()
        except Exception as e:
            self.Sel.unregister(conn)
            conn.close()
            print(e)


    def DownLoad_Send_FileSize(self,conn,mask):
        '''
        发送下载文件大小
        :param conn:
        :param mask:
        :return:
        '''
        data = {'size':0}
        print('文件下载：',self.Action[conn]['cloudfile'])
        chk = conn.recv(1024)#down:2 接收一个激活信号
        filename = self.Action[conn]['cloudfile']
        if os.path.isfile(filename):#判断文件是否存在
            data['size'] = os.path.getsize(filename)
            conn.send(pickle.dumps(data))#发送文件大小
            f = open(filename,'rb')
            self.File_Obj[conn] = {
                'file_obj': f
            }
            #重新注册监听事件
            self.Sel.unregister(conn)
            self.Sel.register(conn,selectors.EVENT_READ,self.DownLoad_Send_FileDta)
        else:
            conn.send(pickle.dumps(data))  # 发送0大小，标识文件不存在
            #回到read回调监听
            self.Sel.unregister(conn)
            self.Sel.register(conn, selectors.EVENT_READ, self.Read)
            del self.Action[conn]


    def DownLoad_Send_FileDta(self,conn,mask):
        '''
        发送下载文件数据
        :param conn:
        :param mask:
        :return:
        '''
        chk = conn.recv(1024)#接收接货信号 down:3
        file_obj = self.File_Obj[conn]['file_obj']
        for line in file_obj:
            conn.send(line)
        file_obj.close()
        #发送完毕，重新进入read监听
        self.Sel.unregister(conn)
        self.Sel.register(conn, selectors.EVENT_READ, self.Read)
        del self.Action[conn]
        del self.File_Obj[conn]





    def UpLoad_Get_FileSize(self,conn,mask):
        '''
        接收客户端发送过来的文件大小
        :param conn:
        :param mask:
        :return:
        '''
        print('文件上传:',self.Action[conn]['localfile'])
        file_size = pickle.loads(conn.recv(1024))
        print('文件大小：',file_size['size'])
        if file_size['size'] == 0:
            print('客户端文件不存在，取消发送')
            #解绑事件，重新进入命令监听事件
            self.Sel.unregister(conn)
            self.Sel.register(conn,selectors.EVENT_READ,self.Read)
        else:
            new_filename = self.ReNmae(self.Action[conn]['localfile'])
            print('收到客户端发送大小：',file_size)
            f = open(new_filename,'wb')
            # 将文件信息记录入全局字典
            self.File_Obj[conn] = {
                'file_obj':f,
                'tmp_file':new_filename,#临时文件名
                'filesize':file_size['size'],#文件总大小
                'recved_size':0,#已接收大小
                'save_as':self.Action[conn]['cloudfile']#保存为的文件名
            }
            conn.send(b'ok')#发送验证数据给客户端，防止粘包
            #重新注册事件，将下一个活动IO交给接收文件数据函数处理
            self.Sel.unregister(conn)
            self.Sel.register(conn,selectors.EVENT_READ,self.UpLoad_Get_FileData)



    def UpLoad_Get_FileData(self,conn,mask):
        '''
        接收文件数据
        :return:
        '''
        filesize = self.File_Obj[conn]['filesize']
        recved_size = self.File_Obj[conn]['recved_size']
        if filesize - recved_size == 0:#文件接收完毕
            #解绑事件
            self.Sel.unregister(conn)
            #重新注册事件监听
            self.Sel.register(conn, selectors.EVENT_READ, self.Read)
            del self.Action[conn] #删除临时数据
            self.File_Obj[conn]['file_obj'].close()#关闭文件
            print(conn.recv(1024).decode())
            print('完成接收，关闭文件')
            self.ReNmae(self.File_Obj[conn]['tmp_file'],self.File_Obj[conn]['save_as'])#重命名文件
            del self.File_Obj[conn]#删除文件句柄
        else:
            if filesize - recved_size < 1024:
                size = filesize - recved_size
            else:
                size =1024
            file_data = conn.recv(size)
            self.File_Obj[conn]['recved_size'] += len(file_data)#记录接收大小
            self.File_Obj[conn]['file_obj'].write(file_data)#写入文件




    def ReNmae(self,filename,type='tmp'):
        '''
        重命名文件
        :param filename:要重命名的文件
        :param type: tmp参数时，在文件最后扩展名加上.tmp;normal参数时，将tmp后缀去掉；其他参数时，type接收一个文件名，重命名为此文件名
        :return:新的文件名
        '''
        file_exp = filename.split('.')
        if type == 'tmp':
            file_exp.append('tmp')
            new_filename = '.'.join(file_exp)
        elif type == 'normal':
            file_exp.pop()
            new_filename = '.'.join(file_exp)
        else:
            #print('重命名参数错误！')
            os.rename(filename,type)
            new_filename = type

        return new_filename


server = Ftp_Server()

