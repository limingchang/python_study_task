(function(){
	$.extend({
		'showTips':function(msg,tips_type='info',tips_position='tips-lefttop'){
			//console.log(msg,tips_type,tips_position);
			var tips = document.createElement('div');
				$(tips).addClass('tips').addClass(tips_type).addClass(tips_position).html(msg);
				var span = document.createElement('span');
				$(span).text('X').addClass('tips-span').click(function(){
					$(tips).hide();
				});
				$(tips).append(span);
				$('body').append(tips);
				var pos_x;
				var pos_y;
				var pos={}
				if(tips_position=='tips-lefttop'){
					pos_x = $(tips).offset().left;
				}else{
					pos_x = $(tips).offset().left -$(tips).innerWidth()/2;
				}
				if($('.'+tips_position).length>1){
					pos_y = $('.'+tips_position+':last').outerHeight()+$('.'+tips_position+':last').offset().top+5;
				}
				pos = {left:pos_x,top:pos_y};
				//console.log(pos);
				$(tips).offset(pos);
				setTimeout(function(){
					$(tips).addClass('tips-show');
				},0)
				setTimeout(function(){
					$(tips).remove()
				},5000)
		}
		
	});
	var ajaxData = function(opt){
		this.defaults = {
			"type":"API",
			"url":null,
			"ajaxType":"post",
			"data":{},
			"requestDataType":"JSON",
			"has_token":false,//是否携带access_token
			"async":false,//ajax模式，true异步，false同步
			//同步模式会阻塞其他js运行
			"callback":this.__callback__(),
		}
		this.res_data = "";
		this.options = $.extend({},this.defaults, opt);
		this.__inti__();
		//return this.res_data;

	}
	ajaxData.prototype = {
		__inti__:function(){

			if(this.options.type == "API"){
				//console.log("调用api");
				this.__api__();
			}else if(this.options.type == "USER_AUTH"){
				// console.log("登录认证");
				this.__loginAuth__();
			}else if(this.options.type == "AUTH_CODE"){
			    // console.log("获取验证码");
				this.__authCode__();
			}

		},
		__api__:function(){
			if(this.options.url == null){
				// console.log('默认URL');
				this.__ajax__(this,"/api/");
			}else {
				this.__ajax__(this,this.options.url);
			}

		},
		__authCode__:function(){
			if(this.options.url == null) {
                this.__ajax__(this, "/auth_code/");
            }else {
				this.__ajax__(this,this.options.url);
			}
		},
		__loginAuth__:function(){
			var data = this.options.data;
			var res;
			if(data['user'].length==0 || data['pwd'].length==0){
				res = {
					"errNum":101,
					"errMsg":"用户名密码不能为空",
				}
			}else if(data['auth_code'].length==0){
				res = {
					"errNum":102,
					"errMsg":"请填写验证码",
				}
			}else{
				//密码加密,再post
				this.options.data['pwd'] = hex_sha1(this.options.data['pwd']);
				if(this.options.url == null){
					this.__ajax__(this,"/login/");
				}else {
					this.__ajax__(this,this.options.url);
				}
				res = JSON.parse(this.res_data);
			}
			this.res_data = res;
			//return res;
		},
		__ajax__:function(that,url){
			$.ajax({
				type:that.options.ajaxType,
				url:url,
				beforeSend:function(XMLHttpRequest){
				    if(that.options.type=="API" && that.options.has_token){
				        XMLHttpRequest.setRequestHeader('accessToken',$.tools().getCookie("accessToken"));
				    }
				},
				data:that.options.data,
				success:function(data,that){
				    formatData(data);
				},
				async:that.options.async,
			});
			function formatData(data){
                that.res_data = data;
			}

		},
		__post__:function(){
			
		},
		__get__:function(){
			
		},
		__callback__:function(){
			
		}
	}
	$.ajaxData = function(opt){
		var a = new ajaxData(opt);
		// console.log(a.options);
		return a.res_data;
	}
	//弹出对话框
	var dialogBox = function(opt,callback=function(){}){
	    this.defaults = {
			width:null,
			//对话框宽度
			height:null,
			//对话框高度
			hasClose:true,
			//是否显示右上角X关闭按钮
			confirmValue: "确定",
            //确定按钮文字内容
            //confirm: function() {},
            //点击确定后回调函数
            cancelValue: "取消",
            //取消按钮文字内容
            //cancel: function() {},
            //点击取消后回调函数，默认关闭弹出框
            callback:callback,
            //点击按钮的回调函数
            type: 'ask',
            //对话框类型：ask(询问对话框),correct(正确/操作成功对话框),error(错误/警告对话框),tips(提示消息)
            title: '',
            //标题内容
            content: '',
            //正文内容
			shadow:false,
			//是否显示遮罩
            btn:null,
            //单击按钮的结果,字符串类型（confirm,cancel）

		}
		this.res_data = "";
		this.options = $.extend({},this.defaults, opt);
		//console.log(this.options);
		this.__init__();

	}
	dialogBox.prototype = {
	    //初始化插件
		__init__:function(){
		    this.element = null;
		    this.__create__();
		    this.__render__();
		    this.__setCSS__();
		    this.__on__(this);
		},
		//创建插件元素
		__create__:function(){
		    var dialogBox = $(document.createElement('div')).addClass('dialog-box');
		    var title = $(document.createElement('div')).addClass('dialog-title');

		    title.append($(document.createElement('div')).text(this.options.title).addClass('left'))
		    if(this.options.hasClose){
		        var btnClose = $(document.createElement('div')).addClass('dialog-close f-error right');
		        btnClose.append("<i class='icon-remove'></i>");
		        title.append(btnClose);
		    }
		    title.append($(document.createElement('div')).addClass('clear-float'));
		    var content = $(document.createElement('div')).addClass('dialog-content').append($(document.createElement('span')).text(this.options.content));
		    var divBtn = $(document.createElement('div')).addClass('dialog-btn');
		    //console.log(this.options.type);
		    dialogBox.append(title).append(content).append(divBtn);
		    switch (this.options.type) {
            case 'correct':
                content.prepend("<i class='f-success icon-ok-sign icon-large'></i>");
                var btn = $(document.createElement('button')).addClass('btn btn-xl success').text(this.options.confirmValue).attr("name","confirm");
                divBtn.append(btn);
                break;
            case 'error':
                content.prepend("<i class='f-error icon-remove-sign icon-large'></i>");
                var btn = $(document.createElement('button')).addClass('btn btn-xl success').text(this.options.confirmValue).attr("name","confirm");
                divBtn.append(btn);
                break;
            case 'tips':
                //content.prepend("<i class='f-info icon-exclamation-sign icon-large'></i>");
                divBtn.hide().remove();
                setTimeout(function(){
					dialogBox.remove();
				},5000)
                break;
            case 'ask':
                content.prepend("<i class='f-info icon-question-sign icon-large'></i>");
                var btn = $(document.createElement('button')).addClass('btn btn-xl success').text(this.options.confirmValue).attr("name","confirm");
                divBtn.append(btn);
                btn = $(document.createElement('button')).addClass('btn btn-xl error').text(this.options.cancelValue).attr("name","cancel");
                divBtn.append(btn);
                break;
            default:
                content.prepend("<i class='f-info icon-exclamation-sign icon-large'></i>");
                break;
            }
		    //console.log(dialogBox);
		    this.element = dialogBox;
		    //创建遮罩
			if(this.options.shadow){
				//查找遮罩
				var shadow = $('.shadow');
				if(shadow.length != 0){
					this.shadow = shadow;
					this.shadow.attr('name','dialog-shadow');
				}else {
					this.shadow = $(document.createElement('div')).addClass('shadow blue hidden');
				}
				//console.log(this.shadow);
				this.shadow.show();
			}

		},
		//渲染插件(插入元素、设置位置、动画等)
		__render__:function(){
		    $("body").append(this.element);
		    this.element.width(this.options.width || 200);
		    this.element.height(this.options.height || 'auto');
		    var height = this.element.height();
		    var width = this.element.width();
		    var pos_x = ($(window).height() - height) / 2;
		    var pos_y = ($(window).width() - width) / 2;
            var pos = {
                top:pos_x,
                left:pos_y
            };
            //console.log(pos);
            this.element.offset(pos);
            //$("body").append(this.element);


		},
		//设置样式
		__setCSS__:function(){
		    //如果按钮是2个，调整距离
		    var count_btn = $(".dialog-btn button").length;
		    //console.log(count_btn);
            if(count_btn == 2){
                var range = (this.element.width() - $(".dialog-btn button").width() * 2) / 8;
                $(".dialog-btn button").css("margin-left",range);
                $(".dialog-btn button").css("margin-right",range);
            }
		},
		//绑定事件
		__on__:function(that){
		    $(".dialog-close").on("click",".icon-remove",function(){
		        that.__destroy__();
		    });
//		    $(".dialog-box").on("click",".dialog-btn .success",function(){
//		        that.options.confirm();
//		        that.__destroy__();
//		    });
//		    $(".dialog-box").on("click",".dialog-btn .error",function(){
//		        that.options.cancel();
//		        that.__destroy__();
//		    });
		    $(".dialog-box").on("click",".dialog-btn button",function(){
		        that.options.btn = $(this).attr("name");
		        that.options.callback();
		        that.__destroy__();
		    });
		},
		//销毁元素
		__destroy__:function(){
		    this.element.hide().remove();
		    if(this.options.shadow){
		    	this.shadow.hide();
		    	//$('div[name=dialog-shadow]').remove();
			}
		},

	}
	$.dialogBox = function(opt,callback){
	    var d = new dialogBox(opt,callback);
	    return;
	}
	//工具
	var tools = function(){
		
	}
	tools.prototype = {
		trim:function(str){
			return str.replace(/(^\s*)|(\s*$)/g, ""); 
		},
		//cookie操作工具
		setCookie:function(name,value,time){
		    var getsec = function(str){
                var str1=str.substring(1,str.length)*1;
                var str2=str.substring(0,1);
                if (str2=="s"){
                    return str1*1000;
                }else if (str2=="h"){
                    return str1*60*60*1000;
                }else if (str2=="d"){
                    return str1*24*60*60*1000;
                }
            }
            var strsec = getsec(time);
            var exp = new Date();
            exp.setTime(exp.getTime() + strsec*1);
            document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();

            //s20是代表20秒
            //h是指小时，如12小时则是：h12
            //d是天数，30天则：d30
            //setCookie("name","hayden","s20");
        },
        delCookie:function(name){
            var exp = new Date();
            exp.setTime(exp.getTime() - 1);
            var cval = getCookie(name);
            if(cval!=null)
            document.cookie= name + "="+cval+";expires="+exp.toGMTString();
        },
        getCookie:function(name){
            var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
            if(arr=document.cookie.match(reg))
                return unescape(arr[2]);
            else
                return null;
        },
        //表单验证工具
        formAuth:function(btn){
            btn.click(function(){
                $("input[require]").each(function(){
                    var flag = true;
                    var msg = '';
                    var err = $(this).parent().next();
                    var min = parseInt($(this).attr("min-len"));
                    var max = parseInt($(this).attr("max-len"));
                    var filed = $(this).attr("filed");
                    var require = $(this).attr("require");
                    var val = $(this).val();
                    if(require == "true"){
                        if(val.length == 0){
                            flag = false;
                            msg = $(this).attr("name")+'不能为空！';
                            err.html("<i class='icon-remove f-error'>"+msg+"</i>");
                            $(this).focus().css("border-color","#d9534f");
                            return false;
                        }
                    }
                    if(min){
                        if(val.length < min){
                            flag = false;
                            msg = '最小长度不能小于'+min;
                            err.html("<i class='icon-remove f-error'>"+msg+"</i>");
                            $(this).focus().css("border-color","#d9534f");
                            return false;
                        }

                    }
                    if(max){
                        if(val.length > max){
                            flag = false;
                            msg = '最大长度不能大于'+max;
                            err.html("<i class='icon-remove f-error'>"+msg+"</i>");
                            $(this).focus().css("border-color","#d9534f");
                            return false;
                        }
                    }
                    if(filed){
                        if(filed == "string"){
                            var reg = /^\w+$/;
                            if(!reg.test(val)){
                                flag = false;
                                msg = '请使用字符、数字';
                                err.html("<i class='icon-remove f-error'>"+msg+"</i>");
                                $(this).focus().css("border-color","#d9534f");
                                return false;
                            }
                        }else if(filed == "tel"){
                            var reg = /^1[34578]\d{9}$/;
                            if(!reg.test(val)){
                                flag = false;
                                msg = '手机格式错误';
                                err.html("<i class='icon-remove f-error'>"+msg+"</i>");
                                $(this).focus().css("border-color","#d9534f");
                                return false;
                            }
                        }else if(filed == "chinese"){
                            var reg = /^[\u0391-\uFFE5]+$/;
                            if(!reg.test(val)){
                                flag = false;
                                msg = '请填入中文';
                                err.html("<i class='icon-remove f-error'>"+msg+"</i>");
                                $(this).focus().css("border-color","#d9534f");
                                return false;
                            }
                        }else if(filed == "email"){

                        }else if(filed == "repeat"){
                            var re = $(".modal").find("[name="+$(this).attr("re-for")+"]");
                            if(re.val() != val){
                                flag = false;
                                msg = '两次密码输入不符';
                                err.html("<i class='icon-remove f-error'>"+msg+"</i>");
                                $(this).focus().css("border-color","#d9534f");
                                return false;
                            }
                        }else if(filed == "ip"){

                        }else if(filed == "number"){

                        }
                    }
                    if(flag){
                        err.html("<i class='icon-ok f-success'></i>");
                        $(this).css("border-color","#ccc");
                        return true;
                    }
                });
            });

        },
		//延时刷新页面工具
		refresh_page:function (s) {
			//s:延时的秒数
			setTimeout(function(){  //使用  setTimeout（）方法设定定时2000毫秒
            	window.location.reload(true);//页面刷新
        	},s*1000);
        },
	}
	$.tools  = function(){
		var t = new tools ();
		return t;
	};

})();
