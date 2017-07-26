# 作业：ATM

 - 程序介绍
    - 用户数据、商品数据、信用卡使用json存储；
    - 测试账号：`lmc`,密码`123`，有管理员权限，请在自行添加用户测试
    - 用户初始现金、信用卡初始额度自定义
    - 实现了ATM的基本功能
    - 用到了os,sys,json,hashlib,time,datetime模块

---

 - 程序结构
```
   ATM
    │  __init__.py
    │  
    ├─admin
    │  │  card_manage.py #信用卡管理接口
    │  │  manage.py #管理系统接口
    │  └  __init__.py  
    │        
    ├─bin
    │  │   atm.py #程序主入口
    │  └   __init__.py
    │      
    ├─conf
    │      __init__.py
    │      
    ├─core
    │  │  card.py #用户信用卡逻辑
    │  │  main.py #程序主逻辑交互
    │  │  shopping.py #购物程序逻辑
    │  │  user.py
    │  └  __init__.py
    │          
    └─db
        │ cards.txt #信用卡数据
        │ card_log.txt #信用卡日志
        │ products.txt #商品数据
        │ users.txt #用户数据
        │ user_log.txt #用户日志
        └ __init__.py
```            

## About Me
```python
myname = 'MC.Lee'
mylink = 'limich.cn'
```
[我的博客](https://limich.cn)
QQ:289959141
E-mail:limich@aliyun.com