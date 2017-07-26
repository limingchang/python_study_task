# -*- coding: utf-8 -*-
'''
普通用户信用卡接口
提供：个人账单、信用卡还款、提现业务
'''
__author__ = 'Mc.Lee'
import json,hashlib,time,datetime
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import user
from admin import card_manage

def auth(func):
    def wrapper(*args,**kwargs):
        print('用户登录'.center(50, '-'))
        res = user.login()
        if not res:
            print('\033[1;31;1m登录失败！\033[0m')
        else:
            func(res)
            # return res

    return wrapper

@auth
def card_menu(user_info):
    print('个人信用卡业务'.center(50,'#'))
    flag = False
    while not flag:
        print('1.个人账单\n2.信用卡还款\n3.提现\n4.转账')
        act = input('请选择指令（q退出）：')
        if act.isdigit():
            act = int(act)
            if act == 1:
                bill(user_info[0])
                print('个人账单')
            elif act == 2:
                res = repayment(user_info)
                if res:
                    if res['errcode'] == 0:
                        print(res['msg'])
                else:
                    print('还款失败，请联系管理员！')
            elif act == 3:
                res = cash(user_info)
                if res:
                    if res['errcode'] == 0:
                        print(res['msg'])
                else:
                    print('提现失败，请联系管理员！')
            elif act == 4:
                res = transfer_accounts(user_info)
                if res:
                    if res['errcode'] == 0:
                        print(res['msg'])
                else:
                    print('转账失败，请联系管理员！')
            else:
                print('\033[1;31;1m错误的选项！\033[0m')
        elif act.lower() == 'q':
            print('退出系统...')
            flag = True
            continue
        else:
            print('\033[1;31;1m错误的指令！\033[0m')
            continue



def repayment(user_info):
    '''
    还款
    :return:
    '''
    res = False
    #print(user_info)
    temp_users = user.get_users()
    temp_cards = card_manage.get_cards()
    user_card = get_user_card(user_info[0])
    debt = user_card['msg'][1]['limit'] - user_card['msg'][1]['banlance']
    while True:
        print('您当前拥有现金【%d】元。'%(user_info[1]['money']))
        print('您当前信用卡欠款金额【%d】元。'% (debt) )
        if user_info[1]['money'] == 0:
            print('钱都没有，还毛线啊！滚蛋！')
            break
        re_money = input('请输入要还款的金额(输入all归还全部欠款)：')
        if re_money.isdigit() and int(re_money) <= user_info[1]['money']:
            re_money = int(re_money)
            if re_money > debt:
                print('您只需归还【%d】元,系统为您自动扣除，多余部分返还现金。'%(debt))
                user_card['msg'][1]['banlance'] = user_card['msg'][1]['limit']
                #temp_users[user_info[0]]['money']
                user_info[1]['money'] -= debt
            else:
                user_card['msg'][1]['banlance'] += re_money
                user_info[1]['money'] -= re_money
        elif re_money.lower() == 'all':
            re_money = debt
            user_card['msg'][1]['banlance'] = user_card['msg'][1]['limit']
            user_info[1]['money'] -= debt
        elif re_money.lower() == 'q':
            break
        else:
            print('输入的还款金额错误！')
            continue
        temp_users[user_info[0]] = user_info[1]
        temp_cards[user_card['msg'][0]] = user_card['msg'][1]
        with open('%s\\db\\users.txt' % (BASE_DIR),'w',encoding='utf-8') as f:
            f.write(json.dumps(temp_users, ensure_ascii=False))
        with open('%s\\db\\cards.txt' % (BASE_DIR),'w',encoding='utf-8') as f:
            f.write(json.dumps(temp_cards, ensure_ascii=False))
        str = '\033[1;36;1m【%s】还款【%s】元，剩余现金【%s】元，信用卡可用额度【%s】元。\033[0m'%(user_info[0],re_money,user_info[1]['money'],user_card['msg'][1]['banlance'])
        res = {
            'errcode':0,
            'msg':str
        }
        info = '还款%d元\n' % (re_money)
        write_card_log('repay', user_info[0], info)
        break
        #print(res)
    return res


def cash(user_info):
    '''
    提现
    :return:
    '''
    res = False
    # print(user_info)
    temp_users = user.get_users()
    temp_cards = card_manage.get_cards()
    user_card = get_user_card(user_info[0])
    while True:
        print('\033[1;36;1m您现在拥有现金【%d】元，可提现额度【%d】元。\033[0m'%(user_info[1]['money'],user_card['msg'][1]['banlance']))
        cash_moeny = input('请输入您要提现的金额\033[1;31;1m（5%手续费哦）\033[0m：')
        if cash_moeny.isdigit() and int(cash_moeny) <= user_card['msg'][1]['banlance']:
            user_info[1]['money'] += int(cash_moeny)
            user_card['msg'][1]['banlance'] -= int(int(cash_moeny) * 1.05)
            temp_users[user_info[0]] = user_info[1]
            temp_cards[user_card['msg'][0]] = user_card['msg'][1]
            with open('%s\\db\\users.txt' % (BASE_DIR), 'w', encoding='utf-8') as f:
                f.write(json.dumps(temp_users, ensure_ascii=False))
            with open('%s\\db\\cards.txt' % (BASE_DIR), 'w', encoding='utf-8') as f:
                f.write(json.dumps(temp_cards, ensure_ascii=False))
            str = '\033[1;36;1m【%s】提现【%d】元，现金合计【%d】元，信用卡可用额度【%d】元\033[0m' % (user_info[0], int(cash_moeny), user_info[1]['money'], user_card['msg'][1]['banlance'])
            res = {
                'errcode': 0,
                'msg': str
            }
            info = '提现%d元\n' % (int(cash_moeny))
            write_card_log('cash', user_info[0],info)
            break
        else:
            print('\033[1;31;1m提现金额输入错误\033[0m')
            continue
    return res


