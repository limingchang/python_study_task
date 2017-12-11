
# 静态购物商城

## 实现功能和作业要求：
 - 按样品网页完成所有效果
 > 一些坑：
 > 1.input标签在div中被认为是文字，按钮和输入框的间距可设置font-size=0使其两两相连（无间距）,再后面记得调回来，否则包含的子标签看不到文字
 > 2.ul类标签（列表），可设置dispaly:inline-block使其变为可调整区域，设置列表项（li dd dt 等）为inline-block可去除列表前面的点，然后调整margin可设置对其（默认margin有值）
 > 3.不要忘记清除浮动<div style="clear:both"></div>
 > 求助项：
 > 凹陷型的线条
 > a标签不同状态的设置
-------

## 一些代码

```html
/*圆角边框*/
border-radius:5px 5px 5px 5px;/*设置上左 上右 下左 下右边框圆角弧度*/

/*插入伪元素*/
:after{
    content:"更多选项";
    position:absolute;
    top:195px;
    left:50%;
    width:90px;
    height:18px;
    margin-left:-45px;
    padding-left:10px;
    font-size:12px;
    line-height:18px;
    border-radius:0 0 5px 5px;
    border:1px solid #dddddd;
    border-top:1px solid #F0FFFF;
}

/*伪元素气泡提示*/

.hot{
    width:3%;
    margin-left:-8%;
    margin-top:-8px;
    float:left;
    height:15px;
    background-color:#FF8C00;
    font-size:12px;
    text-align:center;
    line-height:15px;
    border-radius:5px;
    position:relative;/*让其after或before伪元素依靠它绝对定位*/
    z-index:9;
}
.hot div{
    position:absolute;
    top:0;
    left:3px;
}
.hot:after{/*生成伪元素三角箭头*/
    content: "";/*不管有没有内容，必须写的一句话*/
    width:0;
    height:0;
    position:absolute;/*伪元素必须依靠生成其的标签进行绝对定位*/
    top:15px;
    left:5px;
    border:3px solid transparent;/*transparent-透明*/
    border-top-color:#FF8C00;/*其他三边透明，只显示一边*/
}
```



------

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
