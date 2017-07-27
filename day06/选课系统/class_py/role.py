# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os
import pickle

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from class_py import org,db

class SchoolMember(object):
    def __init__(self,db_obj):
        self.DB_obj = db_obj#关联数据库对象
        self.Is_Login = False #设置登录状态

    def Auth(self):
        '''
        验证登录
        :param db_obj: 数据库对象
        :return:bool
        '''
        if self.Is_Login == True:
            res = True
        else:
            flag = False
            count = 0
            res = False
            while not flag:
                username = input('请输入用户名：')
                if username not in self.DB_obj.DB_Index['role_list']:
                    print('查无此用户！')
                    continue
                else:
                    user_info = self.DB_obj.GET_DATA('select %s from role'%username)
                if user_info['locked'] == True:
                    print('账户[%s]已被锁定，请联系管理员！'%username)
                    res = False
                    flag = True
                    continue
                else:
                    while True:
                        password = input('请输入[%s]的密码：'%username)
                        if user_info['password'] != password:
                            res = False
                            print('密码错误！三次后将锁定账户！')
                            count +=1
                            if count == 3:
                                print('密码错误次数过多[%s]已被锁定！' % username)
                                user_info['locked'] = True
                                #写入用户信息
                                self.DB_obj.SAVE_TABLE_DATA(statement='update_file',data=['role',username,user_info])
                                flag = True
                                break
                            continue
                        else:
                            self.Is_Login = True
                            self.User_Info = user_info
                            flag = True
                            res = True
                            break
        return res


    def enroll(self):
        '''
        成员注册
        :return: member_info
        '''
        role_list = self.DB_obj.DB_Index['role_list']#角色索引列表
        self.UserName = ''
        self.PassWord = ''
        while True:
            if self.UserName == '':
                self.UserName = input('请输入用户名：')
                if self.UserName in role_list:
                    print('此用户已被注册！')
                    self.UserName = ''
                    continue
                else:
                    self.ID = len(role_list)
                    role_list.append(self.UserName)
            else:
                self.PassWord = input('请输入密码：')
                re_pwd = input('请再次输入以确认密码：')
                if re_pwd != self.PassWord:
                    print('两次输入密码不一致，请重新输入！')
                else:
                    break



class Teacher(SchoolMember):
    '''
        讲师类，继承学校成员。
        '''

    def __init__(self, db_obj,type=''):
        '''
        讲师构造函数
        :param db_obj:
        :param type:是否是新注册，新注册不需要验证登录
        '''
        super(Teacher, self).__init__(db_obj)
        # super(class_name,self).__init__(name,age) #新式类写法
        if type != 'enroll':
            self.Login()



    def Login(self):
        if not self.Auth():  # 创建实例立即验证登录
            print('登录验证失败！')
            exit()
        elif self.User_Info['type'] != 'teacher':
            print('登录类型错误！')
            exit()
        else:
            print('欢迎讲师【%s】...'%self.User_Info['username'])



    def enroll(self):
        SchoolMember.enroll(self)
        print('完善个人信息'.center(40,'-'))
        info = {
            'username': self.UserName,
            'password': self.PassWord,
            'admin':False,
            'locked': False,  # 设置锁定状态
        }
        self.Type = 'teacher'
        info['type'] = self.Type
        school_obj = org.School.Relation(self.DB_obj)
        self.school = school_obj.name
        info['school'] = self.school
        #写入索引
        self.DB_obj.SAVE_DB_INDEX(data=['role', self.DB_obj.DB_Index['role_list']])
        # 写入数据库
        self.DB_obj.SAVE_TABLE_DATA(statement='update_file', data=['role', self.UserName, info])



    def Class_List(self):
        '''
        获取该教师实例的班级列表
        :return: 返回班级对象列表
        '''
        self.Auth()#验证登录
        class_list = self.DB_obj.DB_Index['class_list']
        teacher_class_list = []
        for item in class_list:
            class_info = self.DB_obj.GET_DATA('select %s from class'%item)
            if class_info['teacher'] == self.User_Info['username']:
                #创建班级对象
                class_obj = org.School_Class(self.DB_obj,class_info['school'],class_info['name'])
                teacher_class_list.append(class_obj)
        return teacher_class_list


    def Student_List(self,class_obj):
        '''
        获取班级内学生列表
        :param class_obj: 班级对象
        :return: 返回学生对象列表
        '''
        self.Auth()  # 验证登录
        role_list = self.DB_obj.DB_Index['role_list']
        student_list = []#所有学生列表
        for student in role_list:
            student_info = self.DB_obj.GET_DATA('select %s from role'%student)
            if student_info['type'] == 'student' and class_obj.name in student['class_list']:
                student_list.append(student_info)
        return student_list


    def Score_Manage(self,student_name):
        '''
        修改学生成绩
        :param cstudent_name: 学生用户名
        :return: 返回修改后信息
        '''
        self.Auth()  # 验证登录
        student_info = self.DB_obj.GET_DATA('select %s from role'%student_name)
        print('【%s】班-【%s】当前成绩：%s'%(student_info['class'],student_info['username'],student_info['score']))
        while True:
            new_score = input('请输入新的成绩：')
            if new_score.isdigit() and int(new_score) <= 100 and int(new_score) >=0:
                student_info['score'] = int(new_score)
                # 写入数据库.
                res = self.DB_obj.SAVE_TABLE_DATA(statement='update_file', data=['role', student_info['name'], student_info])
                if res:
                    print('【%s】的成绩修改为：%s'%(student_name,new_score))
                break
            else:
                print('成绩格式错误，请重新输入！')
                continue




