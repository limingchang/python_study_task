# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os,platform
from host_manage.models import UserInfo,HostInfo
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


    def check_sign(self,type_or_sign="auto"):
        if type_or_sign == "auto":
            access_token = self.request.POST.get("accessToken",None)
        else:
            access_token = type_or_sign
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
            self.res['errMsg'] = '签名过期'
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

    def add_host(self):
        print('add host')
        hostname = self.request.POST.get("hostname",None)
        hostaddr = self.request.POST.get("hostaddr", None)
        hostport = self.request.POST.get("hostport", None)
        hostroot = self.request.POST.get("hostroot", None)
        hostkey = self.request.POST.get("hostkey", None)
        host = HostInfo(name=hostname,ip=hostaddr,port=hostport,user=hostroot,pwd=hostkey)
        host.save()
        # 获取个人信息
        user_info = self.get_user_info()
        print(user_info)
        host.host_user.add(*user_info)
        self.res['errNum'] = 0
        self.res['errMsg'] = '新增主机'
        self.res['data'] = True
        print(host)
        return self.res


    def del_host(self):
        hostid = self.request.POST.get("id", None)
        print('删除主机：',hostid)
        host = HostInfo.objects.filter(id=hostid)
        host.delete()
        self.res['errNum'] = 0
        self.res['errMsg'] = '删除主机'
        self.res['data'] = True
        return self.res

    def get_user_info(self,type_or_user="auto"):
        if type_or_user == "auto":
            user = self.request.session.get("user", None)
        else:
            user = type_or_user
        user_info = UserInfo.objects.filter(user=user)
        return user_info


    def get_host(self):
        user = self.request.session.get("user", None)
        if user != None:
            user_info = UserInfo.objects.filter(user=user)
            host_info = user_info[0].hostinfo_set.all()
        else:
            host_info = []
        return host_info


    def get_host_list(self):
        host_info = self.get_host()
        host_list = []
        if len(host_info) > 0:
            for item in host_info:
                print(item.ip)
                temp_dict = {}
                temp_dict['id'] = item.id
                temp_dict['ip'] = item.ip
                temp_dict['name'] = item.name
                temp_dict['port'] = item.port
                host_list.append(temp_dict)
        else:
            host_list = []
        return host_list


    def check_ip_status(self,ip='192.168.0.3'):
        def get_os():
            '''
            获取系统类型
            :return:
            '''
            os = platform.system()
            if os == "Windows":
                return "n"
            else:
                return "c"

        def ping_ip(ip_str):
            cmd = ["ping", "-{op}".format(op=get_os()),
                   "1", ip_str]
            output = os.popen(" ".join(cmd)).readlines()
            flag = '停机'
            # print(output)
            for line in list(output):
                if not line:
                    continue
                new_line = str(line).upper().strip()
                # print(new_line)
                if new_line.find("TTL") >= 0:
                    n = new_line.find("TIME=")+5
                    flag = new_line.lower()[n:]
                    break
            return flag
        return ping_ip(ip)