(function(){
	var $contents = document.getElementById("contents");
	var $result = document.getElementById("result");
	var $ignore = document.getElementById("ignoreLetter");
	DOMUtil.getElementsByClassName('input-button')[0].onclick = function(){
		var character=$contents.value.split("");
		var ascii="";
		for(var i=0;i<character.length;i++){
			var code=Number(character[i].charCodeAt(0));
			if(!$ignore.checked||code>127){
				var charAscii=code.toString(16);
				charAscii=new String("0000").substring(charAscii.length,4)+charAscii;
				ascii+="\\u"+charAscii;
			}
			else{
				ascii+=character[i];
			}
		}
		$result.value=ascii;
	};
	DOMUtil.getElementsByClassName('input-button')[1].onclick = function(){
		var character=$result.value.split("\\u");
		var native1=character[0];
		for(var i=1;i<character.length;i++){
			var code=character[i];
			native1+=String.fromCharCode(parseInt("0x"+code.substring(0,4)));
			if(code.length>4){
				native1+=code.substring(4,code.length);
			}
		}
		$contents.value=native1;
	};
})();