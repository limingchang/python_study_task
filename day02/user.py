# -*- coding: utf-8 -*-
#作者：Mc.Lee
import json,hashlib

#注册
def register():
    flag = False
    while not flag:
        username = input('请输入您的用户名：')
        password = input('请输入您的密码：')
        re_password = input('请再次重复您的密码：')
        with open('users.txt','r') as u_info:
            temp_users = json.loads(u_info.read())
        #print(temp_users)
        if username in temp_users:
            print('用户已被注册，请重新输入！')
            continue
        elif re_password != password:
            print('两次输入密码不一致，请重新输入！')
            continue
        else:
            info ={
                    'password':hashlib.sha1(password.encode("utf8")).hexdigest(),
                    'salary':-1,
                    'locked':False,
                    'shopping':{},
                    'authority':0
            }
            temp_users[username] = info
            with open('users.txt','w') as u_info:
                u_info.write(json.dumps(temp_users,ensure_ascii=False))
            flag = True
    return True


def login():
    flag = False
    lock_i = 0
    while not flag:
        username = input('请输入用户名：')
        password = input('请输入密码：')
        password = hashlib.sha1(password.encode("utf8")).hexdigest()
        with open('users.txt','r') as u_info:
            temp_user = json.loads(u_info.read())
        if username not in temp_user:
            print('查无此人！')
            continue
        elif temp_user[username]['locked'] == True:
            print('\033[1;31;1m%s已被锁死，请联系管理员解锁！\033[0m'%(username))
            continue
        elif temp_user[username]['password'] != password:
            lock_i += 1
            if lock_i == 3:
                temp_user[username]['locked'] = True
                with open('users.txt','w') as u_info:
                    u_info.write(json.dumps(temp_user,ensure_ascii=False))
                print('\033[1;31;1m%s已被锁死，请联系管理员解锁！\033[0m' % (username))
                exit()
            print('密码错误，请重新输入，\033[1;31;1m您还有%d次机会\033[0m，账户将被锁死！'%(3-lock_i))
            continue
        else:
            u_info = temp_user[username]
            flag = True
    return username,u_info


if __name__ == '__main__':
    login()
    #register()