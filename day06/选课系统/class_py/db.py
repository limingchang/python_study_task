# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'

import sys,os,re
import configparser,pickle

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)


class DB_CLASS(object):
    def __init__(self):
        self.Sep = os.sep#获取系统路径分隔符
        config = configparser.ConfigParser()
        #config_path = '%s\config\config.ini'%(path)
        config_path = '{_path}{_sep}config{_sep}config.ini'.format(_path=path,_sep=self.Sep)
        #print(config_path)
        config.read(config_path)
        self.DB_Type = config['DEFAULT']['db_type']
        self.DB_Name = config['DEFAULT']['db_name']
        self.DB_Link = config['DEFAULT']['db_link']
        self.Conn = self.db_handler()
        if self.DB_Type == 'file':
            self.DB_Index = self.get_db_index()



    def db_handler(self):
        '''
        数据库链接处理
        :return: 返回数据库连接对象
        '''
        if self.DB_Type == 'file':
            try:
                index_path = '{_path}{_sep}{_dbname}{_sep}db_index.dat'.format(_path=path, _sep=self.Sep,_dbname=self.DB_Name)
                conn = open(index_path, 'rb')
            except FileNotFoundError:
                print('数据表索引丢失，请联系管理员！')
                conn = None
                return conn
            else:
                return conn
        elif self.DB_Type == 'mysql':
            pass
        else:
            print('数据库连接失败！')


    def db_close(self):
        self.Conn.close()


    def get_db_index(self):
        '''
        获取文件数据索引，仅数据库类型为file适用
        :return: 返回索引字典
        '''
        db_index = {
            'course_list':[],
            'school_list':[],
            'class_list':[],
            'role_list':[]
        }
        if self.DB_Type == 'file':
            f = self.Conn
            if f == None:
                index_path = '{_path}{_sep}{_dbname}{_sep}db_index.dat'.format(_path=path,_sep=self.Sep,_dbname=self.DB_Name)
                with open(index_path, 'wb')as f:
                    pickle.dump(db_index, f)
            else:
                db_index = pickle.load(f)
                self.db_close()
        else:
            print('数据库类型错误：%s不适用此方法！'%self.DB_Type)
        return db_index

    def GET_DATA(self,statement):
        '''
        获取数据
        :param statement: 查询语句
        :return: 返回查询到的数据
        '''
        if self.DB_Type == 'file':
            #select school_id(*) from school
            key_table = self.Check_select_sql(statement)
            item_list = self.DB_Index['%s_list' %key_table[1]]
            if key_table[0] == '*':
                data = []
                for key in item_list:
                    filename = '%s%s.dat' % (key_table[1], item_list.index(key))
                    try:
                        info_path ='{_path}{_sep}{_dbname}{_sep}{_filename}'.format(_path=path,_sep=self.Sep, _dbname=self.DB_Name, _filename=filename)
                        f = open(info_path,'rb')
                    except FileNotFoundError:
                        data.append('')
                    else:
                        data.append(pickle.load(f))
                        f.close()
            else:
                data_id = item_list.index(key_table[0])
                filename = '%s%s.dat'%(key_table[1],data_id)
                try:
                    info_path = '{_path}{_sep}{_dbname}{_sep}{_filename}'.format(_path=path, _sep=self.Sep,_dbname=self.DB_Name,_filename=filename)
                    f = open(info_path, 'rb')
                except FileNotFoundError:
                    data = []
                else:
                    data = pickle.load(f)
                    f.close()
            return data
        elif self.DB_Type == 'mysql':
            pass
        else:
            pass

    def SAVE_TABLE_DATA(self,statement='update_file',data=[]):
        '''
        保存表数据
        :param statement:mysql类型为sql语句，file类型为update_file
        :param data: [tabel,key,data],仅文件类型使用此参数
        :return:
        '''
        if self.DB_Type == 'file':
            if statement == 'update_file':
                file_id = self.DB_Index['%s_list'%data[0]].index(data[1])
                filename = '%s%s.dat'%(data[0],file_id)
                info_path = '{_path}{_sep}{_dbname}{_sep}{_filename}'.format(_path=path, _sep=self.Sep,_dbname=self.DB_Name,_filename=filename)
                f = open(info_path ,'wb')
                pickle.dump(data[2],f)
                f.close()
                return True
            else:
                print('执行参数错误！')
                return False
        elif self.DB_Type == 'mysql':
            pass
        else:
            pass


    def SAVE_DB_INDEX(self,data):
        '''
        保存数据库索引，仅file类型数据适用
        :param data: [index_name,list],index_name索引名称，list要保存的索引数据列表
        :return:
        '''
        if self.DB_Type == 'file':
            self.DB_Index['%s_list'%data[0]] = data[1]
            index_path = '{_path}{_sep}{_dbname}{_sep}db_index.dat'.format(_path=path, _sep=self.Sep,_dbname=self.DB_Name)
            f = open(index_path,'wb')
            pickle.dump(self.DB_Index,f)
            f.close()
            return True
        else:
            print('数据库类型错误：%s不适用此方法！' % self.DB_Type)
            return False


    def Check_select_sql(self,sql):
        res = re.search(r'select\s+((\w*,)*(\w+)?)?(\*)?\s+from\s+\w+', sql)
        if res is None:
            print('语法错误！')
        else:
            keys_table = res.group()
            keys = keys_table.replace('select', '')
            keys = keys.split('from')
            table = keys[1].strip()
            keys = keys[0].strip()
            return keys,table



if __name__ == "__main__":
    d1 = DB_CLASS()
    print(d1.DB_Index)
    #d1.get_role_id()


