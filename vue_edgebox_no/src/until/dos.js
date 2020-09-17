const http = require('http')
const url = require('url')
const request = require('request')
const Base64 = require('js-base64').Base64;

var secretKey = null
var key = []
var connkey = 'http://127.0.0.1:9090/?islock=1'
http.createServer((req,res)=>{
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
    res.setHeader('Content-Type', 'application/json')
    let {pathname,query} = url.parse(req.url,true)
    console.log("此处为路径："+pathname)
    if(query.iskey == 0){
        // console.log("false")
        console.log("此处应为secretKey："+secretKey)
        console.log("此处为参数："+JSON.stringify(query))
        console.log("此处为参数："+(JSON.parse(JSON.stringify(query))).hasOwnProperty("secretkey"))
        console.log("此处为方法："+req.method)
        if(secretKey != null || secretKey != ''){
            if(((JSON.parse(JSON.stringify(query))).hasOwnProperty("secretkey")) && ((JSON.parse(JSON.stringify(query))).hasOwnProperty("doskeyArr"))){
                var start = query.secretkey.substring(0,21)
                var doskey = query.secretkey.substring(21,25)
                var end = query.secretkey.substring(25,47)
                var keyArr = JSON.parse(query.doskeyArr)
                query.secretkey = start+end
                // console.log("key:"+key)
                // console.log("keyArr:"+keyArr)
                // console.log("开始："+start)
                // console.log("doskey："+doskey)
                // console.log("结束："+end)
                // console.log("query.secretkey:"+query.secretkey)
                if(secretKey === query.secretkey){
                    console.log("secretkey相等:")
                    console.log("query.secretkey:"+query.secretkey)
                    console.log("secretKey:"+secretKey)
                    console.log("key:"+key)
                    console.log("keyArr:"+keyArr)
                    if(key[1][0] == 0){
                        if(key[1][1] == 0){
                        
                        }else{
                            key[1] = key[1].replace("0","")
                        }
                    }
                    if(key[3][0] == 0){
                        if(key[3][1] == 0){
                        
                        }else{
                            key[3] = key[3].replace("0","")
                        }
                    }
                    if(key[0] == keyArr[0] && key[1] == keyArr[1] && key[2] == keyArr[2] && key[3] == keyArr[3] && key[4]+key[5] == doskey){
                        var conn = 'http://10.167.198.95:9090/apis/yuancheng/getlog/?action='+query.ip
                        console.log("秘钥相等:")
                        console.log("key:"+key)
                        console.log("keyArr:"+keyArr)
                        var data = {}
                        request(conn,function(error,response,body){
                            if(!error && response.statusCode == 200){
                                data = JSON.parse(body)
                                // console.log(body);
                                console.log(data);
                                // console.log(data['db']);
                                res.end(JSON.stringify({
                                    err:true,
                                    db:data['db']
                                }))
                            }else{
                                console.log(error);
                                res.end(JSON.stringify({
                                    err: false,
                                    message:"Not Found 500!"
                                }))
                            }
                        })
                    }else{
                        console.log("秘钥不相等:")
                        console.log("key:"+key)
                        console.log("keyArr:"+keyArr)
                        res.end(JSON.stringify({
                            err: false,
                            message:"Not Found 404！"
                        }))
                    }
                }else{
                    console.log("secretkey不相等:")
                    console.log("query.secretkey:"+query.secretkey)
                    console.log("secretKey:"+secretKey)
                    res.end(JSON.stringify({
                        err: false,
                        message:"Secretkey Exception！"
                    }))
                }
            }else{
                console.log("此处缺少字段："+JSON.stringify(query));
                res.end(JSON.stringify({
                    err: false,
                    message:"Missing fields！"
                }))
            }
        }else{
            console.log("此处secretKey不存在："+secretKey);
            res.end(JSON.stringify({
                err: false,
                message:"Secretkey Error！"
            }))
        }
        request(connkey,function(error,response,body){
            if(!error && response.statusCode == 200){
                data = JSON.parse(body)
                console.log(data);
            }
        })
        secretKey = null
    }else if(query.iskey == 1){
        if(secretKey == null){
            secretKey = query.secret
            console.log("此处为未解密secretKey："+secretKey);
            if(secretKey.indexOf(" ")){
                secretKey=secretKey.replace(" ","+")
            }
            secretKey=Base64.decode(secretKey);
            console.log("此处为解密后secretKey："+secretKey);
            var basekey = query.key
            basekey = Base64.decode(basekey)
            key = basekey.split('+')
            console.log("此处为秘钥："+key);
            
            res.end(JSON.stringify({
                get:true
            }))
        }else{
            res.end(JSON.stringify({
                get:false
            }))
        }
    }else{
        res.end("Not Found 404！")
    }
}).listen("8081")