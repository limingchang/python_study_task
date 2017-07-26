# 选课系统

-----

 - 测试账号`admin`,密码`admin`,管理员权限；`lmc`,密码`123`,讲师权限。
 - 使用类编程模式编写，创建角色接口类`ROLE_INTERFACE`，数据库操作类`db.py`，角色操作类`role.py`,组织（学校、班级、课程等）操作类`org.py`
 - 实现了作业要求的基本功能，时间关系，部分提示信息为设置颜色
 - 目录结构

```
选课系统
    ├─bin
    │  └─ main.py程序主入口
    │
    ├─class_py
    │  │  db.py数据库类模块
    │  │  org.py组织类模块
    │  │  role.py角色类模块
    │  └─ __init__.py
    │
    ├─config
    │  │   config.ini配置文件
    │  └─  __init__.py
    │
    ├─core
    │  │  index.py角色接口核心
    │  └─__init__.py
    │
    └─db数据库
        │  class0.dat
        │  course0.dat
        │  db_index.dat数据索引文件
        │  role0.dat
        │  school0.dat
        └─ __init__.py
```


## About Me
```python
myname = 'MC.Lee'
mylink = 'limich.cn'
```
[我的博客](https://limich.cn)
QQ:289959141
E-mail:limich@aliyun.com

