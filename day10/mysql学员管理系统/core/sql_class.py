# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from sqlalchemy import Column,String,create_engine,Integer,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

import configparser


class DB_Control(object):
    def __init__(self):
        self.Get_Conf()
        #self.Conn()
        self.Tables = self.Table_Framework()
        self.Create_Default_Data()

    def Conn(self):
        conn_str = '%s+pymysql://%s:%s@%s/%s?charset=utf8'%(self.DB_TYPE,self.DB_USER,self.DB_PWD,self.DB_HOST,self.DB_NAME)
        self.Engine = create_engine(
            conn_str,
            encoding='utf8',
            #echo=True
        )
        DB_BASE = declarative_base()
        Session_Class = sessionmaker(bind=self.Engine)
        self.Session = Session_Class()
        return DB_BASE

    def Get_Conf(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(path,'conf','config.ini'))
        self.DB_TYPE = config['DB']['type']
        self.DB_HOST = config['DB']['host']
        self.DB_USER = config['DB']['user']
        self.DB_PWD = config['DB']['pwd']
        self.DB_NAME = config['DB']['db_name']

    def Table_Framework(self):
        Base = self.Conn()
        class User(Base):
            __tablename__ = 'user'
            id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
            name = Column(String(32), nullable=False)
            pwd = Column(String(32), nullable=False)
            type_id = Column(Integer, ForeignKey('role_type.id'))
            type = relationship('Role_Type', backref='user')
            qq = Column(String(32))
            email = Column(String(32))
            #study_record = relationship('Study_Record', secondary=Study_Record, backref='study_record')

            def __repr__(self):
                return '<User>name=%s,type=%s' % (self.name, self.type.name)


        class User_Course(Base):
            __tablename__ = 'user_course'
            id = Column(Integer, primary_key=True, autoincrement=True)
            user_id = Column(Integer, ForeignKey('user.id'))
            user = relationship('User', backref='student_courses')
            course_id = Column(Integer, ForeignKey('course.id'))
            course = relationship('Course',backref='user',foreign_keys=[course_id])
            pay_status = Column(String(32))

            def __repr__(self):
                return '<user_course>user:%s,course:%s'%(self.user.name,self.course.name)


        class Role_Type(Base):
            __tablename__ = 'role_type'
            id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
            name = Column(String(8), nullable=False)

            def __repr__(self):
                return '<role_type>%s:%s'%(self.id,self.name)


        class Course(Base):
            __tablename__ = 'course'
            id = Column(Integer, primary_key=True)
            name = Column(String(32), nullable=False)
            teacher_id = Column(Integer, ForeignKey('user.id'))
            teacher = relationship('User',backref='teacher_courses')
            school_id = Column(Integer, ForeignKey('school.id'))
            school = relationship('School',backref='courses')
            price = Column(Integer,nullable=False)

            def __repr__(self):
                return '<Course>%s,讲师:%s校区:%s'%(self.name,self.teacher.name,self.school.name)

        class S_Class(Base):
            __tablename__ = 's_class'
            id =Column(Integer,primary_key=True)
            name = Column(String(32),nullable=False)
            course_id = Column(Integer,ForeignKey('course.id'))
            course = relationship('Course',backref='class')
            def __repr__(self):
                return '<Class>%s[%s]'%(self.name,self.course.name)

        class Class_Students(Base):
            #班级的学生
            __tablename__ = 'class_students'
            id = Column(Integer,primary_key=True,autoincrement=True)
            class_id = Column(Integer,ForeignKey('s_class.id'))
            s_class = relationship('S_Class',backref='student')
            user_id = Column(Integer,ForeignKey('user.id'))
            student = relationship('User',backref='in_class')
            def __repr__(self):
                return '<Class_Students>姓名：%s[课程：%s-%s]'%(self.student.name,self.s_class.name,self.s_class.course.name)


        class School(Base):
            __tablename__ = 'school'
            id = Column(Integer, primary_key=True)
            name = Column(String(32), nullable=False)
            address = Column(String(32), nullable=False)
            def __repr__(self):
                return '<School>%s[%s]'%(self.name,self.address)

        class Class_Record(Base):
            #教师开课记录
            __tablename__ = 'class_record'
            id = Column(Integer,primary_key=True,autoincrement=True)
            day = Column(Integer,nullable=False)
            class_id = Column(Integer,ForeignKey('s_class.id'))
            s_class = relationship('S_Class',backref='record')
            #study_record = relationship('Study_Record',secondary=Study_Record,backref='course_record')
            def __repr__(self):
                res = '【开课记录】%s(第%d天)'%(self.s_class.name,self.day)
                return res

        class Study_Record(Base):
            #对应教师开课的学习记录
            __tablename__ = 'study_record'
            id = Column(Integer,primary_key=True,autoincrement=True)
            class_record_id = Column(Integer,ForeignKey('class_record.id'))
            class_record = relationship('Class_Record',backref='study_record')
            student_id = Column(Integer,ForeignKey('user.id'))
            student = relationship('User',backref='study_record')
            task_url = Column(String(40))
            score = Column(Integer,nullable=False,default=0)
            def __repr__(self):
                res = '<study_record>%s在%s'%(self.student.name,self.class_record.s_class.name)
                res += '#第%d天课程#'%self.class_record.day
                if self.score == 0:
                    res += '[作业未提交]'
                else:
                    res += '[%d分]' % self.score
                return res


        Base.metadata.create_all(self.Engine)
        table_dict = {
            'user':User,
            'user_courses':User_Course,
            'role_type':Role_Type,
            'course':Course,
            'class':S_Class,
            'class_students':Class_Students,
            'school':School,
            'class_record':Class_Record,
            'study_record':Study_Record
        }
        #返回表结构对象字典
        return table_dict

    def Create_Default_Data(self):
        #检查并创建用户类型表数据
        table = self.Tables['role_type']
        type_obj = self.Session.query(table).all()
        #print(type_obj)
        if len(type_obj) == 0:
            type1 = table(name='student')
            type2 = table(name='teacher')
            type3 = table(name='admin')
            self.Session.add_all([type1,type2,type3])
            self.Session.commit()

    def Fields(self,table_name):
        '''
        根据表名返回字段
        :param table_name:
        :return:
        '''
        pass



    def Search_Data(self):
        #getattr(self.Table_Framework)
        #data = self.Session.query(table)

        pass



if __name__ == '__main__':
    db = DB_Control()
    print(db.Tables)
    table = db.Tables['role_type']
    #db.Create_Tables()
    print(table.__dict__.keys())
    #data = db.Session.query(table).filter(table.id <5 ).all()
    #print(data)