def transfer_accounts(user_info):
    '''
    转账
    :param user_info:
    :return:
    '''
    res = False
    # print(user_info)
    temp_users = user.get_users()
    temp_cards = card_manage.get_cards()
    user_card = get_user_card(user_info[0])
    while True:
        print('信用卡转账'.center(50, '#'))
        print('\033[1;36;1m您现在拥有现金【%d】元。\033[0m' % (user_info[1]['money']))
        if user_info[1]['money'] == 0:
            print('\033[1;31;1m钱都没有，转毛线啊！滚蛋！\033[0m')
            break
        tran_money = input('请输入转账金额(q退出）:')
        if tran_money.isdigit() and int(tran_money) <= user_info[1]['money']:
            tran_money = int(tran_money)
            card_list = []
            i = 0
            for card in temp_cards:
                card_list.append(card)
                print(i, '=> 卡号：', card, '||所有者：', temp_cards[card]['owner'])
                i += 1
            while True:
                act = input('请选择转入的信用卡(q退出）:')
                if act.isdigit() and int(act) < len(temp_cards):
                    act = int(act)
                    temp_cards[card_list[act]]['banlance'] += tran_money
                    user_info[1]['money'] -= tran_money
                    temp_users[user_info[0]] = user_info[1]
                    with open('%s\\db\\users.txt' % (BASE_DIR), 'w', encoding='utf-8') as f:
                        f.write(json.dumps(temp_users, ensure_ascii=False))
                    with open('%s\\db\\cards.txt' % (BASE_DIR), 'w', encoding='utf-8') as f:
                        f.write(json.dumps(temp_cards, ensure_ascii=False))
                    str = '\033[1;36;1m【%s】向【%s】转账%d元成功。\033[0m' % (user_info[0], temp_cards[card_list[act]]['owner'] , user_info[1]['money'], tran_money)
                    res = {
                        'errcode': 0,
                        'msg': str
                    }
                    info = '向%s转账%d元\n'%(temp_cards[card_list[act]]['owner'],tran_money)
                    write_card_log('tran',user_info[0],info)
                    break
                else:
                    print('选择错误！')
                    continue
        else:
            continue
        break
    return res




def bill(username):
    '''
    账单
    :return:
    '''
    print('1.购物账单\n2.信用卡账单')
    while True:
        act = input('请选择（q退出）：')
        if act.isdigit():
            if act == '1':
                print('购物账单'.center(50,'-'))
                log_list = get_logs(username,'user_log.txt')
                #print(log_list)
                for log in log_list:
                    log[3] = eval(log[3])
                    shop_str = '购买：'
                    for shop_list in log[3]:
                        shop_str = '%s%s，%d元；'%(shop_str,shop_list[0],shop_list[1])
                    print(log[2],shop_str,'合计花费：',log[4],'元。')
            if act == '2':
                print('信用卡账单'.center(50,'-'))
                log_list = get_logs(username, 'card_log.txt')
                for log in log_list:
                    print(log[2],log[3])
            elif act == 'q':
                break
            else:
                continue





def get_user_card(username):
    '''
    获取用户名下所有信用卡
    :return:
    '''
    res = {'errcode':1,'msg':'获取失败！'}
    user_card_list = []
    if username == '':
        print('\033[1;31;1m参数错误！\033[0m')
    else:
        temp_cards = card_manage.get_cards()
        for card_id in temp_cards:
            if temp_cards[card_id]['owner'] == username:
                user_card_list.append(temp_cards[card_id])
                user_card_id = card_id
        if len(user_card_list) == 0:
            res = {
                'errcode':2,
                'msg':'您没有信用卡，请联系管理员获取信用卡！'
            }
        else:
            res = {
                'errcode': 0,
                'msg':(user_card_id,user_card_list[0])
            }
    return res


def write_card_log(act,user,info):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    str = '[{_act}]|{_user}|{_time}|{_info}'.format(_act=act,_user=user,_time=now,_info=info)
    with open('%s\\db\\card_log.txt' % (BASE_DIR), 'a', encoding='utf-8') as f:
        f.write(str)

def get_logs(username,filename):
    log_list = []
    with open('%s\\db\\%s' % (BASE_DIR,filename), 'r', encoding='utf-8') as f:
        line = True
        line = f.readline()
        while line:
            line = line.strip().split('|')
            if line[1] == username:
                log_list.append(line)
            line = f.readline()
    return log_list





if __name__ == '__main__':
    print(bill('lmc'))