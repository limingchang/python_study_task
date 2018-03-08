$("#show_modal").click(function(){
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
        $.showTips("<i class='icon-exclamation-sign'></i>"+res.errMsg+",添加成功",'success','tips-center');
        $(".modal input").val("");
        $(".shadow").hide();
        $(".modal").hide();
        window.location.reload()
    }
});
$("button[name='del-host']").on('click',function(){
    var id = $(this).attr('target-data');
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
        $.showTips("<i class='icon-exclamation-sign'></i>"+res.errMsg+",删除成功",'success','tips-center');
        window.location.reload()
    }
});


function chk_ip(ip,ele){
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
var td_ip = $("td[name='host-ip']");
td_ip.each(function(){
    var ip = $(this).text();
    var td_msg = $(this).next().next();
    chk_ip(ip,td_msg);
});
