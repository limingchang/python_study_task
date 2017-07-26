# -*- coding: utf-8 -*-
#作者：Mc.Lee
from user import *
from shopping_cart import *
import json

admin_act_list = ['商品管理','用户管理']
act_list = ['开始购物','注册用户','管理员登录']
#print(login())
def main():
    exit_flag = False
    while not exit_flag:
        print('欢迎使用购物系统'.center(50,'*'))
        for act in act_list:
            print(act_list.index(act),act)
        act = input('请输入数字进入下一步(或输入q退出）：')
        if act.isdigit():
            act = int(act)
            if act < len(act_list) and act >= 0:
                if act == 0:
                    shopping()
                    #print('shopping...')
                elif act == 1:
                    if register():print('\033[1;32;1m注册成功,请重新登录继续操作！\033[0m')
                elif act == 2:
                    admin()
                    #print('admin...')
            else:
                print('指令错误！')
                continue
        elif act == 'q':
            print('谢谢光临！')
            exit_flag = True
            continue
        else:
            print('指令错误！')
            continue

    return


def admin():
    flag = False
    temp_user = login()
    while not flag:
        if temp_user[1]['authority'] == 9:
            print('系统管理'.center(50,'*'))
            print('1.新增商品\n2.用户管理\n')
            act = input('欢迎管理员【%s】,请输入指令继续操作：'%(temp_user[0]))
            if act == '1':
                admin_product()
            elif act == '2':
                print('\033[1;31;1madmin_user模块待有时间再制作...谢谢使用！\033[0m')
                continue
            else:
                print('指令错误！')
                continue
        else:
            print('\033[1;31;1m您不是管理员，滚粗！\033[0m')
            flag = True
            continue
        flag = True

    return


def admin_product():
    print('新增商品（q退出）'.center(50,'*'))
    print('|','名称'.center(18,' '),'|','价格'.center(18,' '),'|')
    with open('product.txt','r') as p_info:
        temp_product = json.loads(p_info.read())
        #print(type(temp_product))
    if len(temp_product) !=0:
        for product in temp_product:
            print('|',product.center(20,' '),'|',str('￥%d'%(temp_product[product]['price'])).rjust(20,' '),'|')
    else:
        print('暂无商品')
    print('-'*47)
    flag = False
    while not flag:
        product_name = input('请输入商品名称(q退出)：')
        if product_name == 'q':
            flag = True
            continue
        product_price = input('请输入商品价格：')
        product_title = input('请输入商品描述：')
        if not product_price.isdigit():
            print('\033[1;31;1m价格必须为整数！\033[0m')
            continue
        else:
            product_price =int(product_price)
            product = {
                'price':product_price,
                'title':product_title
            }
            temp_product[product_name] = product
            #print(temp_product)
            with open('product.txt','w') as p_info:
                p_info.write(json.dumps(temp_product,ensure_ascii=False))
            print('\033[1;32;1m新增【%s】成功！\033[0m'%(product_name))
    return


#if __name__ == '__mian__':
main()