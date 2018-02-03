$(".modal").find("input").each(function(){
    $(this).blur(function(){
        var flag = true;
        var msg = '';
        var err  =$(this).parent().next();
        var min_length = parseInt($(this).attr("min-length"));
        var max_length = parseInt($(this).attr("max_length"));
        var auth_type = $(this).attr("filed");
        var require = $(this).attr("require");
        if(require == "true"){
            if($.tools().trim($(this).val()).length == 0){
                console.log("不能为空！");
                flag = false;
                msg = $(this).attr("name")+'不能为空！';
            }else{
                if(min_length){
                    if($(this).val().length < min_length){
                        flag = false;
                        msg = '格式错误：最小长度不能小于'+min_length;
                    }else{
                        flag = true;
                    }
                }
                if(max_length){
                    if($(this).val().length > max_length){
                        flag = false;
                        msg = '格式错误：最大长度不能大于'+max_length;
                    }else{
                        flag = true;
                    }
                }
                if(auth_type){
                    if(auth_type == "string"){
                        var reg = /^\w+$/;
                        if(!reg.test($(this).val())){
                            flag = false;
                            msg = '格式错误：请使用字符和数字';
                        }else{
                            flag = true;
                        }
                    }else if(auth_type == "tel"){
                        var reg = /^1[34578]\d{9}$/;
                        if(!reg.test($(this).val())){
                            flag = false;
                            msg = '手机格式错误';
                        }else{
                            flag = true;
                        }

                    }else if(auth_type == "email"){

                    }else if(auth_type == "repeat"){
                        var re = $(".modal").find("[name="+$(this).attr("re-for")+"]");
                        if(re.val() != $(this).val()){
                            flag = false;
                            msg = '两次密码输入不符';
                        }else{
                            flag = true;
                        }
                    }
                }
            }
        }
        if(!flag){
            $.showTips(msg,'error','tips-center');
            err.html("<i class='icon-remove f-error'></i>");
            return;
        }else{
            err.html("<i class='icon-ok f-success'></i>");
        }
    });

});