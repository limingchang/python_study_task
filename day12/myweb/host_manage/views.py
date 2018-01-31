from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from api.auth_code import create_validate_code
from io import BytesIO
from base64 import b64encode

def login(request):
    if request.method == 'POST':
        print(request.META['HTTP_ACCESSTOKEN'])
    else:
        auth_code(request)
    return render(request,'login.html')


def auth_code(request):
    f = BytesIO()
    img, code = create_validate_code()
    # request.session['check_code'] = code
    img.save(f, 'PNG')
    img_data = b64encode(f.getvalue())
    # img_data = str(b64encode(f.getvalue()))
    #去除编码后的base64字符串前后b''，以便前端使用
    # img_data = img_data.replace("b'", "")
    # img_data = img_data.replace("'", "")
    return HttpResponse(img_data)