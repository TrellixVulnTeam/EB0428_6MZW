const http = require('http')
const request = require('request')
const url = require('url')
const enc = require('./encryption.js')
const Base64 = require('js-base64').Base64;

var secretkey = null
http.createServer((req,res) =>{
    console.log(req.url);
    let {pathname,query} = url.parse(req.url,true)
    if(query.islock == 1){
        secretkey = null
        console.log(secretkey);
    }else{
        if(secretkey == null){
            secretkey = enc.randomWord(false,43,43)
            var start = secretkey.substring(0,21)
            var end = secretkey.substring(21,43)
            console.log(secretkey);
            // console.log("头："+start);
            // console.log("尾："+end);
            // console.log("头长度："+start.length);
            // console.log("尾长度："+end.length);
            
            // console.log("头的二进制："+enc.strToBinary(start));
            // console.log("尾的二进制"+enc.strToBinary(end));
            // console.log("头的二进制转字符串："+enc.binaryToStr(enc.strToBinary(start)));
            // console.log("尾的二进制转字符串："+enc.binaryToStr(enc.strToBinary(end)));
            
            var twokey = enc.randomWord2(true,2,2)
            var twokey2 = enc.randomWord2(true,2,2)
            var twokey3 = enc.randomWord2(true,2,2)
            var twokey4 = enc.randomWord2(true,2,2)
            var endkey = enc.randomWord(true,2,2)
            var endkey2 = enc.randomWord(true,2,2)
            var key = Base64.encode(twokey+"+"+twokey2+"+"+twokey3+"+"+twokey4+"+"+endkey+"+"+endkey2);
            start = enc.strToBinary(start)
            end = enc.strToBinary(end)
            // console.log("转换二进制后的头："+start);
            // console.log("转换二进制后的尾："+end);
            start=start.replace(/\s+/g,twokey+' '+twokey2)
            end=end.replace(/\s+/g,twokey3+' '+twokey4)
            // console.log("二进制更换后的头："+start);
            // console.log("二进制更换后的尾："+end);
            start=enc.binaryToStr(start)
            end=enc.binaryToStr(end)
            // console.log("二进制转字符串更换后的头："+start);
            // console.log("二进制转字符串更换后的尾："+end);
            
            start=Base64.encode(start)+endkey;
            end=Base64.encode(end)+endkey2;
            // console.log(endkey);
            // console.log(endkey2);
            
            // console.log("base加密后的头："+start);
            // console.log("base加密后的尾："+end);
            // start=Base64.decode(start.slice(0,-2));
            // end=Base64.decode(end.slice(0,-2));
            // console.log("base解密后的头："+start);
            // console.log("base解密后的尾："+end);

            var doskey = twokey+"+"+twokey2+"+"+twokey3+"+"+twokey4
            doskey = Base64.encode(doskey);
            // console.log("doskey："+doskey);
            // start=enc.strToBinary(start);
            // end=enc.strToBinary(end);
            // console.log("再次更换二进制后的头："+start);
            // console.log("再次更换二进制后的尾："+start);
            // console.log("twokey："+twokey);
            // console.log("twokey2："+twokey2);
            // console.log("twokey3："+twokey3);
            // console.log("twokey4："+twokey4);
            // if(twokey2[0] == '0'){
            //     if(twokey2[1] == '0'){
            //         start=start.replace(new RegExp(twokey+' ','g')," ")
            //     }else{
            //         twokey2=twokey2.replace('0','')
            //         start=start.replace(new RegExp(twokey+' '+twokey2,'g')," ")
            //     }
            // }else{
            //     start=start.replace(new RegExp(twokey+' '+twokey2,'g')," ")
            // }
            // if(twokey4[0] == '0'){
            //     if(twokey4[1] == '0'){
            //         end=end.replace(new RegExp(twokey3+' ','g')," ")
            //     }else{
            //         twokey4=twokey4.replace('0','')
            //         end=end.replace(new RegExp(twokey3+' '+twokey4,'g')," ")
            //     }
            // }else{
            //     end=end.replace(new RegExp(twokey3+' '+twokey4,'g')," ")
            // }
            // console.log("再次更换后的头："+start);
            // console.log("再次更换后的尾："+end);
            // start=enc.binaryToStr(start);
            // end=enc.binaryToStr(end);
            // console.log("再次字符串更换后的头："+start);
            // console.log("再次字符串更换后的尾："+end);
            // console.log("twokey："+twokey+"+"+twokey2+"+"+twokey3+"+"+twokey4+"+"+endkey+"+"+endkey2);
            // console.log(key)
            secretkey=Base64.encode(secretkey);
            console.log('secretkey:'+secretkey);
            
            var conn = "http://127.0.0.1:8081?iskey=1&secret="+secretkey+"&key="+key
            request(conn,function(error,response,body){
                if(!error && response.statusCode == 200){
                    console.log(body);
                    res.end(JSON.stringify({
                        err:'200',
                        one:start,
                        two:end,
                        doskey:doskey
                    }))
                }else{
                    res.end(JSON.stringify({
                        err:'500',
                        message:'Not Found 500!'
                    }))
                }
                secretkey = null
            })
        }else{
            console.log("此处应有值："+secretkey);
            res.end(JSON.stringify({
                err:'404',
                message:'Exception operation!'
            }))
            secretkey = null
        }
    }
}).listen(9090)