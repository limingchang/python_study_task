# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import socket,pickle,hashlib

class Ftp_Client(object):
    def __init__(self):
        self.client = socket.socket()
        self.connection('localhost',6512)
        #self.handle()

    def connection(self,ip,port):
        '''
        连接服务端
        :param ip: 服务端ip
        :param port: 服务端端口
        :return:
        '''
        self.client.connect((ip,port))


    def handle(self):
        data={'action':'Chk_Platform'}
        self.client.send(pickle.dumps(data))
        self.Chk_Platform = self.client.recv(1024).decode()
        self.client.close()
        #print(self.Chk_Platform.decode())

    def Auth(self,username,password):
        data={
            'action':'Auth',
            'username':username,
            'password':password
        }
        self.client.send(pickle.dumps(data))
        auth_res = pickle.loads(self.client.recv(1024))
        return auth_res


    def Dir_List(self,list_path):
        data = {
            'action':'Dir_List',
            'path':list_path
        }
        self.client.send(pickle.dumps(data))
        total_data_size = self.client.recv(1024).decode()
        print('total:',total_data_size)
        total_data_size = int(total_data_size)
        self.client.send(b'ok')
        recv_data_size = 0
        recv_data = b''
        while recv_data_size < total_data_size:
            if total_data_size - recv_data_size <1024:
                size = total_data_size - recv_data_size
            else:
                size = 1024
            tmp_data = self.client.recv(size)
            recv_data += tmp_data
            recv_data_size += len(tmp_data)
        else:
            list_res = pickle.loads(recv_data)
        return list_res


    def Chk_File(self,chk_path):
        '''
        检查云端路径是文件还是目录
        :return: True文件，False目录
        '''
        data = {
            'action':'Chk_File',
            'path':chk_path
        }
        self.client.send(pickle.dumps(data))
        chk_res = pickle.loads(self.client.recv(1024))
        return chk_res['res']


    def Get_HomePath(self,username):
        '''
        获取云端个人目录
        :return:
        '''
        data = {
            'action':'Get_HomePath',
            'username':username
        }
        self.client.send(pickle.dumps(data))
        home_path = pickle.loads(self.client.recv(1024))
        return home_path['path'],home_path['sep']


    def UpLoad_File(self,File_Path,save_path,window,progress_bar_obj,max_bar_width):
        '''
        上传文件
        :param File_Path: 上传文件的路径
        :param save_path: 保存文件的路径
        :param window: 进度条窗口对象
        :param scroll_bar_obj: 进度条对象
        :param max_bar_width: 进度条最大宽度
        :return:
        '''
        file_size = os.path.getsize(File_Path)
        file_name = os.path.basename(File_Path)
        data = {
            'action':'UpLoad_File',
            'file_size':file_size,
            'file_name':file_name,
            'save_path':save_path
        }
        self.client.send(pickle.dumps(data))
        chk = pickle.loads(self.client.recv(1024))#接收服务端确认消息，是否为续传
        file = open(File_Path,'rb')
        if chk['continue']:#续传
            file.seek(chk['recv_size'])
        else:
            file.seek(0)
        send_size = 0
        for line in file:
            self.client.send(line)
            send_size += len(line)
            #MD5验证
            md5 = hashlib.md5()
            md5.update(line)
            percent = int(send_size/ (file_size - chk['recv_size'])*10000)/100
            bar_width = int(max_bar_width * send_size/ (file_size - chk['recv_size']))
            progress_bar_obj['width'] = bar_width
            progress_bar_obj.place(width=bar_width)
            if bar_width < int(max_bar_width / 3):
                progress_bar_obj['bg'] = '#FF4040'
            elif bar_width < int(max_bar_width / 3 *2):
                progress_bar_obj['bg'] = '#836FFF'
            else:
                progress_bar_obj['bg'] = '#32CD32'

            progress_bar_obj['text'] = str(percent)+'%'
            window.update_idletasks()
        chk_md5 =pickle.loads(self.client.recv(1024))
        if chk_md5['md5'] == md5.hexdigest():
            res = '上传完成，文件MD5核对一致.'
        else:
            res = '文件MD5异常，请重新上传.'
        return res







if __name__ == '__main__':
    client = Ftp_Client()
