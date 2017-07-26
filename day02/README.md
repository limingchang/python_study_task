# 第二周作业-购物车

---

**文件列表**

 1. main.py为主程序入口；
 2. user.py为登录、注册功能模块；
 3. shopping_cart.py为购物车模块；
 4. product.txt记录商品信息，users.txt记录用户信息，使用utf-8编码，请不要用其他编辑器打开，会造成读取错误。
 3. 测试账号`lmc` 密码`pwd`(管理员权限），账号`alex` 密码`123`(普通权限）；

**功能**

 1. 主界面提供`购物` `注册用户` `管理员登录`三个功能,输入`q`可退出；
 2. 进入`购物`后输入账号密码即可进行（第一次购物需要输入工资），输入`q`退出并结账；
 3. 进入`注册用户`可新增用户，默认购物车为空，工资为空；
 4. 进入`管理员登录`输入`1`可进行`商品新增`,输入`2`可进行用户管理，欲设计`权限管理` `用户删除`功能（因非作业内容，暂未上传，待完善后上传）；

**流程图**

 - 用户登录

```flow
st=>start: 开始
e=>end: 登录
op=>operation: 输入用户名密码
cond=>condition: 是否有此用户
cond2=>condition: 是否已被锁死
cond3=>condition: 密码是否正确

st->op->cond
cond(yes)->cond2
cond(no)->op
cond2(yes)->op
cond2(no,left)->cond3(yes)->e
cond3(no)->op
```

---------------------------

 - 用户注册

```flow
st=>start: 开始
e=>end: 注册成功
op=>operation: 输入用户名密码
op2=>operation: 重复输入密码
cond=>condition: 用户是否被注册
cond2=>condition: 两次输入密码是否一致
op3=>operation: 写入users.txt

st->op->op2->cond
cond(no)->cond2
cond(yes,right)->op
cond2(no)->op
cond2(yes)->op3->e
```

---------------------------

 - 新增商品

```flow
st=>start: 开始
op_print=>operation: 打印已有商品列表
io_act=>operation: 输入商品名称
cond_exit=>condition: 是否输入q
op_price=>operation: 输入商品价格
op_title=>operation: 输入商品描述
cond_price=>condition: 价格是否是整数
op_write=>operation: 写入produc.txt
e=>end: 退出


st->op_print->io_act->cond_exit
cond_exit(yes)->e
cond_exit(no,left)->op_price->op_title->cond_price
cond_price(yes,right)->op_write(right)->io_act
cond_price(no)->io_act
```

---------------------------

 - 购物车

```flow
st=>start: 开始
sub_user=>subroutine: 调用登录模块
cond_salary=>condition: 判断工资有无
io_salary=>inputoutput: 输入工资
op_product=>operation: 输出商品列表
op_act=>operation: 选择商品
cond_act=>condition: 是否输入q
cond_sel=>condition: 是否正确序号
op_write=>operation: 写入users.txt
cond_salary2=>condition: 余额是否充足
op_act2=>operation: 记录临时商品列表
e=>end: 退出

st->sub_user->cond_salary
cond_salary(no)->io_salary->op_product
cond_salary(yes)->op_product
op_product->op_act->cond_act
cond_act(no,left)->cond_sel
cond_act(yes)->op_write->e
cond_sel(no,left)->op_act
cond_sel(yes)->cond_salary2
cond_salary2(no,left)->op_act
cond_salary2(yes)->op_act2->op_act
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