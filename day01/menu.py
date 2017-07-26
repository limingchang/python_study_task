# -*- coding = utf-8 -*-
#作者：Mc.Lee
key_list = {'1':'云南','2':'四川','3':'贵州'}
menu_dic = {
    '云南':{
        '楚雄':['元谋县','大姚县','南华县','武定县'],
        '昆明':['五华区','西山区','盘龙区','官渡区'],
        '丽江':['古城区','华坪县','玉龙县','永胜县'],
    },
    '四川':{
        '成都':['锦江区','武侯区','郫县'],
        '绵阳':['安州区','游仙区','北川县'],
        '眉山':['东坡区','彭山区','仁寿县'],
    },
    '贵州':{
        '贵阳':['观山湖','云岩区','南明区'],
        '遵义':['红花岗','汇川区','桐梓县'],
        '六盘水':['水城县','钟山区','六枝特区'],
    }
}


def menu():
    print('请选择省份：'.center(40, '-'))
    i = 1
    dic_key = {}
    for level in menu_dic:
        dic_key[i] = level#创建临时字典
        print(i,'.',level)
        i += 1
    print('输入q可退出'.center(40, '-'))
    act = input('请输入你选择的省份（中文或数字）：')
    if act.isdigit():
        act = dic_key[int(act)]
    if act == 'q' or act == '退出':
        exit()
    else:
        if act in menu_dic:

            menu_2(act)
        else:
            print('未找到此省份数据，请重新输入！')
            menu()
    return


def menu_2(key):
    print('输入命令返回（b）或退出（q）'.center(33, '-'))
    menu2 = menu_dic[key]
    i = 1
    dic_key = {}
    for level in menu2:
        dic_key[i] = level  # 创建临时字典
        print(i, '.', level)
        i += 1
    print('-'*45)
    act = input('请输入你选择的市（中文或数字）：')
    if act.isdigit():
        act = dic_key[int(act)]
    if act == 'b' or act == '返回':
        menu()
    elif act == 'q' or act == '退出':
        exit()
    else:
        if act in menu_dic[key]:
            key2 = act
            menu_3(key, key2)
        else:
            print('未找到此市级区划数据，请重新输入！')
            menu_2(key)
    return


def menu_3(key, key2):
    print('输入命令返回（b）或退出（q）'.center(33, '-'))
    print('-' * 45)
    menu3 = menu_dic[key][key2]
    i = 1
    dic_key = {}
    for level in menu3:
        dic_key[i] = level  # 创建临时字典
        print(i, '.', level)
        i += 1
    act = input('请输入命令：')
    if act == 'b' or act == '返回':
        menu_2(key)
    elif act == 'q' or act == '退出':
        exit()
    else:
        print('命令错误，请重新输入！')
        menu_3(key,key2)
    return

menu()