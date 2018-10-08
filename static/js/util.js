$(document).ready(function(){
	$("#selectAll").click(function(){
		if (this.checked) {
			$("tbody :checkbox").prop("checked",true);
		} else {
			$("tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll1").click(function(){
		if (this.checked) {
			$("#item-1 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-1 tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll2").click(function(){
		if (this.checked) {
			$("#item-2 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-2 tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll3").click(function(){
		if (this.checked) {
			$("#item-3 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-3 tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll4").click(function(){
		if (this.checked) {
			$("#item-4 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-4 tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll5").click(function(){
		if (this.checked) {
			$("#item-5 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-5 tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll6").click(function(){
		if (this.checked) {
			$("#item-6 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-6 tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll7").click(function(){
		if (this.checked) {
			$("#item-7 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-7 tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll8").click(function(){
		if (this.checked) {
			$("#item-8 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-8 tbody :checkbox").prop("checked",false);
		}
	})

	$("#selectAll9").click(function(){
		if (this.checked) {
			$("#item-9 tbody :checkbox").prop("checked",true);
		} else {
			$("#item-9 tbody :checkbox").prop("checked",false);
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