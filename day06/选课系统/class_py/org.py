# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
from class_py import db,role



class Course(object):
    '''课程类'''
    def __init__(self,db_obj,school_name='',course_neme =''):
        '''
        课程构造类，参数为空则创建课程，非空查找数据库并实例化类
        :param db_obj: 关联数据库对象
        :param school_neme: 开设此课程的学校名称，对应school_list索引列表
        :param course_neme: 课程名
        '''
        self.DB_obj = db_obj
        course_list = self.DB_obj.DB_Index['course_list']
        school_list = self.DB_obj.DB_Index['school_list']
        if school_name == '' or course_neme == '':
            #关联学校并创建课程
            self.Relation_School()
        elif course_neme in course_list and school_name in school_list:
            course_info = self.DB_obj.GET_DATA('select %s from course'%course_neme)
            self.name = course_info['name']#课程名称
            self.price = course_info['price']#课程价格
            self.school = course_info['school']#开设此课程的学校
            self.cycle = course_info['cycle']#课程学习周期，以周为单位
            self.title = course_info['title']#课程简介
            self.Relation_School(self.school)
        else:
            print('暂未开设【%s】课程或学校名称错误，创建课程对象失败！'%course_neme)
            exit()

    def Relation_School(self,school_name=''):
        '''课程关联学校'''
        if school_name == '':
            print('学校列表'.center(40, '-'))
            for item in self.DB_obj.DB_Index['school_list']:
                print(self.DB_obj.DB_Index['school_list'].index(item), '.', item)
            while True:
                act = input('请选择要创建课程的学校：').strip()
                if act.isdigit() and int(act) < len(self.DB_obj.DB_Index['school_list']):
                    # 关联学校对象
                    self.School_obj = School(self.DB_obj, self.DB_obj.DB_Index['school_list'][int(act)])
                    self.Create()  # 创建课程
                    break

        else:
            self.School_obj = School(self.DB_obj, school_name)


    def Create(self):
        course_list = self.DB_obj.DB_Index['course_list']
        while True:
            self.name = input('请输入要创建的课程名称：')
            full_course_name = '%s_%s'%(self.School_obj.name,self.name)
            if full_course_name in course_list:
                print('此课程已经被创建，请不要重复创建！')
                print('已开设的课程列表'.center(40,'-'))
                print(course_list)
                continue
            self.price = input('请输入课程【%s】的价格：'%self.name)
            if self.price.isdigit():
                self.price = int(self.price)
            else:
                print('课程价格必须为整数！')
                continue
            self.school = self.School_obj.name
            self.cycle = input('请输入课程【%s】的学习周期（以周为单位）：'%self.name)  # 课程学习周期，以周为单位
            #print(type(self.cycle))
            if self.cycle.isdigit():
                self.cycle = int(self.cycle)
            else:
                print('课程周期必须为整数！')
                continue
            self.title = input('请输入课程【%s】的简介：'%self.name)  # 课程简介
            course_info = {
                'name':self.name,
                'school':self.school,
                'price':self.price,
                'cycle':self.cycle,
                'title':self.title
            }
            break
        #添加索引
        self.DB_obj.DB_Index['course_list'].append(full_course_name)
        # 保存索引
        self.DB_obj.SAVE_DB_INDEX(data=['course', self.DB_obj.DB_Index['course_list']])
        # 写入数据库
        self.DB_obj.SAVE_TABLE_DATA(statement='update_file', data=['course', full_course_name, course_info])



