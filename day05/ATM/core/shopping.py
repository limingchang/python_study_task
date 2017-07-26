# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'

import json,hashlib,time,datetime
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from admin import manage,card_manage
from core import user,card

def auth(func):
    def wrapper(*args,**kwargs):
        print('用户登录'.center(50, '-'))
        res = user.login()
        if not res:
            print('\033[1;31;1m登录失败！\033[0m')
        else:
            func(res)
            #return res
    return wrapper


@auth
def shopping(user_info):
    #user_info = user.login()
    money = user_info[1]['money']
    res = card.get_user_card(user_info[0])
    money_str = '当前现金【\033[1;36;1m%d元\033[0m】'%(money)
    if res['errcode'] == 0:
        card_limit = res['msg'][1]['limit']
        card_banlance = res['msg'][1]['banlance']#可用余额
        card_frozen = res['msg'][1]['frozen']
        if not card_frozen:
            card_str = '信用卡可用额度【\033[1;36;1m%d元\033[0m】，'% (card_banlance)
            total_card = card_banlance
        else:
            card_str = '\033[1;31;1m信用卡已冻结\033[0m'
            total_card = 0
    else:
        print(res['msg'])
    total_money = money + total_card
    banlance = total_money
    print(money_str,card_str)
    user_shopping = []
    if total_money == 0:
        print('\033[1;31;1m没钱买毛啊！\033[0m')
        return
    flag = False
    while not flag:
        product = show_product()
        #print(product)
        act = input('请选择商品（q退出并结账）：')
        if act.isdigit():
            act = int(act)
            if act < product[0]:
                if total_money - product[1][act][1] < 0:
                    print('\033[1;31;1m余额不足！\033[0m')
                    continue
                else:
                    banlance = banlance - product[1][act][1]
                    user_shopping.append(product[1][act])
                    print('您将【\033[1;32;1m%s\033[0m】加入购物车。' % (product[1][act][0]))
                    print('目前已消费【\033[1;36;1m%d\033[0m】元，余额【\033[1;36;1m%d\033[0m】元'%(total_money - banlance,banlance))
            else:
                print('错误的编号！')
                continue
        elif act == 'q':
            flag = True
        else:
            print('错误的选择！')
            continue
    #写入记录
    if len(user_shopping) > 0:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        shopping_list = user_shopping
        total_now = total_money - banlance
        username = user_info[0]
        if money - total_now < 0:
            money = 0
            total_card = total_card - (total_now - money)
        else:
            money = money - total_now
        str = '[shop]|{_user}|{_time}|{_list}|{_total_now}|{_money}|{_total_card}\n'.format(_user=username, _time=now,
                                                                                            _list=shopping_list,
                                                                                            _total_now=total_now,
                                                                                            _money=money,
                                                                                            _total_card=total_card)

        with open('%s\\db\\user_log.txt' % (BASE_DIR),'a',encoding='utf-8') as f:
            f.write(str)
        #写入用户记录
        temp_user = user.get_users()
        temp_user[username]['money'] = money
        with open('%s\\db\\users.txt' % (BASE_DIR),'w',encoding='utf-8') as f:
            f.write(json.dumps(temp_user, ensure_ascii=False))
        #写入信用卡记录
        temp_cards = card_manage.get_cards()
        for card_id in temp_cards:
            if temp_cards[card_id]['owner'] == username:
                temp_cards[card_id]['banlance'] = total_card
        with open('%s\\db\\cards.txt' % (BASE_DIR),'w',encoding='utf-8') as f:
            f.write(json.dumps(temp_cards, ensure_ascii=False))
    #print(user_shopping)



def show_product():
    product_dict = get_product()
    current_product = []
    print('商品列表'.center(60,'*'))
    print('|', '选择'.center(4, ' '), '|', '名称'.center(20, ' '), '|', '价格'.center(18, ' '), '|')
    i = 0
    for product in product_dict:
        current_product.append((product,product_dict[product]))
        print('|', str(i).center(6, ' '), '|', product.center(22, ' '), '|',str('￥%d元' % (product_dict[product])).rjust(18, ' '), '|')
        i += 1
    return i,current_product


def get_product():
    try:
        f = open('%s\\db\\products.txt' % (BASE_DIR),'r',encoding='utf-8')
    except FileNotFoundError:
        with open('%s\\db\\products.txt' % (BASE_DIR),'w',encoding='utf-8') as f:
            f.write('{}')
        res = {}
    else:
        try:
            res = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            res = {}
    if len(res) == 0:
        print('\033[1;31;1m商品列表为空，请以管理员身份登录以添加商品！\033[0m')
        manage.show_menu()
    return res


def test():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    shopping_list = [('iPhone6s', 5888), ('imac 高配版', 21888), ('卡布奇诺', 18)]
    total_now = 27794
    money = 0
    total_card = 90000
    username = 'lmc'
    if money - total_now < 0:
        money = 0
        total_card = total_card - (total_now - money)
    else:
        money = money - total_now
    str = '[shop]|{_user}|{_time}|{_list}|{_total_now}|{_money}|{_total_card}\n'.format(_user=username,_time=now,_list=shopping_list,_total_now=total_now,_money=money,_total_card=total_card)

    print(str)

if __name__ == '__main__':
    print(shopping())
    #test()