# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'

import re

def calculator(formula):
    formula = formula.strip()
    formula = formula.replace(' ','')
    flag = False
    while not flag:
        if '(' in formula:
            get_formula = re.search(r'\(([^()]+)\)',formula)
            if get_formula is not None:
                get_formula = get_formula.group()
                print('提取：',get_formula)
                result = recount(get_formula)
                formula = re.sub(r'\(([^()]+)\)',str(result),formula,1)
                print('替换为：',formula)
                continue
        else:
            result = recount(formula)
            print("计算结果：",result)
            flag = True
            break




def recount(formula):
    formula = formula.lstrip('(')
    formula = formula.rstrip(')')
    if '*' in formula:
        print('计算*:',formula)
        formula = mul_div(formula)
        print(formula)
        return recount(formula)
    elif '/' in formula:
        print('计算/:', formula)
        formula = mul_div(formula)
        print(formula)
        return recount(formula)
    else:
        get_formula = re.search(r'\d+\.?\d*[\+\-]+\d+\.?\d*',formula)
        if get_formula is not None:
            print('计算+-:',formula)
            formula = add_sub(formula)
            return formula
        else:
            return formula



def mul_div(formula):
    '''
    计算乘除
    :param formula:
    :return:
    '''
    flag = False
    while not flag:
        get_formula = re.search(r'\d+\.?\d*[\*\/]\-?\d+\.?\d*', formula)
        if get_formula is not None:
            get_formula = get_formula.group()
            if '*' in get_formula:
                mul_arr = get_formula.split('*')
                result = float(mul_arr[0]) * float(mul_arr[1])
            elif '/' in get_formula:
                div_arr = get_formula.split('/')
                result = float(div_arr[0]) / float(div_arr[1])
            else:
                result = get_formula
            formula = re.sub(r'\d+\.?\d*[\*\/]\-?\d+\.?\d*',str(result),formula,1)
            continue
        else:
            flag = True
            break
    return formula


def add_sub(formula):
    formula = formula.replace(' ', '')
    formula = formula.replace('--','+')
    formula = formula.replace('+-', '-')
    get_sum = re.findall(r'-?\d+\.?\d*', formula)
    print(get_sum)
    sum_arr = []
    for n in get_sum:
        sum_arr.append(float(n))
    return sum(sum_arr)



if __name__ == '__main__':
    formula = input('请输入算式：')
    calculator(formula)
    #print( '*' or '/' in '-8.0')