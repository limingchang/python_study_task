(function(){
	$.extend({
		'showTips':function(msg,tips_type='info',tips_position='tips-lefttop'){
			//console.log(msg,tips_type,tips_position);
			var tips = document.createElement('div');
				$(tips).addClass('tips').addClass(tips_type).addClass(tips_position).text(msg);
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
			"ajaxType":"post",
			"data":{},
			"requestDataType":"JSON",
			"async":false,//ajax模式，true异步，false同步
			//同步模式会阻塞其他js运行
			"callback":this.__callback__(),
		}
		this.res_data = "";
		this.options = $.extend({},this.defaults, opt);
		this.__inti__();
		return this.res_data;

	}
	ajaxData.prototype = {
		__inti__:function(){

			if(this.options.type == "API"){
				console.log("调用api");
			}else if(this.options.type == "USER_AUTH"){
				console.log("登录认证");
				this.__loginAuth__();
			}else if(this.options.type == "AUTH_CODE"){
			    console.log("获取验证码");
				this.__authCode__();
			}

		},
		__authCode__:function(){
		    this.__ajax__(this,"/auth_code/");

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
				this.__ajax__(this,"/login/");
				res = this.res_data;
			}
			this.res_data = res;
		},
		__ajax__:function(that,url){

			$.ajax({
				type:that.options.ajaxType,
				url:url,
				beforeSend:function(XMLHttpRequest){
				    if(that.options.type=="API"){
				        XMLHttpRequest.setRequestHeader('accessToken','limich123');
				    }
				},
				data:that.options.data,
				success:function(data,that){
				    formatData(data);
				},
				complete:function(XMLHttpRequest){

				},
				async:that.options.async,
			});
			function formatData(data){
			    if(that.requestDataType == 'JSON'){
                     that.res_data = data;
			    }else{
			        that.res_data = {
			            "errNum":0,
			            "errMsg":"ok",
			            "data":data,
			        }
			    }


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
		return a;
	}
	//工具
	var tools = function(){
		
	}
	tools.prototype = {
		trim:function(str){
			return str.replace(/(^\s*)|(\s*$)/g, ""); 
		},
	}
	$.tools  = function(){
		var t = new tools ();
		return t;
	}	
})();
