# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import json,hashlib,time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print('%s\\db\\users.txt' % (BASE_DIR))
sys.path.append(BASE_DIR)

def login(username='',password=''):
    '''
    登录接口，默认登录参数空
    :param username:
    :param password:
    :return: username ，userinfo
    '''
    flag = False
    lock_i = 0
    res = False
    while not flag:
        if username == '' or password == '':
            username = input('请输入用户名：')
            password = input('请输入密码：')
            password = hashlib.sha1(password.encode("utf8")).hexdigest()
        else:
            pass
        temp_user = get_users()
        if username not in temp_user:
            username = ''
            print('\033[1;31;1m查无此人！请输入正确的用户名！\033[0m')
            res = False
            continue
        elif temp_user[username]['locked'] == True:
            print('\033[1;31;1m%s已被锁死，请联系管理员解锁！\033[0m' % (username))
            res = False
            flag = True
            continue
        elif temp_user[username]['password'] != password:
            lock_i += 1
            if lock_i == 3:
                temp_user[username]['locked'] = True
                print(temp_user)
                with open('%s\\db\\users.txt' % (BASE_DIR),'w',encoding='utf-8') as u_info:
                    u_info.write(json.dumps(temp_user, ensure_ascii=False))
                print('\033[1;31;1m【%s】已被锁死，请联系管理员解锁！\033[0m' % (username))
                res = False
                flag = True
                continue
            print('密码错误，请重新输入，\033[1;31;1m您还有%d次机会\033[0m，账户将被锁死！' % (3 - lock_i))
            username = ''
            password = ''
            res = False
            continue
        else:
            u_info = temp_user[username]
            flag = True
            res = (username, u_info)
    return res


def get_users():
    try:
        u_info = open('%s\\db\\users.txt' % (BASE_DIR), 'r', encoding='utf-8')
    except FileNotFoundError:
        print('\033[1;31;1m用户信息文件损坏！即将退出\033[0m')
        time.sleep(1)
        exit()
    else:
        try:
            temp_user = json.loads(u_info.read())
        except json.decoder.JSONDecodeError:
            print('\033[1;31;1m用户信息文件损坏！即将退出\033[0m')
            time.sleep(1)
            exit()
    return temp_user

if __name__ == '__main__':
    print(login())