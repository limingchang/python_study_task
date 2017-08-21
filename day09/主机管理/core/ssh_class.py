# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import paramiko
import configparser,logging
from datetime import datetime
class Host_Manage(object):
    '''
    类Fabric主机管理程序
    '''
    def __init__(self):
        self.Get_Conf()
        print(self.DB_NAME,self.LOG_PATH)
        self.Create_SSHClient('192.168.0.201',22,'limingchang','123456','ls')
        # cmd = {
        #     'act':'download',
        #     'local_file':'up.dat',
        #     'host_file': '/home/limingchang/test.dat'
        # }
        # self.Create_SSHFTP('192.168.0.201',22,'limingchang','123456',cmd)


    def Create_SSHClient(self,ip,port,user,pwd,command):
        '''
        SSH执行命令
        :param ip: 主机地址
        :param port: 主机SSH端口
        :param user: 用户名
        :param pwd: 密码
        :param command: 执行的命令
        :return: 直接打印
        '''
        SSH = paramiko.SSHClient()
        SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        res_msg = ip.center(50, '-')
        try:
            SSH.connect(hostname=ip,port=port,username=user,password=pwd)
            stdin, stdout, stderr = SSH.exec_command(command)
            res, err = stdout.read(), stderr.read()
            result = res if res else err
            res_msg +='\n'+ result.decode()
            #print(result.decode())
        except paramiko.ssh_exception.AuthenticationException as e:
            res_msg += '\n\033[1;31;1m身份验证失败:\n[用于此主机的用户名或密码错误]\033[0m'
            self.Write_Log('warning','主机[%s]身份验证失败'%ip)
            #print('\033[1;31;1m身份验证失败[用于此主机的用户名或密码错误]\033[0m')
        except TimeoutError as e:
            res_msg += '\n\033[1;31;1m主机无响应\033[0m'
            self.Write_Log('error', '主机[%s]无响应' % ip)
            #print('主机无响应')
        else:
            self.Write_Log('info','主机[%s]执行命令[%s]成功'%(ip,command))
        finally:
            res_msg += '\n'+'*'*50
            #print('*'*50)
        print(res_msg)


    def Create_SSHFTP(self,ip,port,user,pwd,command):
        '''
        FTP方法
        :param ip:主机地址
        :param port: 端口
        :param user: 用户名
        :param pwd: 密码
        :param command: 命令组
        {'act':'upload or download'
        'local_file':本地文件
        'host_file':云端文件
        }
        :return:
        '''
        transport = paramiko.Transport(ip, port)
        transport.connect(username=user, password=pwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        # 将localtion.py上传至服务器/tmp/test.py
        cmd_dict = command
        res_msg = ip.center(50,'-')
        if cmd_dict['act'] == 'upload':
            try:
                sftp.put(cmd_dict['local_file'],cmd_dict['host_file'])
            except FileNotFoundError:
                res_msg += '\n'+'\033[1;31,1m本地文件或云端文件夹不存在\033[0m'
                self.Write_Log('warning','上传时错误[%s]:本地[%s]或云端[%s]不存在'%(ip,cmd_dict['local_file'],cmd_dict['host_file']))
            else:
                res_msg += '\n' +'[文件:%s]上传至[%s]成功'%(cmd_dict['local_file'],cmd_dict['host_file'])
                self.Write_Log('info','[%s]上传文件[%s]成功'%(ip,cmd_dict['host_file']))
            finally:
                res_msg += '\n'+'*'*50
            print(res_msg)
        elif cmd_dict['act'] == 'download':
            try:
                sftp.get(cmd_dict['host_file'], cmd_dict['local_file'])
            except FileNotFoundError:
                res_msg += '\n' + '\033[1;31,1m云端文件不存在\033[0m'
                self.Write_Log('warning','从[%s]下载错误:[%s]不存在'%(ip,cmd_dict['host_file']))
            else:
                res_msg += '\n' + '[文件:%s]下载至[%s]成功' % (cmd_dict['host_file'],cmd_dict['local_file'])
                self.Write_Log('info', '从[%s]下载[%s]成功' % (ip, cmd_dict['host_file']))
            finally:
                res_msg += '\n' + '*' * 50
                print(res_msg)
        else:
            print('FTP命令错误')
        #FileNotFoundError: [Errno 2] No such file
        # 将remove_path下载到本地local_path
        #sftp.get('remove_path', 'local_path')

        transport.close()



    def Get_Conf(self):
        Config= configparser.ConfigParser()
        Config.read(os.path.join(path,'conf','conf.ini'))
        self.DB_NAME = Config['DEFAULT']['DB_NAME']
        self.LOG_PATH = Config['DEFAULT']['LOG_PATH']

        #print(Config.sections())

    def Write_Log(self,level,msg):
        '''
        日志记录模块
        :param level:日志级别
        :param msg: 消息
        :return: msg
        '''
        log_file = datetime.now().date().strftime('%Y%m%d')+'.log'
        logging.basicConfig(filename=os.path.join(path,self.LOG_PATH,log_file),
                            level='INFO',
                            format='%(asctime)s [%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %I:%M:%S %p'
                            )
        if hasattr(logging,level):
            func = getattr(logging,level)
            func(msg)
        else:
            print('错误的日志级别')
            exit()
            # logging.debug('[')
            # logging.debug('debug inf')
            # logging.info('info log…')
            # logging.warning("user [alex] attempted wrong password more than 3 times")
            # logging.error('err inf')
            # logging.critical("server is down")
        return msg




if __name__ == "__main__":
    HOST = Host_Manage()