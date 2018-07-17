$.tools().formAuth($("#add_user"));
//注册指向链接
$('li[target-link]').click(function () {
   var link = $(this).attr('target-link');
   window.location.href = link;
});
//添加用户按钮
$("#user_add").click(function () {
    $(".shadow").show();
    //位置修正
    var h = ($(window).height() - $(".modal").height())/4;
    var w = ($(window).width() - $(".modal").width())/2;
    var pos = {
        "left":w,
        "top":h
    };
    $(".modal").css("left",pos.left + "px").css("top",pos.top + "px").show();
    // $(".modal").offset(pos).show();
});
//取消按钮
$("#cancel").click(function () {
    $(".shadow").hide();
    $(".modal input").val("").css("border-color","#ccc");
    $(".modal .errmsg").html("");
    $(".modal").hide();
});
//新增按钮
$("#add_user").click(function () {
    var has_err = $(".modal .f-error");
    // console.log(has_err.length);
    if(has_err.length == 0){
        var inputs = $(".modal input");
        var data = {};
        inputs.each(function () {
            data[$(this).attr("name")] = $(this).val();
        });
        data['act'] = "add_user";
        data['user_group'] = $('#user_group').val();
        opt = {
            "type":"API",
            "url":"/user_manage/api/",
            "data":data
        };
        // console.log(opt);
        var res = $.ajaxData(opt);
        if(res.errNum == 0){
            $.showTips(res.errMsg,tips_type='info',tips_position='tips-center');
        }else {
            $.showTips(res.errMsg,tips_type='error',tips_position='tips-center');
        }
        console.log(res);
        $(".shadow").hide();
        $(".modal input").val("").css("border-color","#ccc");
        $(".modal .errmsg").html("");
        $(".modal").hide();
        $.tools().refresh_page(2);
    }

});
//删除按钮
$('td').on("click","button[name=del]",function () {
    opt={
        title: '提示',
        content: '您确认删除吗？',
        type:'ask',
        shadow:true,
    };
    ele = this;
    $.dialogBox(opt,function () {
        if(this.btn == 'confirm'){
            //执行删除
            var id = $(ele).parent().parent().attr('data-id');
            console.log(id);
            data = {
                "act":"del_user",
                "id":id
            };
            opt={
                "type":"API",
                "url":"/user_manage/api/",
                "data":data
            };
            var res = $.ajaxData(opt);
            if(res.errNum == 0){
                $.showTips(res.errMsg,tips_type='info',tips_position='tips-center');
            }else {
                $.showTips(res.errMsg,tips_type='error',tips_position='tips-center');
            }
            $.tools().refresh_page(2);
        }
    })
});
//修改按钮
$('td').on("click","button[name=edit]",function () {
    console.log('edit');
    //修改标题
    $('.m-title').text('修改用户');
    //传递ID
    $('#save').show().attr('data-id',$(this).parent().parent().attr('data-id'));
    $('#add_user').hide();
    //显示modal
    $(".shadow").show();
    //位置修正
    var h = ($(window).height() - $(".modal").height())/4;
    var w = ($(window).width() - $(".modal").width())/2;
    var pos = {
        "left":w,
        "top":h
    };
    $(".modal").css("left",pos.left + "px").css("top",pos.top + "px").show();
    //填入信息
    $("input[name=user]").val($(this).parent().parent().children().eq(0).text()).attr("disabled","disabled").addClass('disable');
    $("input[name=pwd]").attr("min-len",0);
    //加入不修改密码提示
    //
    $("input[name=email]").val($(this).parent().parent().children().eq(1).text());
    var user_group = $("option");
    var group_name = $(this).parent().parent().children().eq(2).text();
    user_group.each(function(){
        if($(this).text() == group_name){
            $(this).attr("selected",true);
        }
    });



});
//保存按钮
$("#save").click(function(){
    var has_err = $(".modal .f-error");
    // 设置密码可为空
    $("input[name=pwd]").attr('min-len',0);
    if(has_err.length == 0){
        var inputs = $(".modal input");
        var data = {};
        inputs.each(function () {
            data[$(this).attr("name")] = $(this).val();
        });
        data['act'] = "edit_user";
        data['user_group'] = $('#user_group').val();
        data['user_id'] = $(this).attr('data-id');
        opt = {
            "type":"API",
            "url":"/user_manage/api/",
            "data":data
        };
        // console.log(opt);
        var res = $.ajaxData(opt);
        if(res.errNum == 0){
            $.showTips(res.errMsg,tips_type='info',tips_position='tips-center');
        }else {
            $.showTips(res.errMsg,tips_type='error',tips_position='tips-center');
        }


    }
    $(".shadow").hide();
    $(".modal input").val("").css("border-color","#ccc");
    $(".modal .errmsg").html("");
    $(".modal").hide();
    $.tools().refresh_page(2);
    //恢复modal
    // $('.m-title').text('新增用户');
    // $(".modal input").val("");
    // $("input[name=pwd]").attr('min-len',6);
    // $("input[name=user]").removeAttr("disabled").removeClass("disable");
    // $('#add_user').show();
    // $('#save').hide();
});