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
    console.log(data);
    data["act"] = "add_host";
    var opt = {
        "type":"API",
        "ajaxType":"post",
        "data":data,
    }
    console.log(opt);
    var res = $.ajaxData(opt);
    if(!res.errNum){
        $.showTips("<i class='icon-exclamation-sign'></i>"+res.errMsg+",添加成功",'success','tips-center');
        $(".modal input").val("");
        $(".shadow").hide();
        $(".modal").hide();
        window.location.reload()
    }
});