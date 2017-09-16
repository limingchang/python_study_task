# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import hashlib

from core import sql_class

class View_Interface(object):
    def __init__(self):
        self.Is_Login = False
        self.DB = sql_class.DB_Control()
        self.Menu()
        #self.Get_Role_Type()
        self.Menu_For_Type()


    def Menu_For_Type(self):
        role_type = self.Login_User.type.name
        menu_dict = {
            'student':self.Menu_Student,
            'teacher':self.Menu_Teacher,
            'admin':self.Menu_Admin
        }
        if role_type in menu_dict:
            menu_dict[role_type]()
        else:
            print('角色类型错误！程序关闭！')
            exit()

    def Menu_Student(self):
        '''
        if self.Is_Login:
            print('未登录无权操作！')
            exit()
        menu_list = ['1.提交作业','2.查看成绩','3.成绩排名']
        menu_dict = {
            '1.提交作业':,
            '2.查看成绩':,
            '3.成绩排名':
        }
        while True:
            print(('学员【%s】主页'%self.Login_User.name).center(50,'-'))
            for menu in menu_list:
                print(menu)
            act = input('请选择(q退出登录)：')
            if act.isdigit() and int(act) <= len(menu_list) and int(act) > 0:
                func = menu_dict[menu_list[int(act)-1]]
                func()
            elif act == 'q':
                self.Is_Login = False
                self.Login_User = None
                break
            else:
                print('\033[1;32;1m选择错误！\033[0m')
                continue
        self.Menu()
        '''





    def Menu_Teacher(self):
        '''
        if self.Is_Login:
            print('未登录无权操作！')
            exit()

        menu_list = ['1.创建班级','2.开始上课','3.批改作业']
        menu_dict = {
            '1.创建班级':,
            '2.开始上课':,
            '3.批改作业':
        }
        while True:
            print(('教师【%s】工作台'%self.Login_User.name).center(50,'-'))
            for menu in menu_list:
                print(menu)
            act = input('请选择(q退出登录)：')
            if act.isdigit() and int(act) <= len(menu_list) and int(act) > 0:
                func = menu_dict[menu_list[int(act)-1]]
                func()
            elif act == 'q':
                self.Is_Login = False
                self.Login_User = None
                break
            else:
                print('\033[1;32;1m选择错误！\033[0m')
                continue
        self.Menu()
        '''

    def Menu_Admin(self):
        if self.Is_Login is False:
            print('未登录无权操作！')
            exit()
        menu_list = ['1.创建学校','2.创建课程','3.删除用户']
        menu_dict = {
            '1.创建学校':self.Create_School,
            '2.创建课程':self.Create_Course,#关联教师
            #'3.用户管理':
        }
        while True:
            print(('管理员【%s】工作台'%self.Login_User.name).center(50,'-'))
            for menu in menu_list:
                print(menu)
            act = input('请选择(q退出登录)：')
            if act.isdigit() and int(act) <= len(menu_list) and int(act) > 0:
                func = menu_dict[menu_list[int(act)-1]]
                func()
            elif act == 'q':
                self.Is_Login = False
                self.Login_User = None
                break
            else:
                print('\033[1;32;1m选择错误！\033[0m')
                continue
        self.Menu()




    def Login(self):
        while True:
            username = input('用户名:')
            password = input('密  码:')
            password = self.Create_Pwd(password)
            table = self.DB.Tables['user']
            user_obj = self.DB.Session.query(table).filter(table.name==username).filter(table.pwd==password).first()
            if user_obj is None:
                print('\033[1;32;1m认证失败！用户名或密码错误\033[0m')
                continue
            else:
                self.Is_Login = True
                self.Login_User = user_obj
                print('欢迎【%s】%s'%(user_obj.type.name,user_obj.name))
                break
        return self.Is_Login


    
    def Menu(self):
        menu_list = ['1.用户登录','2.注册用户']
        menu_dict = {
            '1.用户登录':self.Login,
            '2.注册用户':self.Register
        }     
        while True:
            print('学员管理系统'.center(50,'-'))
            for menu in menu_list:
                print(menu)
            act = input('请选择(q退出)：')
            if act.isdigit() and int(act) <=len(menu_list) and len(menu_list)>0:
                func = menu_dict[menu_list[int(act)-1]]
                func()
                break
            elif act.strip() == 'q':
                exit()
            else:
                print('选择错误！')
                continue



    def Register(self):
        table = self.DB.Tables['user']
        user_info = {
            'name':'',
            'pwd':'',
            'qq':'',
            'email':''
        }
        while True:
            print('注册用户'.center(50,'-'))
            if user_info['name'] == '':
                username = input('请输入用户名：')
                user_obj = self.DB.Session.query(table).filter(table.name==username).first()
                #table.
                if user_obj is not None:
                    print('用户名已存在，请重新输入！')
                    continue
                else:
                    user_info['name'] = username
            else:
                password = input('请输入密码：')
                re_password = input('重复刚才密码：')
                if password != re_password:
                    print('两次密码不一致，请重新输入！')
                    continue
                else:
                    password = self.Create_Pwd(password)
                    user_info['pwd'] = password
                    qq = input('请输入QQ号码：').strip()
                    email = input('请输入您的邮箱：').strip()
                    user_info['qq'] = qq
                    user_info['email'] = email
                    break
        type_obj_dict = self.Get_Role_Type()
        new_user= table(name=user_info['name'],pwd=user_info['pwd'],qq=user_info['qq'],email=user_info['email'])
        while True:
            print('注册类型'.center(50,'-'))
            type_list = []
            count = 1
            for type_obj in type_obj_dict:
                if type_obj_dict[type_obj].name != 'admin':#不允许创建管理员
                    print(count,'.',type_obj_dict[type_obj].name)
                    type_list.append(type_obj_dict[type_obj].name)
                    count += 1
            act = input('请选择：').strip()
            if act.isdigit() and int(act) <= len(type_list) and int(act) > 0:
                #----判断管理员，只能由管理员创建
                new_user.type = type_obj_dict[type_list[int(act)-1]]
                break
            else:
                print('选择错误！')
                continue
        self.DB.Session.add(new_user)
        self.DB.Session.commit()



    def Create_Pwd(self,pwd):
        #sha1密码
        return hashlib.md5(pwd.encode("utf8")).hexdigest()
        
    




    def Create_School(self):
        #创建学校
        while True:
            print('创建学校'.center(50,'-'))
            name = input('请输入学校名称：')
            address = input('请输入学校地址：')
            table = self.DB.Tables['school']
            school_obj = self.DB.Session.query(table).filter(table.name == name).first()
            if  school_obj is None:
                new_school = table(name=name,address=address)
                self.DB.Session.add(new_school)
                self.DB.Session.commit()
                print('学校【%s】创建成功！'%new_school.name)
                break
            else:
                print('学校[%s]已被创建，地址：%s'%(school_obj.name,school_obj.address))
                continue   

    def Create_Course(self):
        #创建课程
        while True:
            print('创建课程'.center(50,'-'))
            name = input('请输入课程名称：')
            course_table = self.DB.Tables['course']
            school_list = []
            school_table = self.DB.Tables['school']
            school_list_obj = self.DB.Session.query(school_table).all()
            print(school_list_obj)
            



    def Get_Role_Type(self):
        #返回角色类型字典
        table = self.DB.Tables['role_type']
        type_obj = self.DB.Session.query(table).all()
        type_dict = {}
        for t in type_obj:
            type_dict[t.name]=t
        #print(type_dict)
        return type_dict



if __name__ =='__main__':
    view = View_Interface()