class School_Class(object):
    '''班级类'''
    def __init__(self,db_obj,school_name='',class_name=''):
        '''
        班级类构造函数，class_name为空则新建班级，非空查找数据库中的班级并实例化
        班级名称规则：学校名_班级
        :param db_obj: 数据库对象
        :param school_oname: 关联的学校
        :param class_name: 班级编号
        '''
        self.DB_obj = db_obj
        print(self.DB_obj)
        full_class_name = '%s_%s'%(school_name,class_name)
        if school_name == '' or class_name == '':
            #关联学校并创建班级
            self.School_obj = self.Relation_School()
            self.Create()
        elif school_name in self.DB_obj.DB_Index['school_list'] and full_class_name in self.DB_obj.DB_Index['class_list']:
            class_info = self.DB_obj.GET_DATA('select %s from class'%full_class_name)
            self.Relation_School(school_name)
            self.name = class_info['name']#班级名称
            self.school = class_info['school']#关联学校
            self.course = class_info['course']#班级课程
            self.teacher = class_info['teacher']#班级讲师
        else:
            print('学校名或班级名错误，创建班级对象失败！')
            exit()



    def Create(self):
        while True:
            self.name = input("请输入班级名称（如101）：")
            full_class_name = '%s_%s' % (self.School_obj.name,self.name)
            if full_class_name in self.DB_obj.DB_Index['class_list']:
                print('此班级已被创建，请重新输入')
                continue
            else:
                self.DB_obj.DB_Index['class_list'].append(full_class_name)
                #关联课程
                self.Relation_Course()
                #关联班级讲师
                self.Relation_Teacher()
                class_info = {
                    'name':self.name,#班级名称
                    'school':self.School_obj.name,#关联学校
                    'course':self.Course_obj.name,#班级课程
                    'teacher':self.Teacher#班级讲师
                }
                #保存索引列表
                self.DB_obj.SAVE_DB_INDEX(data=['class',self.DB_obj.DB_Index['class_list']])
                # 写入数据库
                self.DB_obj.SAVE_TABLE_DATA(statement='update_file', data=['class', full_class_name, class_info])
                break


    def Relation_Course(self):
        '''
        关联课程
        :return:课程对象
        '''
        print('课程列表'.center(40,'-'))
        course_list = self.DB_obj.DB_Index['course_list']
        course_list_in_school = []
        for item in course_list:
            course_info = self.DB_obj.GET_DATA('select %s from course'%item)
            if course_info['school'] == self.school:
                course_list_in_school.append([item,course_info['school'],course_list.index(item)])
        i = 0
        for c in course_list_in_school:
            print(i,'.',c[0])
            i += 1
        while True:
            act = input('请选择此班级的课程：').strip()
            if act.isdigit() and int(act) < len(course_list) and int(act) >= 0:
                self.Course_obj = Course(self.DB_obj,course_list_in_school[int(act)][1],course_list_in_school[int(act)][0])
                break


    def Relation_Teacher(self):
        '''
        关联讲师
        :return:关联的讲师对象
        '''
        print('讲师列表'.center(40,'-'))
        teacher_list =[]
        role_list = self.DB_obj.DB_Index['role_list']
        for item in role_list:
            role_info = self.DB_obj.GET_DATA('select %s from role'%item)
            if role_info['type'] == 'teacher' and role_info['school'] == self.School_obj.name:
                teacher_list.append([item,role_list.index(item)])
        for t in teacher_list:
            print(teacher_list.index(t),'.',t[0])
        while True:
            act = input('请选择此班级的讲师：').strip()
            if act.isdigit() and int(act) < len(teacher_list) and int(act) >= 0:
                self.Teacher = teacher_list[int(act)][0]
                break


    def Relation_School(self,school_name=''):
        '''
        关联学校
        :param school_name:此班级对象要关联的学校名称
        :return:返回关联的学校对象
        '''
        if school_name =='':
            print('学校列表'.center(40,'-'))
            for item in self.DB_obj.DB_Index['school_list']:
                print(self.DB_obj.DB_Index['school_list'].index(item),'.',item)
            while True:
                act = input('请选择要创建班级的学校：').strip()
                if act.isdigit() and int(act) < len(self.DB_obj.DB_Index['school_list']):
                    #关联学校对象
                    school = School(self.DB_obj, self.DB_obj.DB_Index['school_list'][int(act)])
                    self.school_obj = school
                    self.school = school.name
                    #self.Create()#创建班级
                    break
                else:
                    print('错误的选择！')
                    continue
        else:
            school = School(self.DB_obj,school_name)
        return school


    @staticmethod
    def Class_List(db_obj):
        '''
        班级的静态方法，返回班级列表
        :param db_obj:数据库对象
        :return: 返回班级对象列表
        '''
        class_list = db_obj.DB_Index['class_list']
        class_obj_list = []
        for c in class_list:
            #查询班级信息
            class_info = db_obj.GET_DATA('select %s from class'%c)
            #创建班级对象
            school_class = School_Class(db_obj,class_list['school'],class_info['name'])
            #构建对象列表
            class_obj_list.append(school_class)
        return class_obj_list





class School(object):
    '''学校类'''
    def __init__(self,db_obj,school_name=''):
        '''
        创建学校对象,school_name为空则新建学校，非空则查找数据库中学校并实例化
        :param db_obj: 数据库对象
        :param school_name: 学校名称
        '''
        self.DB_obj = db_obj#关联数据库对象
        if school_name == '':
            self.Create()
        elif school_name in self.DB_obj.DB_Index['school_list']:
            #如果学校名称在索引内
            school_info = self.DB_obj.GET_DATA('select %s from school'%school_name)
            self.name = school_info['name']
            self.address = school_info['address']
            self.teacher_list = school_info['teacher_list']
        else:
            print('学校名称错误，实例创建失败！')
            exit()



    def Create(self):
        while True:
            self.name = input('请输入学校名称：')
            self.address = input('请输入学校地址：')
            self.teacher_list = []
            if self.name in self.DB_obj.DB_Index['school_list']:
                print('该学校已被创建！')
                print('以下学校已创建：',self.DB_obj.DB_Index['school_list'])
                continue
            else:
                school_info = {
                    'name':self.name,
                    'address':self.address,
                    'teacher_list':self.teacher_list
                }
                #保存索引
                self.DB_obj.DB_Index['school_list'].append(self.name)
                self.DB_obj.SAVE_DB_INDEX(data=['school',self.DB_obj.DB_Index['school_list']])
                #写入数据库
                self.DB_obj.SAVE_TABLE_DATA(statement='update_file',data=['school',self.name,school_info])
                break

    @staticmethod
    def Relation(db_obj):
        '''
        静态学校方法
        :param db_obj: 数据库对象
        :return: 关联的学校对象
        '''

        school_list = db_obj.DB_Index['school_list']
        for school in school_list:
            print(school_list.index(school),'.',school)
        while True:
            act = input('请选择要关联的学校：').strip()
            if act.isdigit() and int(act) < len(school_list) and int(act) >=0:
                school = School(db_obj,school_list[int(act)])
                break
            else:
                print('选择错误！')
                continue
        return school



if __name__ == '__main__':
    DB_Data = db.DB_CLASS()  # 创建数据库对象


    # s = School(DB_Data,'北京校区')
    # print('address:',s.address)
    # s_c =School_Class(DB_Data)
    # print(s_c.School_obj)
    # print(s_c.DB_obj.DB_Index)
    #a = DB_Data.GET_DATA('select * from school')
    # r_s = School.Relation(DB_Data)
    # print(r_s)
    # DB_Data.DB_Index['school_list'].append('北京校区')
    # DB_Data.SAVE_DB_INDEX(data=['school', DB_Data.DB_Index['school_list']])
    #print(a)
    #print(DB_Data.DB_Index)
    #course =Course(DB_Data)