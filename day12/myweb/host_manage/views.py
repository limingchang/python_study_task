from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from api.auth_code import create_validate_code
from io import BytesIO
from base64 import b64encode
import hashlib,time,json,random,string


def index(request):
    try:
        access_token = request.META['HTTP_ACCESSTOKEN']
    except KeyError:
        access_token = None
    print(access_token)
    return render(request,"host_manage/index.html")


def login(request):
    if request.method == 'POST':
        # print(request.META['HTTP_ACCESSTOKEN'])
        print(request.POST)
        user = request.POST.get("user",None)
        pwd = request.POST.get("pwd",None)
        check_code = request.POST.get("auth_code",None)
        check_code = check_code.lower
        res = {}
        if user == "lmc" and pwd =="40bd001563085fc35165329ea1ff5c5ecbdbbeef":
            nonce = ''.join(random.sample(string.ascii_letters + string.digits, 16))
            key = 'key'
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
        else:
            res = {
                "errNum": 100,
                "errMsg": "password error",
            }
        print(res)
        time.sleep(1)
        return HttpResponse(json.dumps(res), content_type='application/json')
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