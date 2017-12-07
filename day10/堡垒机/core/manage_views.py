#!/usr/bin/env python
# -*- coding:utf-8 -*-

from core.database_table import *
from conf.db_conn import session
# from pymysql.err import IntegrityError
from sqlalchemy.exc import IntegrityError
class  manage_view(object):
    "管理视图"
    def handler(self):
        while True:
            print("欢迎进入管理视图\n"
                  "add_user 添加堡垒机用户\n"
                  "add_remoteuser 添加远程连接的使用权限帐户\n"
                  "add_host 添加远程连接主机\n"
                  "add_hostgroup 添加主机组\n"
                  "add_bindhost 绑定主机和登陆帐户\n"
                  "add_u_m2m_bindhost 堡垒机用户关联绑定后的主机\n"
                  "add_bhost_m2m_hgroup 绑定后的主机关联主机组\n"
                  "add_user_m2m_group 堡垒机用户关联主机组\n"
                  "exit 退出管理系统")
            operate = input("\033[31;0m请输入进行操作的命令:\033[0m")
            if hasattr(self, operate):
                getattr(self, operate)()

    def exit(self):
        exit()

    def add_user(self):
        '''添加堡垒机用户'''
        while True:
            print('添加堡垒机用户'.center(50,'-'))
            username = input('请输入用户名:').strip()
            if username == 'b':
                break
            if len(username) == 0:continue
            passwd = input('请输入密码:').strip()
            passwd2 = input('请再次输入密码:').strip()
            if len(passwd2) == 0:continue
            if passwd == passwd2:
                u_obj = UserProfile(username=username,password=passwd)
                try:
                    session.add(u_obj)
                    session.commit()
                    print('添加完成')
                except IntegrityError:
                    session.rollback()   #如果上面的事务出错，这里要用到回滚，否则再次查询时会出错
                    print('\033[31;0m用户已存在\033[0m')
            else:
                print('两次密码不一致')
            q_choice = input('是否退出?(y/n):').strip()
            if q_choice == 'y':
                break

    def add_remoteuser(self):
        '''添加远程连接用户'''
        while True:
            print('添加连接远程主机帐户'.center(50,'-'))
            username = input('请输入用户名:').strip()
            if username == 'b':
                break
            if len(username) == 0:continue
            auth_type = input('请输入认证类型(ssh-password/ssh-key):').strip()
            if auth_type == 'ssh-password':
                passwd = input('请输入密码:').strip()
                passwd2 = input('请再次输入密码:').strip()
                if passwd == passwd2:
                    ru_obj = RemoteUser(auth_type=auth_type,username=username,password=passwd)
                    try:
                        session.add(ru_obj)
                        session.commit()
                        print('添加完成')
                    except IntegrityError:
                        session.rollback()   #如果上面的事务出错，这里要用到回滚，否则再次查询时会出错
                        print('\033[31;0m该帐户已存在\033[0m')
                else:
                    print('两次密码不一致')
            elif auth_type == 'ssh-key':
                ru_obj = RemoteUser(auth_type=auth_type,username=username)
                session.add(ru_obj)
                session.commit()
                print('添加完成')
            else:
                print('请输入正确的认证类型')
            q_choice = input('是否退出?(y/n):').strip()
            if q_choice == 'y':
                break

    def add_host(self):
        '''添加远程主机'''
        while True:
            print('添加远程连接主机'.center(50,'-'))
            h_name = input('请输入主机名:').strip()
            if h_name == 'b':
                break
            if len(h_name) == 0:continue
            h_ip = input('请输入IP地址:').strip()
            if len(h_ip) == 0:continue
            port = input('请输入SSH连接端口号(默认为22):').strip()
            if len(port) == 0:
                port = 22
            h_obj = Host(hostname=h_name,ip=h_ip,port=port)
            try:
                session.add(h_obj)
                session.commit()
                print('添加完成')
            except IntegrityError:
                session.rollback()   #如果上面的事务出错，这里要用到回滚，否则再次查询时会出错
                print('\033[31;0m主机已存在，请误重复添加\033[0m')
            q_choice = input('是否退出?(y/n):').strip()
            if q_choice == 'y':
                break
    def add_hostgroup(self):
        '''添加主机组'''
        while True:
            print('创建主机组'.center(50,'-'))
            group_name = input('请输入主机组名:').strip()
            if group_name == 'b':
                break
            if len(group_name) == 0:continue
            group_obj = HostGroup(name=group_name)
            try:
                session.add(group_obj)
                session.commit()
                print('添加完成')
            except IntegrityError:
                session.rollback()   #如果上面的事务出错，这里要用到回滚，否则再次查询时会出错
                print('\033[31;0m主机组已存在\033[0m')
            q_choice = input('是否退出?(y/n):').strip()
            if q_choice == 'y':
                break
    def add_bindhost(self):
        '''主机和使用登陆的帐户密码绑定'''
        while True:
            print('主机绑定远程连接帐户'.center(50,'-'))
            h_obj = session.query(Host).all()
            for h_index,h in enumerate(h_obj):
                print('%s. ip:%s'%(h_index,h))
            choice = input('请选择ip左边相应的序号:').strip()
            if len(choice) == 0:continue
            if choice == 'b':
                break
            if choice.isdigit():
                choice = int(choice)
                if choice < len(h_obj):
                    host_obj = h_obj[choice]
                else:
                    print('所输入的数字不在主机选择范围内')
                    continue
            else:
                print('请输入数字')
                continue
            ruse_obj = session.query(RemoteUser).all()
            for r_index,ruse in enumerate(ruse_obj):
                print('%s. %s'%(r_index,ruse))
            while True:
                ruse_choice = input('请选择该主机要绑定的帐户序号:')
                if len(ruse_choice) == 0:continue
                if ruse_choice.isdigit():
                    ruse_choice = int(ruse_choice)
                    if ruse_choice < len(ruse_obj):
                        r_obj = ruse_obj[ruse_choice]
                        bind_obj = BindHost(host_id=host_obj.id,remoteuser_id=r_obj.id)
                        try:
                            session.add(bind_obj)
                            session.commit()
                            print('绑定成功')
                        except IntegrityError:
                            session.rollback()   #如果上面的事务出错，这里要用到回滚，否则再次查询时会出错
                            print('\033[31;0m已存在\033[0m')
                        break
                    else:
                        print('所输入的数字不在主机选择范围内')
                        continue
                else:
                    print('请输入数字')
                    continue
            q_choice = input('是否退出绑定?(y/n):').strip()
            if q_choice == 'y':
                break

    def add_u_m2m_bindhost(self):
        '''添加堡垒机用户和绑定后的主机关联'''
        while True:
            print('堡垒机用户关联远程主机'.center(50,'-'))
            user_obj = session.query(UserProfile).all()
            for u_index,user in enumerate(user_obj):
                print('%s.%s'%(u_index,user))
            u_choice = input('请选择堡垒机用户序号:').strip()
            if len(u_choice) == 0:continue
            if u_choice == 'b':
                break
            if u_choice.isdigit():
                u_choice = int(u_choice)
                if u_choice < len(user_obj):
                    u_obj = user_obj[u_choice]
                else:
                    print('所输入的数字不在用户选择范围内')
                    continue
            else:
                print('请输入数字')
                continue
            b_host_obj = session.query(BindHost).all()
            for b_index,b_host in enumerate(b_host_obj):
                print('%s.%s'%(b_index,b_host))
            while True:
                b_choice = input('请选择绑定主机的序号:').strip()
                if len(b_choice) == 0:continue
                if b_choice == 'b':
                    break
                if b_choice.isdigit():
                    b_choice = int(b_choice)
                    if b_choice < len(b_host_obj):
                        host_obj = b_host_obj[b_choice]
                        u_obj.bind_hosts.append(host_obj)
                        session.commit()
                        print('关联成功')
                        break
                    else:
                        print('所输入的数字不在用户选择范围内')
                        continue
                else:
                    print('请输入数字')
                    continue
            q_choice = input('是否退出关联?(y/n):').strip()
            if q_choice == 'y':
                break

    def add_bhost_m2m_hgroup(self):
        '''绑定后的主机与组的关联'''
        while True:
            print('远程主机与组的关联'.center(50,'-'))
            h_group_obj = session.query(HostGroup).all()
            for g_index,gruop in enumerate(h_group_obj):
                print('%s.%s'%(g_index,gruop))
            g_choice = input('请选择主机组序号:').strip()
            if len(g_choice) == 0:continue
            if g_choice == 'b':
                break
            if g_choice.isdigit():
                g_choice = int(g_choice)
                if g_choice < len(h_group_obj):
                    gruop_obj = h_group_obj[g_choice]
                else:
                    print('所输入的数字不在用户选择范围内')
                    continue
            else:
                print('请输入数字')
                continue
            b_host_obj = session.query(BindHost).all()
            for b_index,b_host in enumerate(b_host_obj):
                print('%s.%s'%(b_index,b_host))
            while True:
                b_choice = input('请选择绑定主机的序号:').strip()
                if len(b_choice) == 0:continue
                if b_choice == 'b':
                    break
                if b_choice.isdigit():
                    b_choice = int(b_choice)
                    if b_choice < len(b_host_obj):
                        host_obj = b_host_obj[b_choice]
                        gruop_obj.bind_hosts.append(host_obj)
                        session.commit()
                        print('关联成功')
                        break
                    else:
                        print('所输入的数字不在用户选择范围内')
                        continue
                else:
                    print('请输入数字')
                    continue
            q_choice = input('是否退出关联?(y/n):').strip()
            if q_choice == 'y':
                break

    def add_user_m2m_group(self):
        '''堡垒机用户和主机组的关联'''
        while True:
            print('堡垒机用户关联主机组'.center(50,'-'))
            user_obj = session.query(UserProfile).all()
            for u_index,user in enumerate(user_obj):
                print('%s.%s'%(u_index,user))
            u_choice = input('请选择堡垒机用户序号:').strip()
            if len(u_choice) == 0:continue
            if u_choice == 'b':
                break
            if u_choice.isdigit():
                u_choice = int(u_choice)
                if u_choice < len(user_obj):
                    u_obj = user_obj[u_choice]
                else:
                    print('所输入的数字不在用户选择范围内')
                    continue
            else:
                print('请输入数字')
                continue
            h_group_obj = session.query(HostGroup).all()
            for g_index,gruop in enumerate(h_group_obj):
                print('%s.%s'%(g_index,gruop))
            while True:
                g_choice = input('请选择主机组序号:').strip()
                if len(g_choice) == 0:continue
                if g_choice == 'b':
                    break
                if g_choice.isdigit():
                    g_choice = int(g_choice)
                    if g_choice < len(h_group_obj):
                        gruop_obj = h_group_obj[g_choice]
                        u_obj.host_groups.append(gruop_obj)
                        session.commit()
                        print('关联成功')
                        break
                    else:
                        print('所输入的数字不在用户选择范围内')
                        continue
                else:
                    print('请输入数字')
                    continue
            q_choice = input('是否退出关联?(y/n):').strip()
            if q_choice == 'y':
                break