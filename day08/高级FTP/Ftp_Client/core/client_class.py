# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import socket,pickle,hashlib

class Ftp_Client(object):
    def __init__(self):
        self.client = socket.socket()
        self.Server_Ip,self.Server_Port = self.get_config()
        self.connection(self.Server_Ip,self.Server_Port)
        #self.handle()

    def connection(self,ip,port):
        '''
        连接服务端
        :param ip: 服务端ip
        :param port: 服务端端口
        :return:
        '''
        self.client.connect((ip,port))

    def get_config(self):
        import configparser
        config = configparser.ConfigParser()
        config_path = os.path.join(path,'conf','config.ini')
        config.read(config_path)
        ip = config['CLIENT']['server_ip']
        port = int(config['CLIENT']['server_port'])  # 获取端口
        return ip,port


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
        #print('total:',total_data_size)
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
        md5 = hashlib.md5()
        for line in file:
            self.client.send(line)
            send_size += len(line)
            #MD5验证
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

    def DownLoad_File(self,DownLoad_Path,window,progress_bar_obj,max_bar_width):
        '''
        下载文件
        :param DownLoad_Path: 服务器下载路径
        :param window: 进度条窗口
        :param progress_bar_obj: 进度条对象
        :param max_bar_width: 进度条最大宽度
        :return:
        '''
        file_name =os.path.basename(DownLoad_Path)
        if os.path.isfile(file_name):#文件存在则为续传模式
            recv_file_size =os.path.getsize(file_name)
            data = {
                'action':'DownLoad_File',
                'path':DownLoad_Path,
                'continue':True,
                'recv_size':recv_file_size
            }
            f = open(file_name,'ab')
        else:
            recv_file_size = 0
            data = {
                'action': 'DownLoad_File',
                'path': DownLoad_Path,
                'continue': False,
                'recv_size': 0
            }
            f = open(file_name,'wb')
        self.client.send(pickle.dumps(data))#发送下载请求
        #获得服务端回复的文件大小
        chk =pickle.loads(self.client.recv(1024))
        need_file_size = chk['filesize']
        recv_size = 0 #本次收到的大小
        #接收下载文件
        md5 = hashlib.md5()
        while recv_size < need_file_size:
            if need_file_size - recv_size <1024:
                size = need_file_size - recv_size
            else:
                size =1024
            file_data = self.client.recv(size)
            recv_size += len(file_data)
            f.write(file_data)
            # MD5验证

            md5.update(file_data)
            percent = int(recv_size / need_file_size * 10000) / 100
            bar_width = int(max_bar_width * recv_size / need_file_size)
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
        else:
            chk_md5 = {"chk_md5":md5.hexdigest()}
            #print(chk_md5)
            self.client.send(pickle.dumps(chk_md5))#发送md5校检
            chk_md5 =pickle.loads(self.client.recv(1024)) #接收服务端校检结果
            if chk_md5['chk_md5']:
                res = '下载完成，文件MD5核对一致.'
            else:
                res = 'MD5校检异常，请重新下载.'
        return res


    def Chk_Space(self,username,space,up_file):
        '''
        检查个人空间限额
        :param space: 个人空间总限额
        :param up_file: 要上传的文件
        :return:
        '''
        up_size = os.path.getsize(up_file)
        data = {
            'action':'Chk_Space',
            'username':username,
            'space':space,
            'up_size':up_size
        }
        self.client.send(pickle.dumps(data))
        chk_res =pickle.loads(self.client.recv(1024))
        return chk_res['chk_space']

    def Create_Dir(self,will_create_dir,dir_name):
        '''
        创建文件夹
        :param will_create_dir: 将要在哪个目录创建文件夹
        :param dir_name: 要创建的文件夹名
        :return:
        '''
        data = {
            'action':'Create_Dir',
            'will_create_dir':will_create_dir,
            'dir_name':dir_name
        }
        self.client.send(pickle.dumps(data))
        res = pickle.loads(self.client.recv(1024))
        return '创建目录成功！'






if __name__ == '__main__':
    client = Ftp_Client()
