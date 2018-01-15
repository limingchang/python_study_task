//var l_items = document.getElementsByClassName("l-item");
//console.log(l_items);
var menu_group = document.getElementsByClassName("leftout-group");
function iscontains(father, children) {
    if (document.all) {
        if (father.contains(children)) {
            return true;
        }
    } else {
        var reg = father.compareDocumentPosition(children);
        if (reg == 20 || reg == 0) {
            return true;
        }
    }
    return false;
}
function mOver(obj){
    var target_data = obj.attributes["target-data"].value;
    console.log("显示："+target_data);
    var ele = document.getElementById(target_data);
    if(ele==null){
        return;
    }
    //显示当前菜单，并将非当前菜单取消显示
    for(var i=0;i<menu_group.length;i++){
        //var e_id = 'group'+i
        //var e = document.getElementById(e_id);
        if(ele==menu_group[i]){
            //console.log(e_id);
            menu_group[i].style.display="block";
        }else{
            menu_group[i].style.display="none";
        }
    }
    //阻止menu_group对象中由父级移动向子级时触发onmouseout
    ele = document.getElementById(target_data);
    ele.onmouseout = function(eve){
        var eve = window.event || eve;
        var s = eve.toElement || eve.relatedTarget;
        if (!iscontains(this, s)){
            ele.style.display = "none";
        }
    }

}
function Get_target_element(obj){
    var target_data = obj.attributes["target-data"].value;
    var e = document.getElementById(target_data);
    return e;
}
var btn_list = document.getElementsByClassName("btn-circle");
var img_list = document.getElementsByClassName("img-lk");
function img_switch(obj){
    var img_list = document.getElementsByClassName("img-lk");
    var e = Get_target_element(obj);
    remove_sel();
    for(var i=0;i<img_list.length;i++){
        if(img_list[i]==Get_target_element(obj)){
            img_list[i].style.zIndex=10;
            btn_list[i].classList.add('btn-circle-sel');
        }else{
            img_list[i].style.zIndex=1;
        }
    }
}

img_list[0].style.zIndex=10;
btn_list[0].classList.add('btn-circle-sel');
function img_next(type){
    for(var i=0;i<img_list.length;i++){
        if(type=="left" && img_list[i].style.zIndex==10){
            img_list[i].style.zIndex=1;
            remove_sel();
            if(i==0){
                img_list[img_list.length-1].style.zIndex=10;
                btn_list[img_list.length-1].classList.add('btn-circle-sel');
            }else{
                img_list[i-1].style.zIndex=10;
                btn_list[i-1].classList.add('btn-circle-sel');
            }
            break;
        }else if(type=="right" && img_list[i].style.zIndex==10){
            img_list[i].style.zIndex=1;
            remove_sel();
            if(i==img_list.length-1){
                img_list[0].style.zIndex=10;
                btn_list[0].classList.add('btn-circle-sel');
            }else{
                img_list[i+1].style.zIndex=10;
                btn_list[i+1].classList.add('btn-circle-sel');
            }
            break;
        }//else{
           //img_list[0].style.zIndex=10;
           //for(var j=1;j<img_list.length;j++){
                //img_list[j].style.zIndex=1;
           //}
           //break;
        //}
    }
}
function remove_sel(){
    for(var i=0;i<btn_list.length;i++){
        btn_list[i].classList.remove('btn-circle-sel');
    }
}
var Int;
var fk_img_int;
function load(){

    Int = setInterval("img_next('right');",3000);
    fk_img_int = setInterval("fk_img_auto();",2000);
    img_star_stop(Int);

}

function img_star(){
    Int = setInterval("img_next('right');",3000);
}
function img_stop(){
    window.clearInterval(Int);
}
function img_star_stop(){
    //window.clearInterval(int)
    for(var i=0;i<img_list.length;i++){
        img_list[i].onmouseover=function(){
            img_stop(Int);
        }
        img_list[i].onmouseout=function(){
            img_star();
        }
        btn_list[i].onmouseout=function(){
            btn_list[i].classList.remove('btn-circle-sel');
        }
    }
}
//新闻栏移动下划线
var news_tit = document.getElementsByClassName("news-tit-left");
function move_line(obj){
    var news_line = document.getElementById("line1");
    if(obj.offsetLeft==10){
        news_line.style.left="10px";
        var ele = document.getElementById("tab1");
        ele.style.display="block";
        ele = document.getElementById("tab2");
        ele.style.display="none";
    }else{
        news_line.style.left="55px";
        var ele = document.getElementById("tab2");
        ele.style.display="block";
        ele = document.getElementById("tab1");
        ele.style.display="none";
    }
    console.log("left:"+obj.offsetLeft);

    //console.log(news_line.offsetLeft);
}
//强制数字位数
function fix(num, length) {
  return ('' + num).length < length ? ((new Array(length + 1)).join('0') + num).slice(-length) : '' + num;
}

