# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'


def show():
    print('工资管理系统'.center(50,'*'))
    flag = False
    while not flag:
        print('1.查询员工工资\n2.修改员工工资\n3.新增员工记录\n4.退出')
        act = input('请选择：')
        if act.isdigit():
            act = int(act)
            if act == 1:
                search()
                continue
            elif act == 2:
                modify()
                continue
            elif act == 3:
                add()
                continue
            elif act == 4:
                print('再见！')
                flag = True
                continue
            else:
                print('\033[1;31;1m指令错误！请重新输入！\033[0m')
                continue
        else:
            print('\033[1;31;1m指令错误！请输入对应数字！\033[0m')
            continue


def search():
    flag = False
    temp_info = get_info()
    while not flag:
        name = input('请输入要查询的员工姓名（例如：Alex）:')
        name= name.strip().lower().capitalize()  # 忽略输入时人名的大小写错误
        if name in temp_info:
            print('\033[1;32;1m%s的工资是：%d。\033[0m'%(name,temp_info[name]))
            flag = True
        else:
            print('\033[1;31;1m查无此人！请重新输入\033[0m')
            continue


def modify():
    flag =False
    temp_info = get_info()
    while not flag:
        info = input('请输入要修改的员工姓名和工资，用空格分隔（例如：Alex 10）：')
        info = info.split(' ')
        info[0] = info[0].lower().capitalize()#忽略输入时人名的大小写错误
        if len(info) != 2 or not info[1].isdigit():
            print('输入格式不正确：')
            continue
        elif info[0] in temp_info:
            temp_info[info[0]] = int(info[1])
            write_str = ''
            for key in temp_info:
                write_str = '%s%s %d\n' % (write_str,key, temp_info[key])
            with open('info.txt', 'w', encoding='utf-8')as f:
                f.write(write_str)
            print('\033[1;32;1m修改成功！\033[0m')
            flag =True
            continue
        else:
            print('无此员工，请查证后输入：')
            continue


def add():
    flag = False
    temp_info = get_info()
    while not flag:
        info = input('请输入要增加的员工姓名和工资，共空格分割（例如：Eric 100000）：')
        info = info.split(' ')
        info[0] = info[0].lower().capitalize()  # 忽略输入时人名的大小写错误
        if len(info) != 2 or not info[1].isdigit():
            print('输入格式不正确：')
            continue
        elif info[0] in temp_info:
            print('已存在员工，请重新输入！')
            continue
        else:
            temp_info[info[0]] = int(info[1])
            write_str = ''
            for key in temp_info:
                write_str = '%s%s %d\n' % (write_str, key, temp_info[key])
            with open('info.txt', 'w', encoding='utf-8')as f:
                f.write(write_str)
            print('\033[1;32;1新增成功！\033[0m')
            flag = True
            continue


def get_info():
    '''
    获取员工数据
    :return: 员工数据字典
    '''
    temp_info = {}
    with open('info.txt','r',encoding='utf-8') as f:
        line = f.readline()
        while line:
            info = line.rstrip().split(' ')
            #print(info)
            temp_info[info[0]] = int(info[1])
            line = f.readline()
    return temp_info


if __name__ == '__main__':
    show()