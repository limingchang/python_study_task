# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os
from host_manage.models import UserInfo
import hashlib,time,json,random,string



class Host_API(object):
    '''

    '''
    def __init__(self,request):
        self.request = request
        self.res = {
            "errNum":0,
            "errMsg":"",
            "data":"",
        }



    def check_user(self):
        user = self.request.POST.get("user", None)
        user_info = UserInfo.objects.filter(user=user)
        if len(user_info) == 0:
            self.res['errMsg']='用户名可用'
            self.res['data'] = True
        else:
            self.res['errNum'] = 100
            self.res['errMsg'] = '用户名已被注册'
            self.res['data'] = False
        return self.res


    def check_sign(self):
        access_token = self.request.POST.get("accessToken",None)
        server_time = time.time()
        server_sign = self.request.session.get("sign",None)
        sign_timeout = self.request.session.get("sign_timeout",None)
        if access_token == None or server_sign == None:
            self.res["errNum"] = 201
            self.res["errMsg"] = "签名错误"
            self.res['data'] = False
        elif access_token != server_sign:
            self.res['errNum'] = 202
            self.res['errMsg'] = '签名错误'
            self.res['data'] = False
        elif server_time > sign_timeout:
            self.res['errNum'] = 203
            self.res['errMsg'] = '签名失效'
            self.res['data'] = False
        else:
            self.res['errNum'] = 0
            self.res['errMsg'] = '签名认证成功'
            self.res['data'] = True
        return self.res


    def register(self):
        user = self.request.POST.get("user", None)
        pwd = self.request.POST.get("pwd", None)
        name = self.request.POST.get("name", None)
        tel = self.request.POST.get("tel", None)
        key = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        # 随机16位字符串key
        person = UserInfo(user=user,pwd=pwd,name=name,tel=tel,key=key)
        person.save()
        self.res['errNum'] = 0
        self.res['errMsg'] = '用户注册成功'
        self.res['data'] = True
        return self.res



    def get_host(self):
        pass
