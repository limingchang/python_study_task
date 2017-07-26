# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from core import index


def mian():
    print('\033[1;36;1m欢迎使用选课系统\033[0m'.center(40,'█'))
    print('请选择登录类型'.center(45,'-'))
    print('''1.学员视图
2.讲师视图
3.管理视图
q.退出系统''')
    type_list = {
        1:"student",
        2: "teacher",
        3: "admin",
        "q": exit,
    }
    act = input("请选择：")
    if act.isdigit() and int(act) <= len(type_list) - 1:
        role_type = type_list[int(act)]
        role_interface = index.ROLE_INTERFACE(role_type)
    elif act.lower() == 'q':
        type_list[act]()
    else:
        print('\033[1;31;1m指令错误!\033[0m')





if __name__ == '__main__':
    #role = ROLE_INTERFACE("")
    mian()