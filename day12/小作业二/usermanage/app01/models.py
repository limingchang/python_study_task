from django.db import models

# Create your models here.

class UserInfo(models.Model):
    user = models.CharField(
        max_length=32,
        verbose_name='用户名'
    )
    pwd = models.CharField(max_length=32)
    email = models.EmailField()
    group = models.ForeignKey('UserGroup',blank=True, null=True,on_delete=models.SET_NULL)
    ctime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user

class UserGroup(models.Model):
    caption = models.CharField(max_length=64)
    description = models.TextField()
    def __str__(self):
        return self.caption + '|' +self.description