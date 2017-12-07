#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .import set
from core.database_table import *
engine = create_engine(set.ConnParams,encoding='utf-8')
SessionCls = sessionmaker(bind=engine)
session = SessionCls()

if len(engine.table_names()) >0:
    pass
else:#初始时创建的表和数据
    Base.metadata.create_all(engine) #创建表结构
    u_obj = UserProfile(username='alex',password='123456')
    r_obj1 =RemoteUser(auth_type='ssh-password',username='mysql',password='654321')
    r_obj2 =RemoteUser(auth_type='ssh-password',username='root',password='123456')
    h_obj1 = Host(hostname='10mysql',ip='10.0.2.34')
    h_obj2 = Host(hostname='test1',ip='192.168.3.22')
    h_obj3 = Host(hostname='test2',ip='172.33.24.55')
    hg_obj1 = HostGroup(name='北京组')
    hg_obj2 = HostGroup(name='上海组')
    session.add_all([u_obj,h_obj1,h_obj2,h_obj3,r_obj1,r_obj2,hg_obj1,hg_obj2])
    session.commit()
