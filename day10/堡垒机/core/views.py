#!/usr/bin/env python
# -*- coding:utf-8 -*-

from conf.db_conn import session
from core.database_table import *
from demos import demo

def auth():
    '''认证登陆'''
    count = 0
    while count<3:
        username = input('用户名:').strip()
        if len(username) ==0:
            continue
        passwd = input('密码:').strip()
        if len(passwd) ==0:
            continue
        u_obj = session.query(UserProfile).filter_by(username=username).filter_by(password=passwd).first()
        if u_obj:
            return u_obj
        else:
            print('输入的用户或密码错误,还剩%s输入机会'%(3-count-1))
        count +=1
    print('已经超过错误次数')

def cmd_interactive():
    user = auth()
    if user:
        while True:
            print('可登陆的主机如下'.center(50,'-'))
            print('未分组主机:')
            for h in user.bind_hosts:
                print(h)
            print('已分组主机:')
            for h_g in user.host_groups:#用户绑定的主机组
                print(h_g)
                for i in h_g.bind_hosts:
                    print(i)
            choise_ip = input('请输入要连接的主机IP:').strip()
            choise_user = input('请输入要登陆这台主机的权限用户:').strip()
            h_obj = session.query(Host).filter_by(ip=choise_ip).first()#找到输入IP的主机，IP是唯一的
            r_u_obj = session.query(RemoteUser).filter_by(username=choise_user).all()#找到输入用户名的所有帐户，用户名不是唯一
            #循环找到的用户名，根据主机ID和用户名ID，找到相对应的绑定主机
            bind_obj = False
            for r_u in r_u_obj:
                b_obj = session.query(BindHost).filter_by(host_id=h_obj.id).filter_by(remoteuser_id=r_u.id).first()
                if b_obj:
                    bind_obj = b_obj   #找到相对应的绑定主机
            if not bind_obj:
                print('输入错误，请输入正确的IP或权限用户')
                continue
            #判断绑定的主机在不在这个用户的未分组和分组机器里面
            flag = False
            if bind_obj in user.bind_hosts:#如果用户绑定的主机里有这个绑定主机
                flag = True
            if not flag:
                for h_g in user.host_groups:
                    if bind_obj in h_g.bind_hosts:#如果用户所属的组里有这个绑定主机
                        flag = True
            if flag: #执行远程SSH连接
                r_user_obj = session.query(RemoteUser).filter_by(id=bind_obj.remoteuser_id).first()#找到连接使用的用户和密码
                demo.conn_host(user.id,h_obj.id,h_obj.ip,h_obj.port,r_user_obj.username,r_user_obj.password,r_user_obj.auth_type)
                #传入堡垒机用户id，远程主机id,主机IP，端口，SSH连接的用户密码和认证类型
            else:
                print('你没有这个权限')