//秒杀倒计时
function cd_timeout(cd){
    //参数cd为结束时间字符串，例2018/1/10 18:00:00,仅当天！

    var end_time = new Date(cd);
    var now_time = new Date();
    //console.log(end_time);
    var h = document.getElementById("cd-hours");
    var m = document.getElementById("cd-minutes");
    var s = document.getElementById("cd-seconds");
    //console.log(h);
    var cd_h = end_time.getHours()-now_time.getHours();
    var cd_m
    var cd_s
    if(now_time.getSeconds()>end_time.getSeconds()){
        cd_s = 60 - now_time.getSeconds();
        end_time.setMinutes(end_time.getMinutes()-1);
    }else{
        cd_s = end_time.getSeconds()-now_time.getSeconds();
    }
    if(now_time.getMinutes()>end_time.getMinutes()){
        cd_m = 60 - now_time.getMinutes();
        end_time.setHours(end_time.getHours()-1);
    }else{
        cd_m = end_time.getMinutes()-now_time.getMinutes();
    }
    if(now_time.getHours()>end_time.getHours()){
        cd_s = 0;
        cd_m = 0;
        cd_h = 0;
        //end_time.setHours(end_time.getHours()-1);
    }else{
        cd_h = end_time.getHours()-now_time.getHours();
    }
    h.innerHTML = fix(cd_h,2);
    m.innerHTML = fix(cd_m,2);
    s.innerHTML = fix(cd_s,2);
}

//加入计时器
//cd_timeout("2018/1/11 18:00:00");
Int = setInterval("cd_timeout('2018/1/11 20:00:00');",1000);

//商品切换js
var pro_list = document.getElementsByClassName("fk-item");
function product_next(type){
    var way_arg = 1;//方向参数，用于确定X轴偏移正负
    var now_offset_px = 0;//原偏移量
    if(type =="left"){
        way_arg = -1;
    }else{
        way_arg = 1;
    }
    var ele = document.getElementById("fk-list");
    var trans = ele.style.transform;
    console.log(typeof(trans));
    if(trans.length == 0){
        if(way_arg == 1){
            offset_px =199*(-4);
        }else{
            offset_px = -199;
        }
    }else{
        now_offset_px = parseInt(trans.split("(")[1].split(",")[0].split("px")[0]);
        if(now_offset_px == 0 && way_arg==1){
            offset_px = 199*(-4);
        }else if(now_offset_px == -796 && way_arg==-1){
            offset_px = 0;
        }else{
            offset_px = now_offset_px + (199 * way_arg);
        }

    }
    console.log("X原偏移量："+now_offset_px+"|X现偏移量："+offset_px);
    //var now_offset_px = trans.split("(")[1].split(",")[0].split("px")[0];
    //console.log("X偏移量："+parseInt(now_offset_px));
    //offset_px = -199;
    ele.style.transform = "translate3d("+offset_px+"px, 0px, 0px)";
    ele.style.transition = "transform 500ms ease-in-out";

    //ele.style.webkitTransform = "translate3d("+offset_px+"px,0,0);";
    //console.log(ele.style.webkitTransform);
}

//图片切换2
var fk_img_list = document.getElementsByClassName("fk-ch-img");
//获得所有图片对象列表
function fk_img_switch(obj){
    //获取图片对象
    var ele_img = document.getElementById(obj.attributes["target-data"].value);
    ele_img.style.display="block";
    obj.classList.add('fk-ch-circle-sel');
    //取消其他图片显示
    for(var i=0;i<fk_img_list.length;i++){
        if(ele_img != fk_img_list[i]){
            fk_img_list[i].style.display="none";
            obj = document.getElementById(fk_img_list[i].attributes["bang-ele"].value);
            obj.classList.remove('fk-ch-circle-sel');
        }
    }
    //绑定事件
    //鼠标覆盖则暂停计时器
    window.clearInterval(fk_img_int);
    ele_img.onmouseout = function(){
        //鼠标移开恢复计时器
        fk_img_int = setInterval("fk_img_auto();",2000);
    }
}
//用于计时器自动切换
var fk_img_index=0;
function fk_img_auto(){
    if(fk_img_index < fk_img_list.length){

    }else{
        fk_img_index=0;
    }
    fk_img_list[fk_img_index].style.display="block";
    var circle = document.getElementById(fk_img_list[fk_img_index].attributes["bang-ele"].value);
    circle.classList.add('fk-ch-circle-sel');
    //取消其他图片显示
    for(var i=0;i<fk_img_list.length;i++){
        //绑定事件
        fk_img_list[i].onmouseover=function(){
            window.clearInterval(fk_img_int);
        }
        fk_img_list[i].onmouseout = function(){
            //鼠标移开恢复计时器
            fk_img_int = setInterval("fk_img_auto();",2000);
        }
        if(fk_img_list[fk_img_index] != fk_img_list[i]){
            fk_img_list[i].style.display="none";
            circle = document.getElementById(fk_img_list[i].attributes["bang-ele"].value);
            circle.classList.remove('fk-ch-circle-sel');
        }
    }
    fk_img_index++;
}

function back_top(){
    scrollTo(0,0);
}

//浏览器窗口大小改变事件
window.onresize=function(){
     //console.log(window.innerWidth+"||"+window.innerHeight);
}

//滚动事件
window.onscroll = function() {
    //为了保证兼容性，这里取两个值，哪个有值取哪一个
    var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
　　//scrollTop就是触发滚轮事件时滚轮的高度
    //console.log("滚动距离："+scrollTop);
    var ele = document.getElementById("fixed-search-bar");
    if(scrollTop>600){
        console.log("显示搜索");
        ele.style.display="block";
    }else{
        console.log("影藏搜索");
        ele.style.display="none";
    }
}