class Admin(SchoolMember):
    '''
    管理员类，继承学校成员。
    '''
    def __init__(self,db_obj):
        super(Admin,self).__init__(db_obj)
        # super(class_name,self).__init__(name,age) #新式类写法
        if not self.Auth():#创建实例立即验证登录
            print('登录验证失败')
            exit()
        elif self.User_Info['admin'] == False:
            print('您没有管理权限！')
            exit()
        else:
            print('欢迎管理员【%s】...'%self.User_Info['username'])


    def School_Create(self):
        '''
        创建学校
        :return:返回创建的学校对象
        '''
        school = org.School(self.DB_obj)#创建学校实例
        print('\033[1;32;1m【%s】创建成功\033[0m'%school.name)
        return school


    def Teacher_Create(self):
        '''
        创建教师
        :return:返回创建的教师对象
        '''
        teacher = Teacher(self.DB_obj,'enroll')
        teacher.enroll()
        print('\033[1;32;1m【%s】创建成功\033[0m' % teacher.username)
        return teacher

    def Course_Create(self):
        '''
        创建课程
        :return:课程对象
        '''
        course = org.Course(self.DB_obj)
        print('\033[1;32;1m【%s】创建成功\033[0m' % course.name)
        return course


    def Class_Create(self):
        '''
        创建班级
        :return:
        '''
        school_class = org.School_Class(self.DB_obj)
        print('\033[1;32;1m【%s】创建成功\033[0m' % school_class.name)
        return school_class



class Student(SchoolMember):
    def Enroll(self):
        SchoolMember.enroll(self)
        #print('完善个人信息'.center(40,'-'))
        info = {
            'username':self.UserName,
            'password':self.PassWord,
            'admin':False,
            'locked':False,#设置锁定状态
            'payment':False#设置未交费状态
        }
        self.Type = 'student'
        info['type'] = self.Type
        self.class_obj = ''#设置班级对象
        info['class'] =self.class_obj
        # 写入索引
        self.DB_obj.SAVE_DB_INDEX(data=['role', self.DB_obj.DB_Index['role_list']])
        # 写入数据库
        self.DB_obj.SAVE_TABLE_DATA(statement='update_file', data=['role', self.UserName, info])
        print('[%s]注册成功！'%self.UserName)


    def Chose_class(self):
        '''
        选择要学习的课程和班级
        :return:
        '''
        self.Auth()#验证登录
        class_obj_list = org.School_Class.Class_List(self.DB_obj)
        print('班级课程列表：'.center(40,'-'))
        for obj in class_obj_list:
            print(class_obj_list.index(obj),'.',obj.school,'|',obj.name,'|课程：',obj.course,'|讲师：',obj.teacher)
        while True:
            act = input('请选要学习的课程：').strip()
            if act.isdigit() and int(act) < len(class_obj_list) and int(act) >= 0:
                res = class_obj_list[int(act)]
                del class_obj_list#清空班级对象列表，释放内存
                break
            else:
                print('选择错误！')
                continue
        self.User_Info['class'] = res.name
        # 写入数据库
        self.DB_obj.SAVE_TABLE_DATA(statement='update_file', data=['role', self.UserName, self.User_Info])



    def Payment(self):
        '''
        缴费
        :return:成功返回True
        '''
        self.Auth()  # 验证登录
        res =False
        school_class = self.User_Info['class']
        #查询班级信息
        class_info = self.DB_obj.GET_DATA('select %s from class'%c)
        #获得缴费状态
        class_payment = self.User_Info['payment']
        if class_payment == False:
            print('课程【%s】=》（%s）,未缴费，是否缴费？')
            act = input('输入Y/N:')
            if act.strip().lower() == 'y':
                self.User_Info['payment'] = True
                print('缴费成功！')
                # 写入数据库
                self.DB_obj.SAVE_TABLE_DATA(statement='update_file', data=['role', self.UserName, self.User_Info])
                res = True
            else:
                print('您已取消缴费')
                res = False
        else:
            print('您的课程已缴费，不必在此缴费！')
            res = False
        return res



if __name__ == '__main__':
    DB_Data = db.DB_CLASS()  # 创建数据库对象
    # t = Teacher(DB_Data,'enroll')
    # t.enroll()
    # print(t)

    print(DB_Data.DB_Index)
    # info['admin'] = True
    # info['locked'] = False
    # DB_Data.SAVE_TABLE_DATA(statement='update_file',data=['role','admin',info])
    # info = DB_Data.GET_DATA('select admin from role')
    # DB_Data.DB_Index['course_list'] = ['上海校区_python', '北京校区_python']
    # DB_Data.DB_Index['class_list'] = [ '北京校区_第一期1班']
    # DB_Data.SAVE_DB_INDEX(data=['class',DB_Data.DB_Index['class_list']])
    info = DB_Data.GET_DATA('select * from class')
    print(info)