# 静态购物商城

## 实现功能和作业要求：
- 完成电子商务网站页面（动态）（仿京东）

1. 主页部分
  - `:hover`纯CSS导航菜单
  - `float`瀑流商品布局
  - ``js左侧伸缩菜单
  - ``js图片自动切换
  - `@media screen`以1190px为临界实现两种布局

2. 注册页面
  - js部分表单验证

3. 登录页面
  - 登录页面和注册页面基本一致，前面写特效耗时太多，这个页面就不做了。

4. 一些记录
  - 字符超出元素长度以"..."结尾
```
overflow:hidden;
white-space: nowrap;
text-overflow: ellipsis;
//三个一起才能生效
```
  - `border-radius`设置边框圆角
---------
  - `box-shadow`设置阴影，参数如下：

```
none:无阴影
<length>①：第1个长度值用来设置对象的阴影水平偏移值。可以为负值
<length>②：第2个长度值用来设置对象的阴影垂直偏移值。可以为负值
<length>③：如果提供了第3个长度值则用来设置对象的阴影模糊值。不允许负值
<length>④：如果提供了第4个长度值则用来设置对象的阴影外延值。模糊半径
<color>：设置对象的阴影的颜色。
```
  - 单边阴影示例：`box-shadow: 0px 10px 10px -6px rgba(0,0,0,.2);`设置下边阴影，设置模糊半径要大于偏移值得一半

---------

  - `transition：[ transition-property ] || [ transition-duration ] || [ transition-timing-function ] || [ transition-delay ]`过度效果
   - 取值：
    - [ transition-property ]：检索或设置对象中的参与过渡的属性
    - [ transition-duration ]：检索或设置对象过渡的持续时间
    - [ transition-timing-function ]：检索或设置对象中过渡的动画类型
    - [ transition-delay ]：检索或设置对象延迟过渡的时间
   - 例`transition：left 2s ease-in .5s`；当left改变时，将从left初始位置移动到改变后位置，持续2秒，由慢到快，延迟0.5秒开始
   - linear：线性过渡。等同于贝塞尔曲线(0.0, 0.0, 1.0, 1.0)
    - ease：平滑过渡。等同于贝塞尔曲线(0.25, 0.1, 0.25, 1.0)
    - ease-in：由慢到快。等同于贝塞尔曲线(0.42, 0, 1.0, 1.0)
    - ease-out：由快到慢。等同于贝塞尔曲线(0, 0, 0.58, 1.0)
    - ease-in-out：由慢到快再到慢。等同于贝塞尔曲线(0.42, 0, 0.58, 1.0)

---------

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
