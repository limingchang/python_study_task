# 第三周作业

 - 文件列表
    1.info.txt存储工资信息；
    2.salary.py为主程序列表；
 - 功能
    1.实现题目要求基本功能；
    2.部分提示信息高亮+颜色显示；
    3.查询、新增、修改时忽略用户输入的首字母大写，即全大写、全小写均可，程序自动优化为首字母大写进行操作。
 - 后续可优化
    1.新增模块和修改模块还有重复代码，可分割为函数优化。

---

# 流程图


----------

 - 查询模块


```flow
st=>start: 开始
sub1=>subroutine: 获取员工信息子程序
io1=>inputoutput: 输入名字
op1=>operation: 格式化输入信息
cond=>condition: 名字是否在信息表内
op=>operation: 输出工资
e=>end: 结束

st->sub1->io1->op1->cond
cond(yes)->op->e
cond(no)->io1
```


----------

# 修改模块


----------

```flow
st=>start: 开始
sub1=>subroutine: 获取员工信息子程序
io1=>inputoutput: 输入修改信息
op1=>operation: 格式化输入信息
cond1=>condition: 信息格式是否正确
cond=>condition: 名字是否在信息表内
op=>operation: 写入info文件
e=>end: 结束

st->sub1->io1->op1->cond1
cond1(yes)->cond
cond1(no)->io1
cond(no,right)->io1
cond(yes)->op->e
```


----------
# 新增模块

 - 此模块实现代码仅在判断员工是否已有的时候和修改模块不同，流程图就简单画这部分


----------
```flow
st=>start: 开始
op1=>operation: 前置代码
cond=>condition: 名字是否在信息表内
op=>operation: 写入info文件
e=>end: 结束

st->op1->cond
cond(yes,right)->op1
cond(no)->op->e
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