from django.db import models

# Create your models here.


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=18)
    # 用户名，最长18个字符
    pwd = models.CharField(max_length=40)
    # 用户密码，sha1加密字符串，40长度
    name = models.CharField(max_length=12)
    tel = models.CharField(max_length=11)
    key = models.CharField(max_length=16)

    def __str__(self):
        return self.user


class HostInfo(models.Model):
    # 主机信息表
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(protocol="ipv4")
    # ipV4地址
    port = models.IntegerField()
    # host_user = models.ManyToManyField(UserInfo,through='UserHost')
    host_user = models.ManyToManyField(UserInfo)
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

    def __str__(self):
        msg = self.name + " | " + self.ip + " : " + str(self.port)
        return msg


#
# class UserHost(models.Model):
#     #主机和管理者对应关系
#     uid = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
#     hid = models.ForeignKey(HostInfo,on_delete=models.CASCADE)
