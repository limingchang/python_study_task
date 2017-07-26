# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'


import json,hashlib,time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print('%s\\db\\users.txt' % (BASE_DIR))
sys.path.append(BASE_DIR)
from core import user,shopping,card
from admin import card_manage

def auth(func):
    def wrapper(*args,**kwargs):
        print('管理员登录'.center(50, '-'))
        res = user.login()
        if not res:
            print('\033[1;31;1m账户已被锁定！\033[0m')
            print('\033[1;31;1m登录失败！\033[0m')
        else:
            if res[1]['authority']:#是否是管理员身份
                func()
            else:
                print('\033[1;31;1m您没有管理权限！\033[0m')
                exit()
            return res
    return wrapper


@auth
def show_menu():
    flag = False
    while not flag:
        print('管理系统'.center(50,'-'))
        print('1.用户注册\n2.添加商品\n3.信用卡管理')
        act = input('请选择（q退出）：')
        if act == '1':
            print('用户注册'.center(50,'*'))
            register()
        elif act == '2':
            if product_add():
                print('\033[1;32;1m新增商品成功！\033[0m')
            continue
        elif act == '3':
            card_manage.card_menu()
            continue
            # amin_card
        elif act == 'q':
            print('退出')
            return False
        else:
            print('\033[1;31;1m输入了错误的指令！\033[0m')
            flag = False
            continue



#注册
def register():
    flag_name = False
    flag_pwd = False
    try:
        f = open('%s\\db\\users.txt' % (BASE_DIR),'r',encoding='utf-8')
    except FileNotFoundError:
        print('\033[1;31;1m无用户信息文件，创建后重新开始！\033[0m')
        with open('%s\\db\\users.txt' % (BASE_DIR),'w',encoding='utf-8')as f1:
            f1.write('{}')
            register()
    else:
        try:
            temp_user = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            temp_user = {}
        f.close()
    while not flag_name:
        username = input('请输入您要注册的用户名：')
        if username in temp_user:
            print('\033[1;31;1m此用户名已被注册！Change one!\033[0m')
            continue
        else:
            while not flag_pwd:
                password = input('请输入密码：')
                re_password = input('再次确认密码：')
                if password != re_password:
                    print('\033[1;31;1m两次输入的密码不一致!\033[0m')
                    continue
                else:
                    while not flag_pwd:
                        money = input('请输入初始现金：')
                        if money.isdigit():
                            temp_user[username] = {
                                'password':hashlib.sha1(password.encode("utf8")).hexdigest(),
                                'locked': False,
                                'money':int(money),
                                'authority':False
                            }
                            flag_pwd = True
                    else:
                        print('\033[1;31;1m初始现金必须为整数!\033[0m')
                        continue
            with open('%s\\db\\users.txt' % (BASE_DIR),'w',encoding='utf-8')as users:
                users.write(json.dumps(temp_user,ensure_ascii=False))
            flag_name = True
            continue
    return username,temp_user[username]['password']


def product_add():
    with open('%s\\db\\products.txt' % (BASE_DIR), 'r', encoding='utf-8') as f:
        temp_products = json.loads(f.read())
    flag = False
    while not flag:
        product_name = input('输入新商品名称：')
        price = input('输入商品价格：')
        if price.isdigit():
            price = int(price)
            temp_products[product_name] = price
            with open('%s\\db\\products.txt' % (BASE_DIR),'w',encoding='utf-8') as f:
                f.write(json.dumps(temp_products,ensure_ascii=False))
            flag = True
            return True
        else:
            print('\033[1;31;1m错误：\033[0m','\033[1;36;1m商品价格必须是整数！\033[0m')
            continue


if __name__ == '__main__':
    print(show_menu())
    #product_add()