# -*- coding: utf-8 -*-
#作者：Mc.Lee
from user import *
import json

def shopping():
    flag = False
    temp_user = login()
    if temp_user[1]['salary'] < 0:
        salary = input('请输入您的工资：')
        if salary.isdigit():
            salary = int(salary)
        else:
            print('\033[1;31;1m输入错误！工资必须是整数！\033[0m')
            shopping()
    else:
        salary = temp_user[1]['salary']
    shopping_list = temp_user[1]['shopping']
    while not flag:
        print('选择商品(q结账)'.center(75,'*'))
        print('|', '选择'.center(4, ' '),'|', '名称'.center(18, ' '), '|', '价格'.center(18, ' '), '|', '描述'.center(18, ' '), '|')
        print('-'*85)
        with open('product.txt', 'r') as p_info:
            temp_product = json.loads(p_info.read())
            # print(type(temp_product))
        current_product = []
        i = 0
        for product in temp_product:
            current_product.append(product)
            print('|',str(i).center(6,' '), '|',product.center(20, ' '), '|', str('￥%d元' % (temp_product[product]['price'])).rjust(18, ' '), '|',str(temp_product[product]['title']).ljust(18-int(len(temp_product[product]['title'])/2), ' '), '|')
            i += 1
        tips = '您还有【\033[1;32;1m%d元\033[0m】可用'%(salary)
        print(tips.center(85,'*'))
        act = input('请输入序号选择您需要的商品：')
        if act.isdigit():
            act = int(act)
            if act < len(current_product) and act >= 0:
                if salary - temp_product[current_product[act]]['price'] < 0:
                    print('\033[1;31;1m余额不足，请重新选择商品！\033[0m')
                    continue
                else:
                    salary = salary - temp_product[current_product[act]]['price']
                    shopping_list[str(len(shopping_list))] ={
                        'name':current_product[act],
                        'price':temp_product[current_product[act]]['price']
                    }
                    print('\033[1;32;1m您将【%s】加入购物车。\033[0m'%(current_product[act]))
                    #print(shopping_list)
                    continue
            else:
                print('指令错误！')
                continue
        elif act == 'q':
            with open('users.txt','r') as  u_info:
                users_info = json.loads(u_info.read())
            temp_user[1]['salary'] = salary
            temp_user[1]['shopping'] = shopping_list
            print('您已购买如下商品'.center(38,'-'))
            print('|', '名称'.center(16, ' '), '|', '价格'.center(18, ' '), '|')
            print('-'*45)
            money = 0

            for i in range(len(shopping_list)):
                money = money + shopping_list[str(i)]['price']
                print('|',shopping_list[str(i)]['name'].center(18, ' '),'|',str('￥%d元'%(shopping_list[str(i)]['price'])).rjust(18, ' '), '|')
            tips = '\033[1;32;1m您一共消费【%d元】\033[0m'%(money)
            print(tips.center(50,'-'))
            users_info[temp_user[0]] = temp_user[1]
            with open('users.txt','w') as u_info:
                u_info.write(json.dumps(users_info,ensure_ascii=False))
            #print(users_info)
            flag = True

        flag = True
    return


if __name__ == '__main__':
    shopping()