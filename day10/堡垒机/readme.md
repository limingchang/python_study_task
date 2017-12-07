作业要求：
所有的用户操作日志要保留在数据库中
每个用户登录堡垒机后，只需要选择具体要访问的设置，就连接上了，不需要再输入目标机器的访问密码
允许用户对不同的目标设备有不同的访问权限，例:
对10.0.2.34 有mysql 用户的权限
对192.168.3.22 有root用户的权限
对172.33.24.55 没任何权限
分组管理，即可以对设置进行分组，允许用户访问某组机器，但对组里的不同机器依然有不同的访问权限　

用户连接：
1.用户登陆后记录一条login数据，操作的每条命令按确认键后记录到数据库
2.登陆堡垒机后，根据输入相应的IP地址和用户名进行远程连接，如果输入的地址和用户名不在该用户的权限范围内，则会提示没有权限

数据管理：
1.添加相关的数据：堡垒机用户、主机、主机组、登陆主机的帐户
2.关联：主机和登陆帐户的绑定、用户和绑定后主机的关联、用户和主机组的关联、绑定后的主机和主机组的关联
3.用户只有关联绑定主机或关联主机组，才可以登陆到相应的主机

目录结构：
<Fortress_machine>
├__init__.py
├readme.md
├<bin>
│  ├__init__.py
│  ├login_start.py            #堡垒机用户连接远端主机入口
│  └manage_start.py           #添加数据管理入口
├<conf>
│  ├__init__.py
│  ├db_conn.py                #数据库连接
│  ├set.py                    #数据库连接地址
├<core>
│  ├__init__.py
│  ├database_table.py        #每个表的设置
│  ├manage_views.py          #管理主逻辑
│  ├views.py                 #选择登陆主机逻辑
├<demos>                      #在源代码上稍微修改后可以自动远程SSH连接主机，不需要输入密码，并将操作命令的数据记录在数据库
│  ├__init__.py
│  ├demo.log
│  ├demo.py
│  ├demo_keygen.py
│  ├demo_server.py
│  ├demo_sftp.py
│  ├demo_simple.py
│  ├forward.py
│  ├interactive.py
│  ├rforward.py
│  ├test_rsa.key
│  ├user_rsa_key
│  ├user_rsa_key.pub
├<log>
│  └__init__.py