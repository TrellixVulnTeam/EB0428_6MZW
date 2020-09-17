'use strict'

var enc = {
    randomWord: function randomWord(randomFlag, min, max){
        var str = "",
            range = min,
            arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
            'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 
            'W', 'X', 'Y', 'Z',  "!", '@', '$', '%',  '*', '(', ')', 
            '-', '_', '~', '|', '/'];
    
        // 随机产生
        if(randomFlag){
            range = Math.round(Math.random() * (max-min)) + min;
        }
        for(var i=0; i<range; i++){
            var pos = Math.round(Math.random() * (arr.length-1));
            str += arr[pos];
        }
        return str;
    },
    randomWord2: function randomWord2(randomFlag, min, max){
        var str = "",
            range = min,
            arr = ['0', '1'];
    
        // 随机产生
        if(randomFlag){
            range = Math.round(Math.random() * (max-min)) + min;
        }
        for(var i=0; i<range; i++){
            var pos = Math.round(Math.random() * (arr.length-1));
            str += arr[pos];
        }
        return str;
    },
    //将二进制字符串转换成Unicode字符串
    binaryToStr: function binaryToStr(str){
        var result = [];
        var list = str.split(" ");
        for(var i=0;i<list.length;i++){
                var item = list[i];
                var asciiCode = parseInt(item,2);
                var charValue = String.fromCharCode(asciiCode);
                result.push(charValue);
        }
        return result.join("");
    },
    //将字符串转换成二进制形式，中间用空格隔开
    strToBinary:function strToBinary(str){
        var result = [];
        var list = str.split("");
        for(var i=0;i<list.length;i++){
            if(i != 0){
                result.push(" ");
            }
            var item = list[i];
            var binaryStr = item.charCodeAt().toString(2);
            result.push(binaryStr);
        }   
        return result.join("");
    }
}

module.exports = enc