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
        self.Base = self.Conn()
        #self.Table_Framework()

    def Conn(self):
        self.Engine = create_engine(
            'mysql+pymysql://python_day10:123456@192.168.0.106/py_study_day10',
            encoding='utf8',
            echo=True
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


    #Base = self.Conn()
    class User(declarative_base()):
        __tablename__ = 'user'
        id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
        name = Column(String(32), nullable=False)
        pwd = Column(String(32), nullable=False)
        type_id = Column(Integer, ForeignKey('role_type.id'))
        type = relationship('Role_Type', backref='user_id')
        # type_id = relationship('Role_Tpye')
        # course_id = Column(Integer,ForeignKey('couesr.id'))
        qq = Column(String(32))
        email = Column(String(32))

        def __repr__(self):
            return '<User>name=%s,type=%s' % (self.name, self.type.name)

    class User_Course(declarative_base()):
        __tablename__ = 'user_course'
        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship('User', backref='courses', foreign_keys=[user_id])
        course_id = Column(Integer, ForeignKey('course.id'))
        course = relationship('Course',backref='user',foreign_keys=[course_id])
        pay_status = Column(String(32))



        def __repr__(self):
            return '<user_course>user:%s,course:%s'%(self.user.name,self.course.name)

    class Role_Type(declarative_base()):
        __tablename__ = 'role_type'
        id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        name = Column(String(8), nullable=False)

        def __repr__(self):
            return '<role_type>%s:%s'%(self.id,self.name)

    class Course(declarative_base()):
        __tablename__ = 'course'
        id = Column(Integer, primary_key=True)
        name = Column(String(32), nullable=False)
        teacher_id = Column(Integer, ForeignKey('user.id'))
        #teacher = relationship('User',backref='')
        school_id = Column(Integer, ForeignKey('school.id'))

    class School(declarative_base()):
        __tablename__ = 'school'
        id = Column(Integer, primary_key=True)
        name = Column(String(32), nullable=False)
        address = Column(String(32), nullable=False)

    def Creat_Tables(self):
        Base = declarative_base()
        Base.metadata.create_all(self.Engine)


    def Search_Data(self):
        table = getattr(self,'Role_Type')
        print(table)
        data = self.Session.query(table).filter(table.id <5 ).all()
        print(data)


if __name__ == '__main__':
    db = DB_Control()
    table = db.Role_Type()
    data = db.Session.query(table).filter(table.id < 5).all()

