#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column,Enum,Integer,String,DATE, ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType
import datetime
Base = declarative_base()

#堡垒机用户与绑定后的主机多对多关联
user_m2m_bindhost = Table('user_m2m_bindhost', Base.metadata,
                        Column('userprofile_id', Integer, ForeignKey('user_profile.id')),
                        Column('bindhost_id', Integer, ForeignKey('bind_host.id')),
                        )

#绑定后的主机与组的多对多关联表
bindhost_m2m_hostgroup = Table('bindhost_m2m_hostgroup', Base.metadata,
                          Column('bindhost_id', Integer, ForeignKey('bind_host.id')),
                          Column('hostgroup_id', Integer, ForeignKey('host_group.id')),
                          )

#堡垒机用户与组的多对多关联表，一个用户可以属于多个组，一个组里也可以有多个用户
user_m2m_hostgroup = Table('userprofile_m2m_hostgroup', Base.metadata,
                               Column('userprofile_id', Integer, ForeignKey('user_profile.id')),
                               Column('hostgroup_id', Integer, ForeignKey('host_group.id')),
                               )


class Host(Base):#主机表
    __tablename__ = 'host'
    id = Column(Integer,primary_key=True)
    hostname = Column(String(64),unique=True)
    ip = Column(String(64),unique=True)
    port = Column(Integer,default=22)

    def __repr__(self):
        return self.ip

class HostGroup(Base):#主机分组表
    __tablename__ = 'host_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    bind_hosts = relationship("BindHost",secondary="bindhost_m2m_hostgroup",backref="host_groups")#与bindHost通过第三张bindhost_m2m_hostgroup建立多对多的关联

    def __repr__(self):
        return self.name

class RemoteUser(Base):  #远程实际运行命令的用户表
    __tablename__ = 'remote_user'
    __table_args__ = (UniqueConstraint('auth_type', 'username','password', name='_user_passwd_uc'),)#三个字段联合唯一

    id = Column(Integer, primary_key=True)
    AuthTypes = [
        ('ssh-password','SSH/Password'),
        ('ssh-key','SSH/KEY'),
    ]
    auth_type = Column(ChoiceType(AuthTypes))#该字段只有列表里的两种值可选
    username = Column(String(32))
    password = Column(String(128))
    def __repr__(self):
        return "id=%s,auth_type=%s,user=%s,password=%s" %(self.id,self.auth_type,self.username,self.password)

class BindHost(Base):#主机和登陆主机的用户绑定表
    __tablename__ = "bind_host"
    __table_args__ = (UniqueConstraint('host_id','remoteuser_id', name='_host_remoteuser_uc'),)#host_id和remoteuser_id联合起来生成一个_host_remoteuser_uc的唯一字段

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer,ForeignKey('host.id'))
    remoteuser_id = Column(Integer, ForeignKey('remote_user.id'))
    host = relationship("Host",backref="bind_hosts")  #关联host表，并且Host可以通过bind_hosts字段反查
    remote_user = relationship("RemoteUser",backref="bind_hosts")#关联remote_user表
    def __repr__(self):
        return '%s 权限用户:%s'%(self.host.ip,self.remote_user.username)

class UserProfile(Base):#堡垒机上的用户信息表
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True)
    username = Column(String(32),unique=True)
    password = Column(String(128))
    bind_hosts = relationship("BindHost", secondary='user_m2m_bindhost',backref="user_profiles")#通过第三张表与bindHost表建立关联
    host_groups = relationship("HostGroup",secondary="userprofile_m2m_hostgroup",backref="user_profiles")#通过第三张表与host_group表建立关联

    def __repr__(self):
        return self.username

class AuditLog(Base): #用户操作命令记录
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('user_profile.id')) #堡垒机上的用户ID
    host_id = Column(Integer,ForeignKey('host.id'))  #操作对应的主机ID
    cmd = Column(String(128))               #操作的命令
    date_time = Column(String(128),default=str(datetime.datetime.now()))         #操作的时间
    user = relationship('UserProfile',backref='audit_log')
    host = relationship('Host',backref='audit_log')

    def __repr__(self):
        return self.user.username,self.host.ip,self.cmd,self.date_time