function b(){
	h = $(window).height();
	t = $(document).scrollTop();
	if(t > h){
		$('#gotop').show();
	}else{
		$('#gotop').hide();
	}
}
$(document).ready(function(e) {
	b();
	$('#gotop').click(function(){
		$(document).scrollTop(0);	
	});

	document.onkeydown = function(e){
		e = e || window.event;
		if(e.keyCode == 27){
			$('.show_address').prev().remove();
			$('.show_address').remove();
		}
	}
});

$(window).scroll(function(e){
	b();		
});

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
		}
	}
});

//显示我的联系地址
function showAddress(){
	var data = {'action':'getAddress'};

	$.ajax({
		url:'/blog/ajax/',
		type:'post',
		data:data,
		dataType:'json',
		success:function(msg){
			var html = "<div style='width:150%;height:150%;position: fixed;top:0;_position:absolute;_bottom:auto;" +
				"_top:expression(eval(document.documentElement.scrollTop));z-index:99;background:#fff;opacity:0.1;" +
				"filter:alpha(opacity=10);'></div><div class='show_address'><h1>我的联系地址</h1><p>电话："+msg.my_phone+"</p>" +
				"<p>Email："+msg.my_email+"</p><p>QQ："+msg.qq+"</p><p>Winxin："+msg.weixin+"</p><p>微博："+msg.weibo+"</p>" +
				"<span title='Esc or Close' onclick='closeAddress(this);'>X</span></div>";
			$('body').append(html);
			$('.show_address').fadeIn('slow');
		},
		error:function(){
			alert('系统出现异常，正在处理中...');
		}
	});
}

//关闭弹窗
function closeAddress(obj){
	$(obj).parent().fadeOut('slow');
	$(obj).parent().prev().remove();
	$(obj).parent().remove();
}