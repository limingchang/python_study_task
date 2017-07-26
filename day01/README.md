# 第一周作业ReadMe

## 作业一

---

 - day1-test.py文件是登录模块程序
    - 输入命令`l`或者`login`(大小写均可）进行登录
    - 输入`q`退出
    - 密码错误3次锁定账号
 - users.txt存储账号信息
 - 修改bug

```pyrhon
#作者：Mc.Lee
if u_info[0] != username:
    i += 1 
    continue
```

 - `continue`前应加入`i += 1`否则导致写入时出错
 
```python
for line in content:
    line = line.rstrip('\n')
    content[i] = line
```
 - `line.rstrip('\n')`去除换行符，否则写入出错
 - 优化代码

```python
if u_info[2] == 3:
    print('Wrong password more than 3 times!')
    exit()
else:
    print('password error!')
    u_login()
```
### 三次错误强制退出
----------

## 作业二

 - day1-menu.py文件是三级菜单程序
    - 显示一级菜单（省份），输入中文省份名或对应数字进入二级菜单，输入`q`或`退出`结束程序
    - 输入中文市名或对应数进入三级菜单，输入`b`或`返回`回到菜单选择，输入`q`或`退出`结束程序
    - 三级菜单状态下输入`b`或`返回`回到菜单选择，输入`q`或`退出`结束程序

 - 优化
### 加入临时字典，同list一起输出
```python
i = 1
dic_key = {}
for level in menu_dic:
    dic_key[i] = level#创建临时字典
    print(i,'.',level)
    i += 1
```
### 加入`act`判断，数字和中文均可处理
```python
act = input('请输入你选择的省份（中文或数字）：')
if act.isdigit():
    act = dic_key[int(act)] #替换临时字典中的值给act
```
----------


## About Me
```python
myname = 'MC.Lee'
mylink = 'limich.cn'
```
[我的博客](https://limich.cn)
QQ:289959141
E-mail:limich@aliyun.com