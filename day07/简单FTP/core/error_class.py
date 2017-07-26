# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

class Client_Error(Exception):
    def __init__(self,errcode,act):
        self.Err_Msg(errcode,act)

    def Err_Msg(self,errcode,act):
        if errcode == 0:
            self.message = '[客户端]执行[%s]成功'%act
        elif errcode == 2:
            self.message = '[客户端]执行[%s]错误:参数错误'%act
        elif errcode == 301:
            self.message = '[客户端]执行[%s]错误:本地文件不存在' % act
        elif errcode == 302:
            self.message = '[客户端]执行[%s]错误:本地文件超过最大可上传大小' % act
        else:
            self.message = '[客户端]执行[%s]错误:未知错误'%act

    def __str__(self):
        return self.message


class Server_Error(Exception):
    def __init__(self,errcode,act):
        self.Err_Msg(errcode,act)

    def Err_Msg(self,errcode,act):
        if errcode == 0:
            self.message = '[服务端]执行[%s]成功'%act
        elif errcode == -1:
            self.message = '[服务端]执行[%s]错误:\033[1;31;1m指令错误\033[0m'%act
        elif errcode == 1:
            self.message = '[服务端]执行[%s]错误:未登录用户不能操作'%act
        elif errcode == 100:
            self.message = '[服务端]执行[%s]成功:登录成功' % act
        elif errcode == 101:
            self.message = '[服务端]执行[%s]错误:用户名或密码错误' % act
        elif errcode == 102:
            self.message = '[服务端]执行[%s]错误:用户不存在' % act
        elif errcode == 2:
            self.message = '[服务端]执行[%s]错误:参数错误'%act
        elif errcode == 301:
            self.message = '[服务端]执行[%s]错误:本地文件不存在' % act
        elif errcode == 302:
            self.message = '[服务端]执行[%s]错误:文件超过最大可上传大小' % act
        elif errcode == 303:
            self.message = '[服务端]执行[%s]错误:云端文件不存在，请检查下载文件名参数' % act
        else:
            self.message = '[服务端]执行[%s]错误:未知错误'%act

    def __str__(self):
        return self.message

if __name__ == '__main__':
    def show_error(errcode,act):
        try:
            raise Client_Error(errcode,act)
        except Client_Error as e:
            print(e)

    show_error(0,'login')