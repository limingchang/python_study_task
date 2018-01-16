//插入元素
function append_ele(ele_type,append_parentNode,class_list){
    //ele_type,插入元素的类型，如：div 、i、span，string
    //append_parentNode,插入元素的父节点,element
    //class_list,css样式类表，array
    var ele = document.createElement(ele_type);
    for(var i=0;i<class_list.length;i++){
        ele.classList.add(class_list[i]);
    }
    append_parentNode.appendChild(ele);
}
//移除元素
function remove_ele(parent_ele){
    var child_list = parent_ele.childNodes;
    if(child_list.length==6){
        child = parent_ele.lastChild;
        parent_ele.removeChild(child)
    }
}

//表单的js
//用户名的js
var input_username = document.getElementById("username");
input_username.onfocus=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    tip_ele.classList.remove("error");
    remove_ele(form_item);
    tip_ele.innerHTML="<i class='i-tip i-ico-info'></i>支持中文、字母、数字、“-” “_”的组合，4-20个字符";
}

input_username.onblur=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    //console.log(form_item);
    if(this.value.length==0){
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>用户名不能为空！";
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
    }else if(!(this.value.length>=4 && this.value.length<=20)){
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>长度只能在4-20个字符之间";
    }else if(!isNaN(this.value)){
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>用户名不能是纯数字，请重新输入！";
    }else{
        tip_ele.classList.remove("error");
        form_item.classList.remove("text-error");
        append_ele("i",form_item,["i-tip","i-check","i-ico-success"]);
        tip_ele.innerHTML="";
    }
}
//密码评分
function checkStrong(val) {
    var modes = 0;
    if (val.length < 6) return 0;
    if (/\d/.test(val)) modes++; //数字
    if (/[a-z]/.test(val)) modes++; //小写
    if (/[A-Z]/.test(val)) modes++; //大写
    if (/\W/.test(val)) modes++; //特殊字符
    if (val.length > 12) return 4;
    return modes;
};

//密码的JS
var input_pwd = document.getElementById("pwd");
input_pwd.onfocus=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    tip_ele.classList.remove("error");
    remove_ele(form_item);
    tip_ele.innerHTML="<i class='i-tip i-ico-info'></i>建议使用字母、数字和符号两种及以上组合，6-20个字符";
}
input_pwd.onblur = function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    if(this.value.length==0){
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>用户名不能为空！";
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
    }else if(this.value.length<6 && this.value.length >20){
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>长度只能在6-20个字符之间";
    }else{
        var pwd_score = checkStrong(this.value);
        append_ele("i",form_item,["i-tip","i-check","i-ico-success"]);
        if(pwd_score<2){
            tip_ele.innerHTML="<i class='i-tip i-ico-ruo'></i>有被盗风险,建议使用字母、数字和符号两种及以上组合！";
            //安全强度适中，可以使用三种以上的组合来提高安全强度
            //你的密码很安全
        }else if(pwd_score>=2 && pwd_score<4){
            tip_ele.innerHTML="<i class='i-tip i-ico-zhong'></i>安全强度适中，可以使用三种以上的组合来提高安全强度！";
        }else{
            tip_ele.innerHTML="<i class='i-tip i-ico-qiang'></i>你的密码很安全！";
        }
    }
}

//重复密码的js
var input_re_pwd = document.getElementById("re-pwd");
input_re_pwd.onfocus=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    tip_ele.classList.remove("error");
    remove_ele(form_item);
    tip_ele.innerHTML="<i class='i-tip i-ico-info'></i>请再次输入密码！";
}
input_re_pwd.onblur=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    if(this.value != input_pwd.value){
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>两次密码输入不一致！";
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
    }else{
        tip_ele.classList.remove("error");
        form_item.classList.remove("text-error");
        append_ele("i",form_item,["i-tip","i-check","i-ico-success"]);
        tip_ele.innerHTML="";
    }

}
//手机js
//手机号检查
function check_mobile(tle_number){
    if(!(/^1[3|4|5|7|8][0-9]\d{8}$/.test(tle_number))){
        return false;
    }else{
        return true;
    }
}
var input_tel = document.getElementById("tel");
input_tel.onfocus=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    tip_ele.classList.remove("error");
    remove_ele(form_item);
    tip_ele.innerHTML="<i class='i-tip i-ico-info'></i>完成验证后，您可以使用手机登录和找回密码！";
}
input_tel.onblur=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    if(check_mobile(this.value)){
        tip_ele.classList.remove("error");
        form_item.classList.remove("text-error");
        append_ele("i",form_item,["i-tip","i-check","i-ico-success"]);
        tip_ele.innerHTML="";

    }else{
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>格式不正确！";
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
    }
}
//验证方式切换
function switch_auth_type(obj){
    var target_data = obj.attributes["target-data"].value;
    var target_ele = document.getElementById(target_data);
    var target_tip = document.getElementById(target_ele.attributes["target-data"].value);
    console.log(target_tip.parentNode);
    if(target_data=="email"){
        target_ele.value="";
        target_tip.parentNode.classList.remove("hidden");
        target_ele.parentNode.classList.remove("hidden");
        obj.attributes["target-data"].value="tel";
        obj.innerHTML="手机验证";
        document.getElementById("tel").parentNode.classList.add("hidden");
        document.getElementById(document.getElementById("tel").attributes["target-data"].value).parentNode.classList.add("hidden");
    }else{
        target_ele.value="";
        target_tip.parentNode.classList.remove("hidden");
        target_ele.parentNode.classList.remove("hidden");
        obj.attributes["target-data"].value="email";
        obj.innerHTML="邮箱验证";
        document.getElementById("email").parentNode.classList.add("hidden");
        document.getElementById(document.getElementById("email").attributes["target-data"].value).parentNode.classList.add("hidden");
    }
}
//邮箱验证
function isEmail(str){
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
    return reg.test(str);
}
//邮箱输入的js
var input_email = document.getElementById("email");
input_email.onfocus=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    tip_ele.classList.remove("error");
    remove_ele(form_item);
    tip_ele.innerHTML="<i class='i-tip i-ico-info'></i>完成验证后，您可以使用邮箱登录和找回密码！";
}
input_email.onblur=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    if(isEmail(this.value)){
        tip_ele.classList.remove("error");
        form_item.classList.remove("text-error");
        append_ele("i",form_item,["i-tip","i-check","i-ico-success"]);
        tip_ele.innerHTML="";

    }else{
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>格式不正确！";
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
    }
}
//验证码js
var Auth_code = "de8ug";
var input_authcode = document.getElementById("authcode");
input_authcode.onfocus=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    console.log(tip_ele);
    tip_ele.classList.remove("error");
    remove_ele(form_item);
    tip_ele.innerHTML="<i class='i-tip i-ico-info'></i>看不清？点击图片更换验证码！";
}
input_authcode.onblur=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    if(this.value==Auth_code){
        tip_ele.classList.remove("error");
        form_item.classList.remove("text-error");
        append_ele("i",form_item,["i-tip","i-check","i-ico-success"]);
        tip_ele.innerHTML="";

    }else{
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>验证码不正确！";
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        remove_ele(form_item);
    }
}

//彩蛋
function createcode(){
    alert("别点啦！没做！纯js验证码，搞死我啊！\n去关注de8ug，让他教你！\n你猜验证码是不是de8ug？");
}