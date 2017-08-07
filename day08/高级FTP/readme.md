# 高级FTP

## 使用python内置tkinter模块（UI）编写，UI界面拙略，见谅

shell版本和UI版本差不多，去掉UI加载使用client_class创建实例即可，固不再编写shell版本

----------

## 实现功能

- 用户密码使用sha1加密,测试账号`lmc`密码`123`，默认配额10MB
- 未提供注册功能，需要新增账户可以使用`server_class`中的`create_user()`函数，支持多用户登录
- 用户仅能访问服务器家目录`home`下的以个人用户名命名的文件夹
- 注册用户时可设置磁盘配额，以MB为单位
- UI界面中可双击选择下载的文件或者双击目录来切换文件夹
- 上传下载均会进行md5验证
- UI界面的Lable做了一个进度条，并根据传输数据的多少改变颜色
- 支持断点续传（检测同名文件是否存在）

---------------------------

## 实现思路

1. 创建UI，渲染模块框架
2. UI界面的每次操作转化为一个client请求，由client.class的实例提交到服务端
3. client获取结果返回给UI界面解析，并显示给用户



## About Me
```python
myname = 'MC.Lee'
mylink = 'limich.cn'
```
[我的博客](https://limich.cn)
QQ:289959141
E-mail:limich@aliyun.com

[代码GitHub地址](https://github.com/limingchang/python_study_task.git)

[代码国内码云同步地址](https://git.oschina.net/limich/python_study.git)