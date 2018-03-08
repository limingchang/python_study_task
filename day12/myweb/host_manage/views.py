from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse,redirect
from api.auth_code import create_validate_code
from io import BytesIO
from base64 import b64encode
from api.host_manage import Host_API
import hashlib,time,json,random,string
from host_manage.models import UserInfo

def index(request):
    try:
        access_token = request.META['HTTP_ACCESSTOKEN']
    except KeyError:
        access_token = request.COOKIES.get("accessToken",None)
    # del request.session["user"]
    # print(access_token)
    user = request.session.get("user",None)
    if user == None:
        msg = "用户登录"
        url = "/login/"
        lg_out = ""
    else:
        user_info = UserInfo.objects.filter(user=user)
        msg = "欢迎，" + user_info[0].name
        url = ""
        lg_out = "退出登录"
    return render(request,"host_manage/index.html",{"msg":msg,"url":url,"lg_out":lg_out})



def login_out(request):
    request.session.clear()
    # msg = "用户登录"
    # url = "/login/"
    # lg_out = ""
    response = redirect('/index/')
    response.delete_cookie('accessToken')
    return response
    # return render(request, "host_manage/index.html", {"msg": msg, "url": url,"lg_out":lg_out})


def host(request):
    try:
        access_token = request.META['HTTP_ACCESSTOKEN']
    except KeyError:
        access_token = request.COOKIES.get("accessToken",None)

    print(access_token)
    res = Host_API(request).check_sign(type_or_sign=access_token)
    # print(res)
    # 判断是是否有签名访问
    if res["data"] == False:
        res_sign = False
    else:
        res_sign = True
    # 获取个人主机信息
    user = request.session.get("user",None)
    host_info = Host_API(request).get_host()
    for item in host_info:
        # item.status = Host_API(request).check_ip_status(ip=item.ip)
        # 太慢，弃用
        item.status = '停机'
    if len(host_info) == 0:
        host_info = False
    return render(request, "host_manage/host.html",{"sign":res_sign,"host_info":host_info})



def setting(request):
    pass



def api(request):
    if request.method == 'POST':
        act = request.POST.get("act",None)
    else:
        act = request.GET.get("act", None)

    print('API act:',act)

    if act == 'check_user':
        res = Host_API(request).check_user()
    elif act == 'register':
        res = Host_API(request).register()
    elif act == 'check_sign':
        res = Host_API(request).check_sign()
    elif act == 'add_host':
        access_token = request.META['HTTP_ACCESSTOKEN']
        chk = Host_API(request).check_sign(access_token)
        if chk["data"]:
            res = Host_API(request).add_host()
        else:
            res = chk
    elif act == 'del_host':
        access_token = request.META['HTTP_ACCESSTOKEN']
        chk = Host_API(request).check_sign(access_token)
        if chk["data"]:
            res = Host_API(request).del_host()
        else:
            res = chk
    elif act == 'check_ip_status':
        ip = request.POST.get("ip", None)
        chk = Host_API(request).check_ip_status(ip=ip)
        res = {
            "errNum": 0,
            "errMsg": "IP检测",
            "data": chk,
        }
    else:
        res = {
            "errNum": 301,
            "errMsg": "错误参数",
            "data": False,
        }

    return HttpResponse(json.dumps(res),content_type="application/json")
















def login(request):
    if request.method == 'POST':
        # print(request.META['HTTP_ACCESSTOKEN'])
        # print(request.POST)
        user = request.POST.get("user",None)
        pwd = request.POST.get("pwd",None)
        check_code = request.POST.get("auth_code",None)
        check_code = check_code.lower()
        server_check_code = request.session['check_code']
        server_check_code = server_check_code.lower()
        res = {}
        Hres = HttpResponse()
        if check_code == server_check_code:
            user_info = UserInfo.objects.filter(user=user)
            if user_info[0].user == user and user_info[0].pwd == pwd:
                # 颁发签证
                nonce = ''.join(random.sample(string.ascii_letters + string.digits, 16))
                key = user_info[0].key
                t = int(time.time())
                sign_array = [str(t), nonce, key]
                sign_str = "".join(sorted(sign_array))
                server_signature = hashlib.sha1(sign_str.encode()).hexdigest()
                # 保存签名并设置过期时间
                request.session['sign'] = server_signature
                request.session['sign_timeout'] = time.time()+3600*24 # 默认过期时间一天
                res = {
                    "errNum":0,
                    "errMsg":"ok",
                    "access_token":server_signature,
                }
                request.session['user'] = user
                Hres.set_cookie(key="accessToken", value=server_signature, expires=time.time() + 36000)
            else:
                res = {
                    "errNum": 100,
                    "errMsg": "用户名或密码错误",
                }
        else:
            res = {
                "errNum": 102,
                "errMsg": "验证码错误",
            }
        time.sleep(1)
        Hres.content = json.dumps(res)
        Hres.content_type = 'application/json'
        return Hres
    else:
        auth_code(request)
    return render(request,'host_manage/login.html')


def auth_code(request):
    f = BytesIO()
    img, code = create_validate_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    img_data = b64encode(f.getvalue())
    return HttpResponse(img_data)