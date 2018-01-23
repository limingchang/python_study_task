(function(){
	$.fn.extend({
		'createTrByGet':function(url){
			var table = $(this);
			var tableData;
			$.getJSON(url, function(json){
				tableData = json;
				$.createTable(table,tableData);
			});
		},
		"saveTableData":function(url){
			//var url = "data/table_data.js";
			$.getJSON(url, function(json){
				return json;
			}); 
		}
	})
	$.extend({
		'createTable':function(table,tableData,type=true){
			//table,要添加数据的表格jQuery对象
			//tableData ,表格数据
			//type，是否清空表格后创建，默认true
			if(type){table.empty()}
			for(item in tableData['data']){
					var tr = document.createElement('tr');
					for(host in tableData['data'][item]){
						var tdKey = host;
						var tdData = tableData['data'][item][host];
						var td = document.createElement('td');
						//console.log(tdKey+':'+tdData);
						if(host == 'id'){
							var checkbox = document.createElement('input');
							$(checkbox).attr('type','checkbox').attr('name',tdKey).attr('value',tdData);
							$(td).append(checkbox);
						}else if(host == 'host_status'){
							var select = document.createElement('select');
							select.options.add(new Option("在线",0)); //这个兼容IE与firefox 
							select.options.add(new Option("下线",1));
							$(select).val(tdData);
							$(select).attr("disabled","disabled");
							$(td).attr('name',tdKey).append(select);
						}else{
							$(td).addClass('edit-td');
							$(td).attr('name',tdKey).text(tdData);
						}
						$(tr).append(td);
					}
					var td = document.createElement('td');
					var btn = document.createElement('button');
					$(btn).addClass('btn btn-cancel btn-ml').text('删除');
					$(btn).attr('name','delete');
					$(td).append(btn);
					$(tr).append(td);
					table.append(tr);
				}
		},
		'showTips':function(msg,tips_type='tips-info',tips_position='tips-lefttop'){
			//console.log(msg,tips_type,tips_position);
			var tips = document.createElement('div');
				$(tips).addClass('tips').addClass(tips_type).addClass(tips_position).text(msg);
				var span = document.createElement('span');
				$(span).text('X').addClass('tips-span').click(function(){
					$(tips).remove();
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
					pos_y = $('.'+tips_position+':last').prev().outerHeight()+$('.'+tips_position+':last').prev().offset().top+5;
					console.log($('.'+tips_position+':last').prev());
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
		
	})
	//模态弹出框插件
	var Dialog = function(ele,opt){
		this.$element = ele;
		this.div = '';
		this.shadow ='';
		this.defaults = {
			'title':'对话框',
			'msg':'提示消息',
			'type':'okcancel'
		};
		this.options = $.extend({},this.defaults, opt);
	}
	Dialog.prototype = {
		_rander:function(){
			//插件渲染
			var dialog = document.createElement('div');
			$(dialog).addClass('modal-dialog light-blue');
			var title = document.createElement('div');
			$(title).addClass('modal-title blue').text(this.options.title);
			var text = document.createElement('div');
			$(text).addClass('modal-dialog-text').text(this.options.msg);
			var btn = document.createElement('div');
			$(btn).addClass('modal-dialog-btn');
			var btn_sure = document.createElement('button');
			$(btn_sure).text('确认').addClass('btn btn-xl btn-info').attr('name','sure');
			var btn_cancel = document.createElement('button');
			$(btn_cancel).text('取消').addClass('btn btn-xl btn-cancel').attr('name','cancel');
			$(btn).append(btn_sure).append(btn_cancel);
			$(dialog).append(title).append(text).append(btn);
			this.div = $(dialog);
			this.shadow = $(document.createElement('div')).addClass('shadow light-blue');
			$('body').append(this.shadow).append(this.div);
			
		},
		_bind:function(that){
			//事件绑定
			var ele = that.$element;
			//console.log('bing:'+ele);
			//console.log('_bind:'+that.$element)
			this.div.on('click','.btn-xl',function(){
				//console.log(this);
				var type = $(this).attr('name');
				var res;
				if(type=='sure'){
					res = true;
					that.$element.remove();
				}else if(type=='cancel'){
					res = false;
				}else{
					
				}
				that._destory();
			});
		},
		_destory:function(){
			this.div.remove();
			this.shadow.remove();
		},
		show:function(){
			this._rander();
			//$('body').append(this.$element);
			this._bind(this);
		}
	}
	//注册插件
	$.Dialog = function(ele,opt){
		var d = new Dialog(ele,opt);
		return d;
	}
	//拖动组件插件
	var drag_div = function(drag_ele,control_ele,pos_limit){
		/**
		 * drag_ele,要注册拖动的jQuery对象
		 * control_ele,控制（触发）drag_ele拖动的jQuery对象
		 * pos_limit,拖动位置限制
		 * 
		 * */
		this.d_ele = drag_ele;
		this.c_ele = control_ele;
		this.limit = {
			mix_x:0,
			min_y:0,
		};
		this.limit_pos = $.extend({},this.limit,pos_limit);
	};
	drag_div.prototype={
		//样式渲染
		_rander:function(){
			this.c_ele.css('cursor','move');
		},
		//事件监听
		_on:function(that){
			this.c_ele.mousedown(function(e){
				that._rander();
				var pos_x = e.pageX - that.d_ele.offset().left;
				var pos_y = e.pageY - that.d_ele.offset().top;
				var pos = {left:pos_x,top:pos_y};
				var min_x = that.limit_pos.min_x;
				var max_x = $(window).width()-that.c_ele.width();
				var min_y = that.limit_pos.min_y;
				var max_y = $(window).height()-that.c_ele.parent().height();
				$(document).mousemove(function(e_move){
					var _x = e_move.pageX - pos.left;
					var _y = e_move.pageY - pos.top;
					_x = _x<=min_x?min_x:_x;
					_x = _x>=max_x?max_x:_x;
					_y = _y<=min_y?min_y:_y;
					_y = _y>=max_y?max_y:_y;
					var move_pos = {left:_x,top:_y}
					//console.log(move_pos);
					that.d_ele.offset(move_pos);
				});
			});
			$(document).mouseup(function(){
				that._destory();
			})
		},
		//销毁
		_destory:function(){
			this.c_ele.css('cursor','default');
			$(document).off('mousemove');
		},
		//初始化
		init:function(){
			this._on(this);
		}
	}
	//注册插件
	$.dragElement = function(drag_ele,control_ele,pos_limit){
		var drag = new drag_div(drag_ele,control_ele,pos_limit);
		return drag;
	}
	//ctrl捕捉批量修改
	var ctrlEdit = function(active_ele,edit_ele){
		/**
		 * active_ele;注册事件的jQuery对象
		 * edit_ele;事件触发时批量修改的jQuery对象
		 */
		this.active_ele = active_ele;
		this.edit_ele = edit_ele;
		this.key = false;
		$(window).keyup(function(){
			key = 0;
		})
	};
	ctrlEdit.prototype = {
		init:function(){
			this._on(this);
		},
		_on:function(that){
			$(window).keydown(function(e){
				that.key = e.ctrlKey;
				that.active_ele.on('change','',function(){
					if(that.key){
						that.edit_ele.val($(this).val());
					}
				});
			});
			$(window).keyup(function(){
				that.key = false;
			})
		},
		_destory:function(){
			$(window).off('keydown');
			$(window).off('keyup');
		}
	}
	$.ctrlEdit = function(active_ele,edit_ele){
		var c = new ctrlEdit(active_ele,edit_ele);
		return c;
	}
})()

