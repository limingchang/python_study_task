# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
import pickle,threading

from core import ssh_class

class Host_Manage():
    '''
    主机管理系统接口
    '''
    def __init__(self,SSH_Manage_Obj):
        '''
        构造函数
        '''
        self.SSH = SSH_Manage_Obj
        self.DB_Name = self.SSH.DB_NAME
        #显示菜单
        group_name = self.Show_Menu()
        #获取主机组下的主机信息字典
        host_dict = self.Get_Host_Dict(group_name)


    def Show_Menu(self):
        '''
        显示菜单
        :return:返回选择的主机组名
        '''
        print('请选择主机群组'.center(50,'-'))
        self.Group_List = self.Get_Host_Group()
        if len(self.Group_List) == 0:
            print('机组数量为零，请创建机组继续...')
            self.Create_Group()
        else:
            count = 0
            for group_name in self.Group_List:
                print(count,'.',group_name)
            while True:
                act = input('请选择主机组：')
                if act.isdigit() and int(act) < len(self.Group_List):
                    break
                else:
                    print('选择错误！')
                    continue
            return self.Group_List[int(act)]


    def Show_Host_Menu(self,host_dict):
        '''
        主机管理菜单
        :param host_dict: 主机信息字典
        :return:
        '''
        menu_list = ['1.执行命令','2.上传/下载','3.新增主机','4.修改主机信息']
        menu_dict = {
            '1.执行命令':'Run_Command',
            '2.上传/下载':'FTP_File',
            '3.新增主机':'Add_Host',
            '4.修改主机信息':'Modify_Host'
        }
        for menu in menu_list:
            print(menu)
        while True:
            act = input('请选择：')
            if act.isdigit() and int(act)<len(menu_list):
                menu = menu_dict[menu_list[int(act)]]
            else:
                print('选择错误！')
                continue
        func = getattr(self,menu)
        func(host_dict)


    def Get_Host_Group(self):
        '''
        获取主机组
        :return: 返回主机组列表
        '''
        group_list = []
        filename = os.path.join(path,self.DB_Name,'group_list.dat')
        if os.path.isfile(filename):
            with open(filename,'rb') as f:
                group_list = pickle.load(f)
        else:
            with open(filename,'wb') as f:
                pickle.dump(group_list,f)
        return group_list



    def Get_Host_Dict(self,group_name):
        '''
        根据主机组名称返回机组字典
        :param group_name: 主机组名称
        :return: host_dict
        '''
        host_dict = {}
        filename = os.path.join(path,self.DB_Name,group_name+'.dat')
        if os.path.isfile(filename):
            with open(filename,'rb')as f:
                host_dict = pickle.load(f)
        else:
            print('机组信息数据丢失！')
        return host_dict


    def Create_Group(self):
        '''
        新建机组
        :return:
        '''
        group_name = input('请输入新机组名：')
        if group_name in self.Group_List:
            print('此机组名已被创建')
            group_name =''
        else:
            self.Group_List.append(group_name)
            filename = os.path.join(path, self.DB_Name, 'group_list.dat')
            with open(filename,'wb') as f:
                pickle.dump(self.Group_List,f)
            self.Create_Host(group_name)

    def Create_Host(self,group_name):
        '''
        向主机组group_name里添加主机信息
        :param group_name: 主机组名
        :return: 返回添加后此主机组中所有主机信息
        '''
        host_file = os.path.join(path,self.DB_Name,group_name+'.dat')
        host_dict ={}
        if os.path.isfile(host_file):
            with open(host_file,'rb') as f:
                host_dict = pickle.load(f)
        else:
            host_dict = {}
        flag = False
        while not flag:
            print('新增主机信息'.center(50, '-'))
            host_name = input('请输入主机名称：')
            if host_name in host_dict:
                print('此主机已被创建')
                continue
            ip = input('输入主机地址：')
            port = input('输入主机端口：')
            user = input('输入主机用户名：')
            pwd = input('输入主机密码：')
            host_dict[host_name] = {
                'ip':ip,
                'port':port,
                'user':user,
                'pwd':pwd
            }
            while True:
                act = input('是否继续创建主机(y/n)？').strip().lower()
                if act == 'y':
                    flag = False
                    break
                elif act == 'n':
                    flag = True
                    break
                else:
                    print('输入错误！')
                    continue
        # 写入数据
        with open(host_file, 'wb') as f:
            pickle.dump(host_dict,f)
        return host_dict



if __name__ == '__main__':
    ssh_obj = ssh_class.SSH_Manage()
    host_manage = Host_Manage(ssh_obj)
