# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print('%s\\db\\users.txt' % (BASE_DIR))
sys.path.append(BASE_DIR)
from core import shopping,card
from admin import manage

def show_menu():
    flag = False
    while not flag:
        print('欢迎使用ATM+购物商城系统'.center(50, '$'))
        print('1.购物商城系统\n2.ATM信用卡系统\n3.管理入口')
        act = input('请选择（q退出）：')
        if act == '1':
            shopping.shopping()
        elif act == '2':
            card.card_menu()
        elif act == '3':
            manage.show_menu()
        elif act == 'q':
            print('退出')
            exit()
        else:
            print('\033[1;31;1m输入了错误的指令！\033[0m')
            flag = False
            continue





if __name__ == '__main__':
    show_menu()
