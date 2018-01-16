//插入元素
function append_ele(ele_type,append_parentNode,class_list){
    //ele_type,插入元素的类型，如：div 、i、span，string
    //append_parentNode,插入元素的父节点,element
    //class_list,css样式类表，array
    var ele = document.createElement(ele_type);
    console.log(ele);
    for(var i=0;i<class_list.length;i++){
        ele.classList.add(class_list[i]);
    }
    append_parentNode.appendChild(ele);
}

//表单的js
//用户名的js
var input_username = document.getElementById("username");
input_username.onfocus=function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
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
    }else if(this.value.length<4 && this.value.length >20){
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>长度只能在4-20个字符之间";
    }else if(!isNaN(this.value)){
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>用户名不能是纯数字，请重新输入！";
    }else{
        tip_ele.classList.remove("error");
        form_item.classList.remove("text-error");
        append_ele("i",tip_ele,["i-tip","i-check","i-ico-success"]);
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
    tip_ele.innerHTML="<i class='i-tip i-ico-info'></i>建议使用字母、数字和符号两种及以上组合，6-20个字符";
}
input_pwd.onblur = function(){
    var tip_ele = document.getElementById(this.attributes["target-data"].value);
    var form_item = tip_ele.parentNode.previousSibling.previousSibling;
    if(this.value.length==0){
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>用户名不能为空！";
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
    }else if(this.value.length<6 && this.value.length >20){
        tip_ele.classList.add("error");
        form_item.classList.add("text-error");
        tip_ele.innerHTML="<i class='i-tip i-ico-error'></i>长度只能在6-20个字符之间";
    }else{
        var pwd_score = checkStrong(this.value);
        append_ele("i",tip_ele,["i-tip","i-check","i-ico-success"]);
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
