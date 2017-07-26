# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import re,json,time
import configparser
primary_key = ''
auto_incremrnt = ''
key_index = ''

def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    global primary_key
    global auto_incremrnt
    global key_index
    primary_key = config['db_config']['primary_key']
    auto_incremrnt = config['db_config']['auto_incremrnt']
    key_index = json.loads(config['db_config']['key_index'])


def check_sql(sql):
    sql = sql.strip()
    sql = sql.lower()
    if sql.startswith('select'):
        print('检测到查询语句：',sql)
        sql_search(sql)
    elif sql.startswith('insert'):
        print('检测到插入语句：', sql)
        sql_insert(sql)
    elif sql.startswith('update'):
        print('检测到更新语句：', sql)
        sql_update(sql)
    elif sql.startswith('delete'):
        print('检测到删除语句：', sql)
        sql_delete(sql)
    else:
        print('不是SQL语句或未设置此功能！')

def get_data(table,keys,limit):
    '''
    获取数据
    :param table: 表名/文件名
    :param keys:字段 
    :param limit: 限制条件
    :return: 
    '''
    temp_data = get_table_data(table)
    limit_list = limit_parse(limit)
    a = limit_data(temp_data,keys,limit_list)
    print(a)
    print('查询到%d条数据。'%(len(a)))





def limit_data(temp_data,keys,limit):
    res_data = {}
    key_list = []
    if '*' in keys:
        for key in key_index:
            key_list.append(key)
    else:
        key_list = keys.split(',')
    for item in temp_data:
        res_data[item[key_index[primary_key]]] = {}
        for index in key_index:
            if primary_key != index and index in key_list:
                res_data[item[key_index[primary_key]]][index] = item[key_index[index]]

    return final_data(res_data,limit)


def final_data(temp_data,limit):
    res_data = {}
    if limit[2] == '=':
        for item in temp_data:
            if temp_data[item][limit[0]].lower() == str(limit[1]):
                res_data[item] = temp_data[item]
    elif limit[2] == '<':
        for item in temp_data:
            if temp_data[item][limit[0]] < str(limit[1]):
                res_data[item] = temp_data[item]
    elif limit[2] == '>':
        for item in temp_data:
            if temp_data[item][limit[0]] > str(limit[1]):
                res_data[item] = temp_data[item]
    elif limit[2] == 'like':
        for item in temp_data:
            if str(limit[1]) in temp_data[item][limit[0]].lower():
                res_data[item] = temp_data[item]
    return res_data




def limit_parse(limit):
    limit_keys = ['>','<','=','like']
    limit = limit.replace(' ','')
    for key in limit_keys:
        if key in limit:
            res = limit.split(key)
            res[1] = eval(res[1])
            res.append(key)
    return res








def sql_search(sql):
    #res = re.search(r'select\s+\w*\**\s+from\s+\w+',sql)
    res = re.search(r'select\s+((\w*,)*(\w+)?)?(\*)?\s+from\s+\w+', sql)
    if res is None:
        print('语法错误！')
    else:
        keys_table = res.group()
        keys = keys_table.replace('select','')
        keys = keys.split('from')
        table = keys[1].strip()
        keys = keys[0].strip()
        limit = sql.split(res.group())[-1].replace('where','').strip()
        get_data(table, keys, limit)



def sql_insert(sql):
    res = re.search(r'insert\s+into\s+\w+',sql)
    if res is None:
        print('语法错误！')
    else:
        table_name = res.group()
        table_name = table_name.split(re.search(r'insert\s+into\s+',table_name).group())
        table_name = table_name[-1].strip()
        arr = sql.split(res.group())
        values = re.search(r'\([^()]+\)',arr[-1])
        if values is None:
            print('语法错误！')
        else:
            values = values.group().rstrip(')').lstrip('(').split(',')
            insert_data(table_name, values)


def insert_data(table_name,values):
    print(table_name)
    print(values)
    temp_data = get_table_data(table_name)
    data = []
    if len(values) != len(key_index)-2:
        print('缺少字段（name,age,phone,job）！')
    else:
        count = len(temp_data)
        date = time.strftime("%Y-%m-%d")
        data.append(str(count+1))
        data.append(values[0])
        data.append(values[1])
        data.append(values[2])
        data.append(values[3])
        data.append(date)
        temp_data.append(data)
        write_table(temp_data, table_name)


def sql_delete(sql):
    res = re.search(r'delete\s+\d+', sql)
    if res is None:
        print('语法错误！')
    else:
        staff_id = sql.replace('delete','').strip()
        temp_data = get_table_data('staff_table')
        for item in temp_data:
            if item[0] == staff_id:
                temp_data.remove(item)
        write_table(temp_data,'staff_table')
        print('删除成功!')

def sql_update(sql):
    res = re.search(r'update\s+\w+\s+set\s+',sql)
    if res is not None:
        table_name = res.group()
        table_name = table_name.split(re.search(r'update\s+\w+\s+set\s+', table_name).group())
        table_name = table_name[-1].strip()
        print(table_name)


def get_table_data(table):
    temp_data = []
    with open('%s.txt' % (table), 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            line = line.strip()
            temp_data.append(line.split(','))
            line = f.readline()
    return temp_data



def write_table(temp_data,table):
    write_str = ''
    for item in temp_data:
        print(item)
        data_str = ','.join(item)
        write_str = '%s%s\n' % (write_str, data_str)
    with open('%s.txt' % (table), 'w', encoding='utf-8') as f:
        f.write(write_str)


if __name__ == '__main__':
    sql = input('请输入语句：')
    get_config()
    check_sql(sql)
