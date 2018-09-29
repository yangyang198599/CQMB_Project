$(document).ready(function(){
	$("#selectAll").click(function(){
		if (this.checked) {
			$("tbody :checkbox").prop("checked",true);
		} else {
			$("tbody :checkbox").prop("checked",false);
		}
	})

	$(window).bind("load", function() { 
	var mainHeight = 0, 
	$main = $(".main");  
	
	positionFooter(); 
	//定义positionFooter function 
	function positionFooter() { 
		mainHeight = $main.height(); 

		//如果页面内容高度小于屏幕高度，footer将固定定位到屏幕底部，否则footer取消固定定位
		if ( mainHeight < document.documentElement.clientHeight) { 		
			$("footer").css({"bottom":"0","position":"fixed"});
		
	    }else {
	    	$("footer").css({"position":"static"});
	    } 
	} 
	$(window).scroll(positionFooter).resize(positionFooter); 
	}); 


})