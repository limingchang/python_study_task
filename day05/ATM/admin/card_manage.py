# -*- coding: utf-8 -*-
'''
管理员用户信用卡接口
'''
__author__ = 'Mc.Lee'
import json,hashlib,time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import user


def card_menu():
    print('信用卡管理端'.center(50, '#'))
    flag = False
    while not flag:
        print('1.添加信用卡\n2.修改用户额度\n3.冻结账户')
        act = input('请选择指令（q退出）：')
        if act.isdigit():
            act = int(act)
            if act == 1:
                res = card_add()
                if res:
                    print('\033[1;36;1m为%s添加信用卡成功,额度%d元\033[0m' %(res['owner'],res['limit']))
                else:
                    print('\033[1;31;1m添加失败！请联系管理员\033[0m')
                    continue
            elif act == 2:
                res = card_modify()
                if res:
                    print('\033[1;36;1m为%s修改信用卡额度成功,新额度%d元\033[0m' % (res['owner'], res['limit']))
                else:
                    print('\033[1;31;1m修改失败！请联系管理员\033[0m')
                    continue
            elif act == 3:
                res = card_fronzen()
                if res:
                    isfrozen = '\033[1;31;1m冻结\033[0m' if res['frozen'] else '\033[1;32;1m正常\033[0m'
                    print('%s的信用卡已修改为【%s】' % (res['owner'], isfrozen))
                else:
                    print('\033[1;31;1m修改失败！请联系管理员\033[0m')
                    continue
            else:
                print('\033[1;31;1m错误的选项！\033[0m')
        elif act.lower() == 'q':
            print('退出系统...')
            flag = True
            continue
        else:
            print('\033[1;31;1m错误的指令！\033[0m')
            continue

def card_add():
    res = False
    temp_cards = get_cards()
    flag = False
    while not flag:
        card_id = input('请输入信用卡卡号（必须为纯数字8位）：')
        if  not card_id.isdigit() or len(card_id) != 8:
            print('\033[1;31;1m卡号错误!\033[0m')
            continue
        else:
            if re_cardid(temp_cards,card_id):
                print('\033[1;31;1m卡号已存在!\033[0m')
                continue
            else:
                while not flag:
                    card_limit = input('请输入信用卡最高额度：')
                    if not card_limit.isdigit():
                        print('\033[1;31;1m信用卡额度必须为整数!\033[0m')
                        continue
                    else:
                        #获取用户列表并循环显示，记录进临时列表
                        temp_user = user.get_users()
                        i = 0
                        user_list = []
                        for users in temp_user:
                            user_list.append(users)
                            print(i,'┄',users)
                            i += 1
                        while not flag:
                            card_woner = input('请选择卡片所有者：')
                            if card_woner.isdigit():
                                card_woner = int(card_woner)
                                #判断用户是否有卡
                                if re_card_owner(temp_cards,user_list[card_woner]):
                                    print('\033[1;31;1m他有卡了，别添加了!\033[0m')
                                    continue
                                else:
                                    temp_cards[card_id] = {
                                        'limit' :int(card_limit),
                                        'owner':user_list[card_woner],
                                        'banlance':int(card_limit),
                                        'frozen':False
                                    }
                                    with open('%s\\db\\cards.txt' % (BASE_DIR), 'w', encoding='utf-8') as f:
                                        f.write(json.dumps(temp_cards, ensure_ascii=False))
                                    flag =True
                                    res = temp_cards[card_id]
                                    break
                            else:
                                print('\033[1;31;1m错误的选择！\033[0m')
                                continue
                break
        break
    return res


def card_modify():
    flag = False
    res = False
    temp_cards = get_cards()
    while not flag:
        print('信用卡额度修改'.center(50,'#'))
        card_list = []
        i = 0
        for card in temp_cards:
            card_list.append(card)
            print(i,'=> 卡号：',card,'|| 额度：',temp_cards[card]['limit'],'||所有者：',temp_cards[card]['owner'])
            i += 1
        act = input('请输入序号选择要修改额度的信用卡(q退出）:')
        if act.isdigit() and int(act) < len(temp_cards):
            act = int(act)
            while not flag:
                card_limit = input('请为%s设定新的信用卡额度（当前额度%d元）：' %(temp_cards[card_list[act]]['owner'],temp_cards[card_list[act]]['limit']))
                if not card_limit.isdigit():
                    print('\033[1;31;1m信用卡额度必须为整数!\033[0m')
                    continue
                else:
                    temp_cards[card_list[act]]['banlance'] = temp_cards[card_list[act]]['banlance'] + int(card_limit) - temp_cards[card_list[act]]['limit']
                    temp_cards[card_list[act]]['limit'] = int(card_limit)
                    #print(temp_cards)
                    with open('%s\\db\\cards.txt' % (BASE_DIR), 'w', encoding='utf-8') as f:
                        f.write(json.dumps(temp_cards, ensure_ascii=False))
                    res = temp_cards[card_list[act]]
                    flag = True
                    break

        elif act == 'q':
            flag = True
            break
        else:
            print('选择错误！')
            continue
    return res


def card_fronzen():
    flag = False
    res = False
    temp_cards = get_cards()
    while not flag:
        print('冻结信用卡'.center(50,'#'))
        card_list = []
        i = 0
        for card in temp_cards:
            card_list.append(card)
            if temp_cards[card]['frozen']:
                print('%d=> 卡号：%s||所有者：%s||状态：\033[1;31;1m冻结\033[0m' % (i,card,temp_cards[card]['owner']))
            else:
                print('%d=> 卡号：%s||所有者：%s||状态：\033[1;32;1m正常\033[0m' % (i, card, temp_cards[card]['owner']))
            i += 1
        act = input('请输入序号选择要冻结/解冻的信用卡(q退出）:')
        if act.isdigit() and int(act) < len(card_list):
            act = int(act)
            temp_cards[card_list[act]]['frozen'] = not temp_cards[card_list[act]]['frozen']
            with open('%s\\db\\cards.txt' % (BASE_DIR), 'w', encoding='utf-8') as f:
                f.write(json.dumps(temp_cards, ensure_ascii=False))
            res = temp_cards[card_list[act]]
            flag = True
            break
        elif act == 'q':
            flag = True
            res = False
            break
        else:
            print('选择错误！')
            continue

    return res


def re_cardid(temp_cards,card_id):
    '''
    判断卡号是否已存在
    :param temp_cards: 信用卡临时数据
    :param card_id: 信用卡ID
    :return: 存在返回真，不存在返回假
    '''
    res = False
    if card_id in temp_cards:
        res = True
    else:
        res = False
    return res


def re_card_owner(temp_cards,owner):
    '''
    判断用户是否拥有了信用卡
    :param temp_cards: 信用卡临时数据
    :param owner: 信用卡拥有者
    :return: 有返回真，没有返回假
    '''
    res = False
    for card in temp_cards:
        if temp_cards[card]['owner'] == owner:
            res = True
    return res




def get_cards():
    try:
        f = open('%s\\db\\cards.txt' % (BASE_DIR),'r',encoding='utf-8')
    except FileNotFoundError:
        with open('%s\\db\\cards.txt' % (BASE_DIR), 'w', encoding='utf-8') as f:
            f.write('{}')
        res = {}
    else:
        try:
            res = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            res = {}
    if len(res) == 0:
        print('\033[1;31;1m信用卡列表为空，请添加卡片！\033[0m')
    return res


if __name__ == '__main__':
    card_menu()