from django.shortcuts import render,HttpResponse
import json
from app01 import models

# Create your views here.
def index(request):
    user_list = models.UserInfo.objects.all()
    # print(user_list)
    group_list = models.UserGroup.objects.all()
    return render(request,'user.html',{'userlist':user_list,'grouplist':group_list})


def group(request):
    group_list = models.UserGroup.objects.all()
    # print(group_list)
    return render(request,'group.html',{'grouplist':group_list})

def api(request):
    data = request.POST
    print(data)
    act = request.POST.get('act',None)
    res = {
        'errNum':401,
        'errMsg':'非法调用API',
    }
    if act == 'add_user':
        user = request.POST.get('user',None)
        pwd = request.POST.get('pwd',None)
        email = request.POST.get('email', None)
        user_group_id = request.POST.get('user_group', None)
        models.UserInfo.objects.create(
            user=user,
            pwd=pwd,
            email=email,
            group_id=user_group_id,
        )
        res = {
            'errNum':0,
            'errMsg':'创建用户成功',
        }
    elif act == "del_user":
        id = request.POST.get('id',None)
        user = models.UserInfo.objects.filter(id=id).first()
        user.delete()
        res = {
            'errNum': 0,
            'errMsg': '删除用户成功',
        }
    elif act == "add_group":
        group_caption = request.POST.get('group_name',None)
        group_description = request.POST.get('description',None)
        models.UserGroup.objects.create(
            caption = group_caption,
            description = group_description,
        )
        res = {
            'errNum': 0,
            'errMsg': '创建组成功',
        }
    elif act == "del_group":
        group_id = request.POST.get('group_id',None)
        users = models.UserInfo.objects.filter(group_id=group_id).update(group_id="")
        group = models.UserGroup.objects.filter(id=group_id).first()
        group.delete();
        res = {
            'errNum': 0,
            'errMsg': '删除组成功',
        }
    elif act == "edit_group":
        group_id = request.POST.get('group_id', None)
        group_name = request.POST.get('group_name', None)
        group_description = request.POST.get('description', None)
        group = models.UserGroup.objects.filter(id=group_id)[0]
        group.caption = group_name
        group.description = group_description
        group.save()
        print(group)
        # group.update()
        res = {
            'errNum': 0,
            'errMsg': '修改组成功',
        }
    return HttpResponse(json.dumps(res), content_type="application/json")