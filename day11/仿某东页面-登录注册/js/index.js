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
function img_swicth(obj){
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
function img_load(){

    Int = setInterval("img_next('right');",3000);
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











//浏览器窗口大小改变事件
window.onresize=function(){
     //console.log(window.innerWidth+"||"+window.innerHeight);
}








