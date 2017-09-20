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
        self.Login_User = None
        self.DB = sql_class.DB_Control()
        self.Menu()
        #self.Get_Role_Type()
        #self.Menu_For_Type()


    def Menu_For_Type(self):
        if self.Login_User is None:
            self.Login()
        else:
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

        if self.Is_Login is False:
            print('未登录无权操作！')
            exit()
        menu_list = ['1.挑选课程','2.提交作业','3.查看成绩']
        menu_dict = {
            '1.挑选课程':self.Sel_Student_Course,
            '2.提交作业':self.Submit_Homework,
            '3.查看成绩':self.Show_Score
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






    def Menu_Teacher(self):
        
        if self.Is_Login is False:
            print('未登录无权操作！')
            exit()

        menu_list = ['1.创建班级','2.选择学员','3.开始上课','4.批改作业']
        menu_dict = {
            '1.创建班级':self.Create_Class,
            '2.选择学员':self.Choose_Student,
            '3.开始上课':self.Start_Class,
            '4.批改作业':self.Homework_Correcting
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
        

    def Menu_Admin(self):
        if self.Is_Login is False:
            print('未登录无权操作！')
            exit()
        menu_list = ['1.创建学校','2.创建课程','3.用户XX']
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
        self.Menu_For_Type()


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
        #self.Login()


    def Create_Pwd(self,pwd):
        #md5密码
        return hashlib.md5(pwd.encode("utf8")).hexdigest()


    def Sel_Student_Course(self):
        #学生选课
        choose = None
        table = self.DB.Tables['user_courses']
        course_table = self.DB.Tables['course']
        course_list = self.DB.Session.query(course_table).all()
        if len(course_list) == 0:
            print('8组导师好懒，还没创建课程哦！')
            choose = None
        else:
            while True:
                print('快挑选您喜欢的课程吧！'.center(50,'-'))
                count = 1
                for course in course_list:
                    print(count,'.',course.name,'[',course.teacher.name,']-',course.school.name)
                act = input('请选择：')
                if act.isdigit() and int(act) > 0 and int(act) <= len(course_list):
                    choose = course_list[int(act)-1]
                    student_course_table = self.DB.Tables['user_courses']
                    student_course_list = self.DB.Session.query(student_course_table).filter(student_course_table.user==self.Login_User).filter(student_course_table.course==choose).all()
                    #判断是否重复选课
                    if len(student_course_list) != 0:
                        print(choose,'\033[1;31;1m您已参加此课程，加油学习哦！\033[0m')
                        choose = None
                        continue
                    else:
                        break
                else:
                    print('选择错误！')
                    choose = None
                    continue
            new_sel_course = table(user=self.Login_User,course=choose)
            self.DB.Session.add(new_sel_course)
            self.DB.Session.commit()
        return choose

    def Submit_Homework(self):
        #提交作业
        table = self.DB.Tables['study_record']

        while True:
            empty_task_list = self.DB.Session.query(table).filter(table.student == self.Login_User).filter(table.task_url == None).all()
            if len(empty_task_list) == 0:
                print('\033[1;36;1m您没有需要提交的作业！\033[0m')
                break
            count = 1
            print('选择您要提交作业的上课记录'.center(50,'-'))
            for task in empty_task_list:
                print(count,'.',task.class_record.s_class.name,'第',task.class_record.day,'天','[',task.class_record.s_class.course.name,']')
                count += 1
            act = input('请选择：')
            if act.isdigit() and int(act) > 0 and int(act) <= len(empty_task_list):
                task_url = input('请输入您的作业链接：')
                empty_task_list[int(act)-1].task_url = task_url
                self.DB.Session.commit()
                print('\033[1;36;1m提交成功，继续提交或者q退出。\033[0m')
                continue
            elif act == 'q':
                break
            else:
                print('选择错误！')
                continue



    def Homework_Correcting(self):
        #批改作业
        pass

    def Show_Score(self):
        #查看成绩
        table = self.DB.Tables['study_record']
        your_score_list = self.DB.Session.query(table).filter(table.student==self.Login_User).all()
        for your_score in your_score_list:
            #print(your_score)
            all_score_list = self.DB.Session.query(table).filter(table.class_record==your_score.class_record).order_by(table.score.desc()).all()
            ranking = all_score_list.index(your_score) + 1
            #ranking = type(all_score_list)
            print(your_score,'班级排名：',ranking)




    def Choose_Student(self):
        '''
        教师选择学员
        :return:
        '''
        table = self.DB.Tables['user']
        type_table = self.DB.Tables['role_type']
        role_type = self.DB.Session.query(type_table).filter(type_table.name=='student')
        #student_list = self.DB.Session.query(table).filter(table.type==role_type)
        choose_class = self.Sel_Class()
        while True:
            if choose_class is None:
                break
            else:
                print('选择学生加入您的班级'.center(50,'-'))
                student_course_table = self.DB.Tables['user_courses']
                student_list = self.DB.Session.query(table).filter(table.type==self.Get_Role_Type()['student']).all()
                #.filter(table.student_courses.course==choose_class.course).all()
                your_student_list = []
                for student in student_list:
                    for course in student.student_courses:#查询个人课程列表
                        if course.course == choose_class.course:
                            your_student_list.append(student)
                #print(your_student_list)
                count = 1
                for your_student in your_student_list:
                    print(count,'.',your_student.name,'QQ:',your_student.qq)
                    count += 1
                act = input('请选择学生(q退出)：')
                #查询这个学生是否已选择
                if act.isdigit() and int(act) > 0 and int(act) <= len(your_student_list):
                    choose_student = your_student_list[int(act)-1]
                    class_student_table = self.DB.Tables['class_students']
                    in_class = self.DB.Session.query(class_student_table).filter(class_student_table.s_class==choose_class).filter(class_student_table.student==choose_student).all()
                    if len(in_class) == 0:
                        add_class_student = class_student_table(s_class=choose_class,student=choose_student)
                        self.DB.Session.add(add_class_student)
                        self.DB.Session.commit()
                        print('添加学员【%s】成功，请继续选择！'%choose_student.name)
                        continue
                    else:
                        print('学员【%s】已经在您班级里了，请选择其他人！'%choose_student.name)
                        continue
                elif act == 'q':
                    break
                else:
                    print('选择错误！')
                    continue


            


    def Create_Class(self):
        #创建班级
        res = False
        table = self.DB.Tables['class']
        print('请为班级选择课程')
        choose_course = self.Sel_Course()
        if choose_course is None:
            res = False
        else:
            class_name = input('请输入班级名称：')
            new_class = table(name=class_name,course=choose_course)
            self.DB.Session.add(new_class)
            self.DB.Session.commit()
            print('创建班级【%s-%s】成功'%(choose_course.name,class_name))
            res = True
        return res
    
    def Start_Class(self):
        #开始上课
        table = self.DB.Tables['class_record']
        choose_class = self.Sel_Class()
        record_list = self.DB.Session.query(table).filter(table.s_class==choose_class).all()
        if len(record_list) == 0:
            new_day = 1
        else:
            new_day = record_list[-1].day + 1
        new_record = table(day=new_day,s_class=choose_class)
        self.DB.Session.add(new_record)
        self.DB.Session.commit()
        print('%s【第%d天】开始上课...'%(choose_class,new_day))
        #为学员创建上课记录in table study_record
        table_students = self.DB.Tables['class_students']
        your_students_list = self.DB.Session.query(table_students).filter(table_students.s_class==choose_class)
        new_study_record = []
        for your_student in your_students_list:
            your_student_record = self.DB.Tables['study_record'](class_record=new_record,student=your_student.student)
            new_study_record.append(your_student_record)
        self.DB.Session.add_all(new_study_record)
        self.DB.Session.commit()

        return True



    def Sel_Class(self):
        #选择班级上课或者其他操作
        choose = None
        table_course = self.DB.Tables['course']
        table_class = self.DB.Tables['class']
        while True:
            print('选择班级继续操作'.center(50,'-'))
            class_obj_list = []
            course_list = self.DB.Session.query(table_course).filter(table_course.teacher==self.Login_User).all()
            for course_obj in course_list:
                temp_class = self.DB.Session.query(table_class).filter(table_class.course==course_obj).all()
                class_obj_list.extend(temp_class)
            count = 1
            if len(class_obj_list) == 0:
                print('您还没创建班级！')
                break
            for class_obj in class_obj_list:
                print(count,'.',class_obj.name,class_obj.course.name)
                count += 1
            act = input('请选择班级:')
            if act.isdigit() and int(act) <= len(class_obj_list) and int(act) > 0:
                choose = class_obj_list[int(act)-1]
                break
            else:
                print('选择错误！')
                continue
        return choose


    def Sel_Course(self):
        #选择班级的课程
        choose = None
        table = self.DB.Tables['course']
        course_list = self.DB.Session.query(table).filter(table.teacher==self.Login_User).all()
        while True:
            print('请选择课程'.center(50,'-'))
            count = 1
            if len(course_list) == 0:
                print('还没有创建课程，请联系管理员！')
                break
            for course_obj in course_list:
                print(count,'.',course_obj.name,course_obj.school.name)
                count += 1
            act = input('请选择课程:')
            if act.isdigit() and int(act) <= len(course_list) and int(act) > 0:
                choose = course_list[int(act)-1]
                break
            else:
                print('选择错误！')
                continue
        return choose



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
        print('创建课程'.center(50,'-'))
        name = input('请输入课程名称：')
        table = self.DB.Tables['course']
        choose_school = self.Sel_School()
        choose_teacher = self.Sel_Teacher()
        while True:
            price = input('请输入课程价格：')
            if price.isdigit():break
            else:
                print('价格必须是整数数字！')
                continue
        new_course = table(name=name,school=choose_school,teacher=choose_teacher,price=price)
        self.DB.Session.add(new_course)
        self.DB.Session.commit()


            
    def Sel_School(self):
        #选择学校，返回选择的学校ORM
        choose = None
        school_table = self.DB.Tables['school']
        school_list_obj = self.DB.Session.query(school_table).all()
        if len(school_list_obj) == 0:
            print('学校列表为空，不能为课程关联学校，请先创建！')
            self.Create_School()
        else:
            while True:
                print('选择学校'.center(50,'-'))
                count = 1
                for s_obj in school_list_obj:
                    print(count,'.',s_obj.name,s_obj.address)
                    count +=1
                act = input('请选择学校：')
                if act.isdigit() and int(act) >0 and int(act) <= len(school_list_obj):
                    choose = school_list_obj[int(act)-1]
                    break
                else:
                    print('选择错误！')
                    continue
        return choose

    
    def Sel_Teacher(self):
        #选择教师，返回选择的教师obj
        choose = None
        table = self.DB.Tables['user']
        teacher_list = self.DB.Session.query(table).filter(table.type==self.Get_Role_Type()['teacher']).all()
        if len(teacher_list) == 0:
            print('还没有老师注册哦,快去邀请8组猴哥啊~')
            print('由于您没有可选的老师，程序结束！')
            exit()
        while True:
            count = 1
            for teacher_obj in teacher_list:
                print(count,'.',teacher_obj.name)
            act = input('请选择讲师：')
            if act.isdigit() and int(act) >0 and int(act) <= len(teacher_list):
                choose = teacher_list[int(act)-1]
                break
            else:
                print('选择错误！')
                continue
        return choose







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