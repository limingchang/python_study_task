# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys,os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,path)
from class_py import db,role

# d1 = db.DB_CLASS()
# print(d1.Role_List)
class ROLE_INTERFACE(object):
    '''
    角色接口集中处理类
    '''
    def __init__(self,role_type):
        self.DB_Data = db.DB_CLASS()#创建数据库对象
        self.DB_Index = self.DB_Data.DB_Index#获取角色索引
        if role_type == 'student':
            self.Role = role.Student(self.DB_Data)  # 创建学生对象
            self.student_view()
        elif role_type == 'teacher':
            self.Role = role.Teacher(self.DB_Data)#创建教师对象
            self.teacher_view()
        elif role_type == 'admin':
            self.Role= role.Admin(self.DB_Data)#创建管理员对象
            self.admin_view()
        else:
            print('\033[1;31;1mRoleTypeError!\033[0m')


    def Student_Action(self,act):
        if act == 'enroll':
            self.Role.Enroll()
        elif act == 'chose_class':
            self.Role.Chose_class()
        elif act == 'payment':
            self.Role.Payment()
        else:
            print('参数错误：role_student 参数错误！')
        self.student_view()


    def Teacher_action(self,act,class_obj):
        #获取班级学生列表
        student_list = self.Role.Student_List(class_obj)
        #print(student_list)
        if len(student_list) == 0:
            print('很遗憾，还没有学生选择您的班级和课程！')
        else:
            if act == 'class_chose':
                print('您开始给【%s】上课...'%class_obj.name)
            elif act == 'student_list':
                print('学生列表'.center(40, '-'))
                for student in student_list:
                    print(student['username'])
            elif act == 'score_manage':
                print('学生列表'.center(40,'-'))
                for student in student_list:
                    print(student_list.index(student),'.',student['username'],'|成绩：',student['score'])
                while True:
                    act = input('请选择要修改成绩的学生：')
                    if act.isdigit() and int(act) < len(student_list) and int(act) >= 0:
                        student_name = student_list[int(act)]
                        self.Role.Score_Manage(student_name)
                        break
                    else:
                        print('错误的选择！')
                        continue
            else:
                print('参数错误：role_teacher 参数错误！')
        self.teacher_view()


    def Admin_action(self,act):
        if act == 'school_create':
            self.Role.School_Create()
        elif act == 'teacher_create':
            self.Role.Teacher_Create()
        elif act == 'course_create':
            self.Role.Course_Create()
        elif act == 'class_create':
            self.Role.Class_Create()
        else:
            print('参数错误：role_admin 参数错误！')
        self.admin_view()


    def act(self,view_list):
        act = input("请选择：")
        if act.isdigit() and int(act) < len(view_list):
            view_list[int(act)][0](view_list[int(act)][1])
        elif act.lower() == 'q':
            view_list[act]()
        else:
            print('\033[1;31;1m指令错误!\033[0m')

    def student_view(self):
        print("学员视图".center(45,'-'))
        print('''1.学员注册
2.选择班级/课程
3.交学费
q.退出系统''')
        view_list = {
            1:[self.Student_Action,('enroll')],
            2:[self.Student_Action,('chose_class')],
            3:[self.Student_Action,('payment')],
            "q":exit
        }
        self.act(view_list)


    def teacher_view(self):
        print("讲师视图".center(45, '-'))
        print('请选择班级以进行操作：')
        class_obj_list = self.Role.Class_List()
        if len(class_obj_list) == 0:
            print('您没有关联班级，请联系管理员在创建班级时关联您！')
        else:
            for obj in class_obj_list:
                print(class_obj_list.index(obj),'.',obj.name)
            while True:
                act = input('请选择：').strip()
                if act.isdigit() and int(act) < len(class_obj_list) and int(act) >= 0:
                    class_obj = class_obj_list[int(act)]
                    break
            print('[%s]的操作选项'.center(40,'-')%class_obj.name)
            print('''1.选择上课班级
2.学生列表
3.成绩管理
q.退出系统''')
            view_list = {
                1: 'class_chose',
                2: 'student_list',
                3: 'score_manage',
                "q": exit
            }
            act = input("请选择：")
            if act.isdigit() and int(act) < len(view_list):
                self.Teacher_action(view_list[int(act)],class_obj)
            elif act.lower() == 'q':
                view_list[act]()
            else:
                print('\033[1;31;1m指令错误!\033[0m')


    def admin_view(self):
        print("管理视图".center(45, '-'))
        print('''1.创建讲师
2.创建学校
3.创建课程
4.创建班级
q.退出系统''')
        view_list = {
            1: [self.Admin_action,('teacher_create')],
            2: [self.Admin_action,('school_create')],
            3: [self.Admin_action,('course_create')],
            4: [self.Admin_action,('class_create')],
            "q": exit
        }
        self.act(view_list)





