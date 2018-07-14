//开启表单验证
$.tools().formAuth($("#add_group"));
//注册指向链接
$('li[target-link]').click(function () {
   var link = $(this).attr('target-link');
   window.location.href = link;
});
//添加组模态框
$('#group_add').click(function () {
    $(".shadow").show();
    //位置修正
    var h = ($(window).height() - $(".modal").height())/4;
    var w = ($(window).width() - $(".modal").width())/2;
    var pos = {
        "left":w,
        "top":h
    };
    $(".modal").css("left",pos.left + "px").css("top",pos.top + "px").show();

});
//取消按钮
$("#cancel").click(function () {
    $(".shadow").hide();
    $(".modal input").val("").css("border-color","#ccc");
    $(".modal .errmsg").html("");
    $('.m-title').text("新增用户组");
    $(".modal").hide();
});
//模态框新增按钮
$("#add_group").click(function () {
   var has_err = $(".modal .f-error");
    // console.log(has_err.length);
    if(has_err.length == 0){
        var inputs = $(".modal input");
        var data = {};
        inputs.each(function () {
            data[$(this).attr("name")] = $(this).val();
        });
        data['act'] = "add_group";
        opt = {
            "type":"API",
            "url":"/user_manage/api/",
            "data":data
        };
        console.log(opt);
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
//删除组按钮

$('td').on('click','button[name=del]',function(){
    var opt = {
       title: '提示',
       content: '您确认删除吗？',
       type:'ask',
       shadow:true,
   };
   var ele = this;
   $.dialogBox(opt,function () {
       if(this.btn == 'confirm'){
           //执行删除
           var id = $(ele).parent().parent().attr('data-id');
           console.log(id);
           data = {
                "act":"del_group",
                "group_id":id
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
           //location.reload(true);
           $.tools().refresh_page(2);
        }
    });
});

//修改按钮
$('td').on('click','button[name=edit]',function(){
    console.log('modify');
    //格式化模态框
    $('.m-title').text("修改组信息");
    $('#save').show();
    $('#add_group').hide();
    //填入原数据
    $("input[name='group_name']").val($(this).parent().parent().children().eq(0).text());
    $("input[name='description']").val($(this).parent().parent().children().eq(1).text());
    var id = $(this).parent().parent().attr('data-id');
    $('#save').attr('group_id',id);
    $(".shadow").show();
    //位置修正
    var h = ($(window).height() - $(".modal").height())/4;
    var w = ($(window).width() - $(".modal").width())/2;
    var pos = {
        "left":w,
        "top":h
    };
    $(".modal").css("left",pos.left + "px").css("top",pos.top + "px").show();

});
//保存按钮
$("#save").click(function () {
    var has_err = $(".modal .f-error");
    if(has_err.length == 0){
        var inputs = $(".modal input");
        var data = {};
        inputs.each(function () {
            data[$(this).attr("name")] = $(this).val();
        });
        data['group_id'] = $(this).attr('group_id');
        data['act'] = "edit_group";
        var opt={
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
    };
    $(".shadow").hide();
    $(".modal input").val("").css("border-color","#ccc");
    $(".modal .errmsg").html("");
    $(".modal").hide();
    //恢复模态框标题
    $('.m-title').text("新增用户组");

    $.tools().refresh_page(2);
});