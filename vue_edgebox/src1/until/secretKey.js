let enc = require("./encryption.js")

function log(str,boo){
    var max = 160
    var changeStr = ""
    //匹配中文
    var regular = str.match(/[\u4E00-\u9FA5]/g)
    var regular2 = str.match(eval(/[！：；。，、）（]/ig))
    var regular4 = str.match(/[\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]/g)
    // console.log(regular);
    // console.log(regular2);
    // console.log(regular4);
    
    var len = 0
    if(max > str.length + 2){
        len = max - str.length
        if(regular != null){
            // if(regular.length <= 1) len = len - 1
            // len = len - regular.length  
            // if((len % 2) == 0)
        }
        if(regular2 !== null){
            // if(regular2.length <= 1)  len = len - 1
            // len = len - ((regular2.length / 2) + 1)
            // len = len - regular2.length
            
            // len = len - (regular2.length / 2).toFixed(0)
            // if((len % 2) != 0) len = len -1
        }
        for(var i = 0; i < len; i++){
            if(i < (len / 2).toFixed(0)){
                (i == 0) ? changeStr += "*" : (boo == true) ? changeStr += "*" : changeStr += " "
                
            }
            if(i == (len / 2).toFixed(0)){
                changeStr = changeStr + str
            }
            if(i >= (len / 2).toFixed(0)){
                
                if(i == ((len / 2)+1).toFixed(0)){
                    // console.log(changeStr.length);
                    if(regular != null){
                        len = len - (regular.length-2)
                        // console.log(regular.length*2);
                    }
                    if(regular2 != null){
                        // console.log(regular2);
                        // if(regular2.length != 1) len = len - regular2.length
                        len = len - (regular2.length-2)
                        // if(regular == null && regular2.length == 1) len = len - regular2.length
                        
                        // console.log(regular2.length*2);
                    }
                }
                
                (i == (len - 1).toFixed(0)) ? changeStr += "*" : (boo == true) ? changeStr += "*" : changeStr += " "
            }
        }
        // console.log(changeStr.length);
        console.log(changeStr);
    }else{
        var arr = []
        var n = 120
        for(var i = 0; i < str.length/n; i++){
            var splitStr = str.slice(n*i,n*(i+1))
            arr.push(splitStr)
        }
        
        for(var i = 0; i < arr.length; i++){
            log(arr[i], boo)
        }
    }
}

function secretkey(str){
    log("12ab")
    log("！！！！")
    log("123！！！@#啊")
    log("啊")
    log("啊啊")
    log("啊啊啊")
    log("！")
    log("！！")
    log("！！！")
    log("12ab!")
    log("12ab!！")
    log("12ab!！！")
    log("12ab!！！！")
    log("12ab!！！！！")
    var binary1 = enc.randomWord2(true,7,7)
    var binary2 = enc.randomWord2(true,7,7)
    var binary3 = enc.randomWord2(true,7,7)
    log("加密",true)
    log("SEC字符串：" + str,true);
    log("!@#$%^&&*！：“",false);
    log("SEC未改变二进制：" + enc.strToBinary(str),false);
    str = changeBinary(str,false) + " " + binary1 + " " + binary2 + " " + binary3 + " "
    log("SEC改变二进制并添加虚拟二进制后：" + str ,false);
    var len = str.split(/\s+/g)
    var change = ""
    len.forEach((v,i) =>{
        if(i != len.length - 1){
            if(v.length >= 15){
                change = change + v
            }else{
                change = change + (v + enc.randomWord2(true,2,2))
            }
            change = change + " "
        }
    })
    // str = str.replace(/\s+/g,endkey+' ')
    str = change
    // str = str.substring(0, str.length-1)
    log("SEC替换二进制后：" + str,false);

    str=enc.binaryToStr(str)
    log("SEC二进制转字符串：" + str,false);
    
    var a = new Array();
    //min:33 , max:126
    //min:-127 , max:
    for(var i = 0; i <= 350; i++){
        a[i] = i -127
    }
    
    log("SEC改变byte前：" + enc.stringToByte(str),false);
    
    str = changeByte(str, true)
    log("SEC改变byte后：" + str,false);
    
    str = enc.byteToString(str)
    log("SECbyte转字符串：" + str,false);
    
    str = changeBinary(str,false)
    log("SEC改变二进制：" + str,false);

    str = enc.binaryToStr(str)
    log("SEC二进制转字符串：" + str,false);

    str = Base64.encode(str);
    log("SECbase64加密：" + str,true);
    
    return str;
}

function changeSecret(str){
    log("解密",true);
    
    log("changeSEC：" + str,true);
    str = Base64.decode(str)
    log("changeSECbase64解密：" + str,false);

    str = changeBinary(str,false)
    log("changeSEC改变二进制后：" + str,false);

    str = enc.binaryToStr(str)
    log("changeSEC二进制转字符串：" + str,false);
    
    log("changeSEC改变byte前：" + enc.stringToByte(str),false);
    str = changeByte(str, false)
    log("changeSEC改变byte后：" + str,false);

    str = enc.byteToString(str)
    log("changeSECbyte转字符串：" + str,false);

    str = changeBinary(str,true)
    log("changeSEC改变二进制：" + str,false);
    
    str = enc.binaryToStr(str)
    log("changeSEC二进制转字符串：" + str,true); 
    return str
}

function changeByte(str,boo){
    str = enc.stringToByte(str)
    
    if(boo == true){
        str.forEach((v,i) =>{
            if((i+1) < str.length) (v-120 >= 100) ? str[i] = v - 120 : str[i] = v - 100
            // if((i+1) < str.length) str[i] = v - 50
        })
    }else if(boo == false){
        str.forEach((v,i) =>{
            if((i+1) < str.length) (v >= 100) ? str[i] = v + 120 : str[i] = v + 100
            // if((i+1) < str.length) str[i] = v + 50
        })
    }
    return str
}

function changeBinary(list,boo){
    // console.log("=========================================")
    list = enc.strToBinary(list)
    // console.log("list:" + list);
    
    list = list.split(/\s+/g)
    if(list[list.length-1] == 0){
        list.pop();
    }
    
    let changeList = null
    list.forEach((v, i) => {
        // if(boo == true && v.length >= 15){
        //     console.log(v);
        //     v = 1 + v
        //     console.log(v);
            
        // }
        if(changeList == null){
            changeList = v[0]
        } else {
            changeList = changeList + v[0]
        }
        for(let si = 1; si < v.length ; si++){
            if(v[si] == 0){
                changeList = changeList + "1"
            }else if(v[si] == 1){
                changeList = changeList + "0"
            }
        }
        if((i+1) < list.length) changeList = changeList + " "
    });

    if(boo == true){
        list = (changeList.substring(0,changeList.length-2)).split(/\s+/g)
        changeList = null
        list.forEach((v,i) => {
            if(i < (list.length-3) && changeList != null) changeList = changeList + " " + ((v.length < 15) ? v.substring(0,v.length-2) : v)
            if(changeList == null) changeList = ((v.length < 15) ? v.substring(0,v.length-2) : v)
        })
    }
    return changeList
}

export default{
    secretkey,
    changeSecret,
}