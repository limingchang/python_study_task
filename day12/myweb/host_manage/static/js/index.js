//注册表单验证
//$.tools().formAuth($(".modal #register"));
$("div[target-url]").click(function(){
    //$.tools().setCookie("lmc","dadadaf","s20")
    if($(this).attr("target-url")=="/login/"){
        window.location.href = "/login/";
        return;
    }
    var accessToken = $.tools().getCookie("accessToken");
    console.log(accessToken);
    if(accessToken == null){
        alert("请先登录")
        window.location.href = "/login/";
    }else{
        console.log("验证签名");
        var opt = {
            "type":"API",
            "ajaxType":"post",
            "data":{
                "act":"check_sign",
                "accessToken":accessToken,
            },
        }
        var res = $.ajaxData(opt);
        if(res.data){
            window.location.href = $(this).attr("target-url");
        }else{
            $.showTips("<i class='icon-exclamation-sign'></i>"+res.errMsg+",请重新登录",'error','tips-center');
            $("a[herf='/login_out/']").click();
            window.setTimeout("window.location='/login/'",2000);
        }
    }
    //window.location.href = $(this).attr("target-url");
});
$("#reg").click(function(){
    $(".shadow").show();
    $(".modal").slideDown();
    $(".modal").find("input")[0].focus();
});
$("#cancel").click(function(){
    $(".shadow").hide();
    $(".modal").hide();
    $(".modal").find(".errmsg").html("");
    $(".modal").find("input").val("");
});
//ajax用户名验证
$("input[name='user']").blur(function(){
    var val = $(this).val();
    if(val.length >=6 && val.length<=18){
        $(this).parent().next().html("<i class='f-info icon-spinner icon-spin icon-large'></i>");
        var opt = {
            "type":"API",
            "ajaxType":"post",
            "data":{
                "act":"check_user",
                "user":$(this).val(),
            },
        }
        var res = $.ajaxData(opt);
        //console.log(res);
        if(!res.errNum){
            $(this).parent().next().html("<i class='icon-ok f-success'></i>");
        }else{
            $(this).parent().next().html("<i class='icon-remove f-error'>"+res.errMsg+"</i>");

        }
    }


});
$(".modal #register").click(function(){
    //$("input[name='user']").blur();
    var inputs = $(".modal").find("input");
    var err = $(".modal").find(".icon-remove");
    var data = {
        "act":"register"
    };
    var opt = {
        "type":"API",
        "ajaxType":"post",
        "data":"",
    }
    if(err.length == 0){
        inputs.each(function(){
            var key = $(this).attr("name");
            var val = $(this).val()
            if(key == "pwd" || key == "repwd"){
                data[key]=hex_sha1(val);
            }else{
                data[key]=val;
            }

        });
        opt["data"] = data;
        var res = $.ajaxData(opt);
        $.showTips(res.errMsg,'info','tips-center');
        $(".modal").find("input").val("");
        $(".shadow").hide();
        $(".modal").hide();

    }else{
        $.showTips("<i class='icon-exclamation-sign'></i>表单填写有误",'warring','tips-center');
    }

});