$("#test").click(function(){
    // create_cell('123',{'name':"ip","id":123});
    // refresh_host();
});
$("#show_modal").click(function(){
//    refresh_host();
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
$("#add_host").click(function(){
    var data = {};
    $(".modal input").each(function(){
        data[$(this).attr("name")] = $(this).val();
    });
    data["act"] = "add_host";
    var opt = {
        "type":"API",
        "ajaxType":"post",
        "data":data,
    }
    var res = $.ajaxData(opt);
    if(!res.errNum){
        $.showTips("<i class='icon-exclamation-sign'></i>【"+res.errMsg+"】操作成功",'success','tips-center');
        $(".modal input").val("");
        $(".shadow").hide();
        $(".modal").hide();
        refresh_host();
    }
});
$("#tb").on('click',"button[name='del-host']",function(){
    var ele = this;
    var opt = {
        title:"操作确认",
        content:"您确定要删除此条记录吗？",
        type:"ask",
    }
    $.dialogBox(opt,callback=function(){
        if(this.btn == 'confirm'){
            var id = $(ele).attr('target-data');
            var data = {};
            data["act"] = "del_host";
            data["id"] = id;
            var opt = {
                "type":"API",
                "ajaxType":"post",
                "data":data,
            };
            var res = $.ajaxData(opt);
            if(!res.errNum){
                $.showTips("<i class='icon-exclamation-sign'></i>【"+res.errMsg+"】操作成功",'success','tips-center');
                refresh_host();
            }
        }
    });


});
$("#tb").on('click',"button[name='edit-host']",function(){
    //console.log($(this).parent().siblings());
    var tds = $(this).parent().siblings();
    tds.each(function(){
        if($(this).attr("name") != "host-status"){
            var input = $(document.createElement('input')).attr("name",$(this).attr("name")).addClass('edit-input');
            input.val($(this).text());
            $(this).text("");
            $(this).append(input);

        }
    });
    $('input[name=host-name]').focus();
    //修改为保存按钮icon-save
    $(this).html("<i class='icon-save'></i>保存").attr("name","save-host").removeClass("orange").addClass("success");
    //创建详情行
    var tr = $(this).parent().parent();
    var detail_tr = $(document.createElement("tr")).addClass("detail-tr");
    detail_tr.append($(document.createElement("td")).attr("colspan","5").text(""));
    tr.after(detail_tr);
    var detail_div = $(document.createElement('div')).addClass('detail-div');
    var root_label = $(document.createElement('label')).text("Root:");
    var root_input = $(document.createElement('input')).attr('name','root').addClass('edit-input');
    detail_div.append(root_label).append(root_input);
    var key_label = $(document.createElement('label')).text("Key:");
    var key_input = $(document.createElement('input')).attr('name','key').addClass('edit-input');
    detail_div.append(key_label).append(key_input);
    detail_tr.find('td').append(detail_div);
    //获取详情数据
    var host_id = $(this).attr('target-data');
    console.log(host_id);
    var data = {};
    data['act'] = 'get_host_by_id';
    data['id'] = host_id;
    var opt = {
        "type":"API",
        "ajaxType":"post",
        "data":data,
    }
    var res = $.ajaxData(opt);
    if(!res.errNum){
        root_input.val(res.data['root']);
        key_input.val(res.data['key']);
    }else{
        detail_tr.text(res.errMsg);
    }
});

$("#tb").on("click","button[name=save-host]",function(){
    var data = {};
    data['act'] = 'save_host';
    data['host-id'] = $(this).attr('target-data');
    var inputs = $(this).parent().parent().find('input');
    //inputs.add($(this).parent().parent().next());
    var detail_inputs = $(this).parent().parent().next().find('input');
    inputs.each(function(){
        data[$(this).attr('name')] = $(this).val();
    });
    detail_inputs.each(function(){
        data[$(this).attr('name')] = $(this).val();
    });
    console.log(data);
    var opt = {
        "type":"API",
        "ajaxType":"post",
        "data":data,
    }
    var res = $.ajaxData(opt);
    console.log(res);
    if(!res.errNum){
        $.showTips("<i class='icon-exclamation-sign'></i>【"+res.errMsg+"】操作成功",'success','tips-center');

    }else{
        $.showTips("<i class='icon-remove-sign'></i>【"+res.errMsg+"】操作失败",'error','tips-center');
    }
    refresh_host();
});

function refresh_host(){
    var data = {};
    data["act"] = "refresh_host";
    var opt = {
        "type":"API",
        "ajaxType":"post",
        "data":data,
    }
    var res = $.ajaxData(opt);
    var tb = $("#tb").html("");
    var data = res.data;
    if(res.errNum){
        tb.html("<tr><td class='f-warring' colspan='5'><i class='icon-exclamation-sign'></i>"+res.errMsg+"</td></tr>");
    }else{
        if(data.length == 0){
            tb.html("<tr><td class='f-warring' colspan='5'><i class='icon-exclamation-sign'></i>您还没有可管理的主机</td></tr>");
        }else{
            for(var i=0;i<data.length;i++){
                //console.log(data[i]);
                var tr = document.createElement("tr");
                $(tr).append(create_cell(data[i].name,{"name":"host-name","target-data":data[i].id}));
                $(tr).append(create_cell(data[i].ip,{"name":"host-ip"}));
                $(tr).append(create_cell(data[i].port,{"name":"host-port"}));
                $(tr).append(create_cell("连接中...",{"name":"host-status"}));
                var td_act = create_cell("");
                var btn_del = document.createElement("button");
                $(btn_del).attr("name","del-host").attr("target-data",data[i].id).addClass("btn btn-ml error");
                //$(btn_del).html("<i class='icon-trash'></i>删除");
                $(btn_del).text("删除").prepend($(document.createElement('i')).addClass('icon-trash'));
                $(td_act).append(btn_del);
                var btn_edit = document.createElement("button");
                $(btn_edit).attr("name","edit-host").attr("target-data",data[i].id).addClass("btn btn-ml orange");
                //$(btn_edit).html("<i class='icon-pencil'></i>修改");
                $(btn_edit).text("修改").prepend($(document.createElement('i')).addClass('icon-pencil'));
                $(td_act).append(btn_edit);
                $(tr).append(td_act);
                tb.append(tr);
            }
            chk_ip();
        }
    }
}

function create_cell(str,attr={}){
    var td = document.createElement('td');
    $(td).text(str);
    for(item in attr){
        //console.log(item+'|'+attr[item]);
        $(td).attr(item,attr[item]);
    }
    // if(name != ""){
    //     $(td).attr("name",name);
    // }

    return td;
}

function chk_ip_res(ip,ele){
    var data = {};
    data['ip'] = ip;
    data['act'] = 'check_ip_status';
    $.ajax({
        type:"post",
        url:"/api/",
        data:data,
        success:function(data){
            if(data.data == '停机'){
                ele.html("<span class='f-error'><i class='icon-circle'></i></span>停机");
            }else{
                ele.html("<span class='f-success'><i class='icon-circle'></i></span>"+data.data);
            }
        },
    });
}
function chk_ip(){
    var td_ip = $("td[name='host-ip']");
    td_ip.each(function(){
        var ip = $(this).text();
        var td_msg = $(this).next().next();
        chk_ip_res(ip,td_msg);
    });

}
chk_ip();
