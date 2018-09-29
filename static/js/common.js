$(function() {
	initInput();
	iconButton();
	initSubtitle();
	initDatagrid();
	aImgOver();
});

function initDatagrid() {
	var jtable = $("table[type=data]");
	var jthead = jtable.find("thead");
	var jbody = jtable.find("tbody");

	jbody.find("tr").hover(function() {
		$(this).addClass("trHover");
	}, function() {
		$(this).removeClass("trHover");
	});

	jbody.find("input[type=checkbox]").click(
			function() {
				if (jbody.find("input[type=checkbox]").length == jbody
						.find("input[type=checkbox][checked]").length) {
					jthead.find("input[type=checkbox]").attr("checked",
							"checked");
				} else {
					jthead.find("input[type=checkbox]").removeAttr("checked");
				}
			});

	jthead.find("input[type=checkbox]").click(
			function() {
				var jchecks = $(this).parents("table").find(
						"tbody input:checkbox").filter(function() {
					return $(this).attr("disabled") != true;
				});

				if ($(this).prop("checked")) {
					jchecks.prop("checked", "checked");
				} else {
					jchecks.removeAttr("checked");
				}
			});
	
	jbody.find("tr").dblclick(
			function() {
				if ($(this).find("input[type=radio]").length > 0) {
					$(this).find("input[type=radio]").click();
				}

				if ($(this).find("input[type=checkbox]").length > 0) {
					$(this).find("input[type=checkbox]").click();
				}

				if (jbody.find("input[type=checkbox]").length == jbody
						.find("input[type=checkbox][checked]").length) {
					jthead.find("input[type=checkbox]").attr("checked",
							"checked");
				} else {
					jthead.find("input[type=checkbox]").removeAttr("checked");
				}
			});
}

function initSubtitle() {
	$(".subtitle").click(function() {
		var t = $(this).parent().parent().next("tbody");
		t.toggle();

		if (t.get(0).style.display == "none") {
			$(this).get(0).className = "subtitleClose";
		} else {
			$(this).get(0).className = "subtitle";
		}
	});
	$(".subtitleClose").click(function() {
		var t = $(this).parent().parent().next("tbody");
		t.toggle();

		if (t.get(0).style.display == "none") {
			$(this).get(0).className = "subtitleClose";
		} else {
			$(this).get(0).className = "subtitle";
		}
	});

}

function iconButton(p) {
	p = p || document.body;
	$(":image", p).addClass("iconBtn") 
	.hover(function() {
		$(this).attr("class", "iconBtnOver");
	}, function() {
		$(this).attr("class", "iconBtn");
	}).mousedown(function() {
		$(this).attr("class", "iconBtnDown");
	}).mouseout(function() {
		$(this).attr("class", "iconBtn");
	});

	$(":image:disabled", p).addClass("iconBtnDisabled").attr("title", "不可用");
}

function initInput(p) {
	p = p || document.body;
	var inputFocus = "inputOn";
	var inputDisabled = "inputDisabled";
	var inputReadonly = "inputReadonly";
	var buttonDisabled = "buttonDisabled";
	$("input:text:disabled,input:password:disabled,textarea:disabled", p)
			.addClass(inputDisabled);
	$("input:text[readonly],input:password[readonly],textarea[readonly]", p)
			.not("[nochange]").addClass(inputReadonly);

	$("input:text,textarea").not("[readonly]").focus(function() {
		$(this).addClass(inputFocus);
	}).blur(function() {
		$(this).removeClass(inputFocus);
	});
	$(":button[disabled],:reset[disabled],:submit[disabled]").addClass(
			buttonDisabled);
}

var popUpWin = 0;
function popUp(url, width, height, winname, left, top) {
	if (popUpWin) {
		if (!popUpWin.closed)
			popUpWin.close();
	}
	if (isNaN(width)) {
		width = screen.width / 2;
	}
	if (isNaN(height)) {
		height = screen.height / 2;
	}
	if (isNaN(left)) {
		left = (screen.width - width) / 2;
	}
	if (isNaN(top)) {
		top = (screen.height - height) / 2;
	}
	var winnames = (winname == '') ? 'popUpWin' : winname;
	popUpWin = window
			.open(
					url,
					winnames,
					'toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,copyhistory=yes,width='
							+ width
							+ ',height='
							+ height
							+ ',left='
							+ left
							+ ', top='
							+ top
							+ ',screenX='
							+ left
							+ ',screenY='
							+ top + '');
}
function goback() {
	history.back();
}


function showDialog(url, width, height, jsonObj, sFeatures) {

	if (isNaN(width)) {
		width = screen.width / 2;
	}
	if (isNaN(height)) {
		height = screen.height / 2;
	}
	var left = (screen.width - width) / 2;
	var top = (screen.height - height) / 2;

	if (sFeatures == undefined) {
		sFeatures = "dialogHeight:" + height + "px; dialogWidth:" + width
				+ "px;" + "dialogLeft:" + left + "px;dialogTop:" + top
				+ "px;status:no;";
	} else
		sFeatures += "dialogHeight:" + height + "px; dialogWidth:" + width
				+ "px;" + "dialogLeft:" + left + "px;dialogTop:" + top
				+ "px;status: no;";
	if (jsonObj == undefined) {
		jsonObj = "";
	}
	var rtn = window.showModalDialog(url, jsonObj, sFeatures);
	return rtn;
}

function aImgOver() {
	var obj = $("img").not("[noOver]");
	obj.parent().parent("td").width("60");
	obj.not("[class='readonly']").each(function(i) {
		if ($(this).parent("a")) {
			$(this).hover(function() {
				$(this).addClass("aImgOver");
			}, function() {
				$(this).removeClass("aImgOver");
			});
		}
	});
}

function toutf8(s) {   
    var out, i, len, c;   
    out = "";   
    len = s.length;   
    for(i = 0; i < len; i++) {   
    	c = s.charCodeAt(i);   
    	if ((c >= 0x0001) && (c <= 0x007F)) {   
        	out += s.charAt(i);   
    	} else if (c > 0x07FF) {   
        	out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));   
        	out += String.fromCharCode(0x80 | ((c >>  6) & 0x3F));   
        	out += String.fromCharCode(0x80 | ((c >>  0) & 0x3F));   
    	} else {   
        	out += String.fromCharCode(0xC0 | ((c >>  6) & 0x1F));   
        	out += String.fromCharCode(0x80 | ((c >>  0) & 0x3F));   
    	}   
    }   
    return out;   
}