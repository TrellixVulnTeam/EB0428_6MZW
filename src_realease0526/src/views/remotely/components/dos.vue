<template>
    <el-card id="card" class="box-card" style="background:black;color:white;max-height:27.2em;overflow:auto" @click="autoFocus()">
        <div id="text" style="background:black;color:white;" @click="autoFocus()">
            <ul id="ul">
                <li v-for="(i,b) in total" :key="b">{{i}}<br/></li>
            </ul>
            <el-input
            v-loading= "loading"
            type="text"
            id="in"
            class="input_text"
            v-model="command"
            resize="none"
            @keyup.enter.native="enter()"
            autofocus="autofocus">
            <span slot="prepend" style="font-size:18px">></span>
            </el-input>
        </div>
    </el-card>
</template>

<style>
    ul {
        margin:0px;
        padding:0px;
        list-style:none;
    }
    .input_text .el-input__inner:focus{
        border: 1px solid black;
    }
    .input_text .el-input__inner:hover{
        border: 1px solid black;
    }
    .input_text .el-input__inner{
        color:green;
        border: 1px solid black;
        background-color:black;
    }
    .input_text .el-input-group__prepend{
        padding:0px;
        color:white;
        border: 1px solid black;
        background-color:black;
    }
</style>

<script>
// let path = require("path")
// alert(path.resolve(__dirname,"dos.vue"))
const enc = require('../../../until/encryption.js')
const Base64 = require('js-base64').Base64;
export default {
  data () {
    return {
      command: '',
      loading: false,
      total: ['Welcome！You can enter：ping 192.168.1.1',' ']
    }
  },
  created () {
  },
  directives: {
    focus: {
      inserted: function (el, { value }) {
        // console.log(el, { value })
        if (value) {
          el.focus()
        }
      }
    }
  },
  watch: {
    loading: {
      handler (newVal, oldVal) {
        if (newVal == false) {
          this.scoll()
        }
      },
      deep: true
    }
  },
  methods: {
    enter () {
      var _this = this
      var ip = $('#in').val()
      this.loading = true
      if (ip.indexOf('ping ') >= 0 || ip === 'ipconfig' || ip === 'ipconfig /all') {
        _this.total.push('>' + ip)
        this.$axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8' // 此处是增加的代码，设置请求头的类型
        this.$axios.defaults.timeout = 1000 * 60 * 2
        // 单独指令
        // ip = ip.replace("ping ","");
        // this.$axios.get("/yuancheng/getlog/?ip="+ip)
        // this.$axios.get("/yuancheng/getlog/",{
        //   params:{
        //     action:ip
        //   }

        this.$axios.get("/secKey")
          .then(response =>{
            if(response.data.err == '200'){
              var one = response.data.one
              var two = response.data.two
              var doskey = response.data.doskey
              var onekey = one.substr(one.length-2)
              var twokey = two.substr(two.length-2)
              var start=Base64.decode(one.slice(0,-2));
              var end=Base64.decode(two.slice(0,-2));
              doskey = Base64.decode(doskey);
              var doskeyArr = doskey.split('+')
              start=enc.strToBinary(start);
              end=enc.strToBinary(end);
              
              if(doskeyArr[1][0] == '0'){
                  if(doskeyArr[1][1] == '0'){
                      start=start.replace(new RegExp(doskeyArr[0]+' ','g')," ")
                  }else{
                      doskeyArr[1]=doskeyArr[1].replace('0','')
                      start=start.replace(new RegExp(doskeyArr[0]+' '+doskeyArr[1],'g')," ")
                  }
              }else{
                  start=start.replace(new RegExp(doskeyArr[0]+' '+doskeyArr[1],'g')," ")
              }
              if(doskeyArr[3][0] == '0'){
                  if(doskeyArr[3][1] == '0'){
                      end=end.replace(new RegExp(doskeyArr[2]+' ','g')," ")
                  }else{
                      doskeyArr[3]=doskeyArr[3].replace('0','')
                      end=end.replace(new RegExp(doskeyArr[2]+' '+doskeyArr[3],'g')," ")
                  }
              }else{
                  end=end.replace(new RegExp(doskeyArr[2]+' '+doskeyArr[3],'g')," ")
              }
              // console.log(doskeyArr);
              
              start=enc.binaryToStr(start);
              end=enc.binaryToStr(end);
              var secretkey = start+onekey+twokey+end
              // console.log("加入秘钥的秘钥："+secretkey);
              this.$axios.get("/command",{
                params:{
                  ip:ip,
                  iskey:0,
                  secretkey:secretkey,
                  doskeyArr:JSON.stringify(doskeyArr)
                }
              }).then(response =>{
                  if(response.data.err == true){
                    // 所有指令
                    var db = response.data.db
                    // console.log(response.data)
                    var array = []
                    array.push(db.split('&'))
                    for (var i in array[0]) {
                      _this.total.push(array[0][i])
                    }
                    $('#in').val('') // 清空输入框
                    $('#text').scrollTop($('#text').scrollTop() + 32)// 滚动条拉到最下面，显示出输入框
                    _this.total.push(' ')
                    _this.loading = false
                  }else{
                    _this.total.push(response.data.message)
                    $('#in').val('') // 清空输入框
                    $('#text').scrollTop($('#text').scrollTop() + 32)// 滚动条拉到最下面，显示出输入框
                    _this.total.push(' ')
                    _this.loading = false
                  }
              }).catch(error =>{
                  $('#in').val('') // 清空输入框
                  _this.total.push('再次出错')
                  _this.total.push(error)
                  _this.total.push(' ')
                  _this.loading = false
              })
            }else if(response.data.err == '404'){
              $('#in').val('') // 清空输入框
              _this.total.push(response.data.message)
              _this.total.push(' ')
              _this.loading = false
            }else{
              $('#in').val('') // 清空输入框
              _this.total.push(response.data.message)
              _this.total.push(' ')
              _this.loading = false
            }
          }).catch(error =>{
            $('#in').val('') // 清空输入框
                  _this.total.push('第一次出错')
            _this.total.push(error)
            _this.total.push(' ')
            _this.loading = false
        })
      } else if (ip.indexOf('clear') >= 0) {
        this.total = ['Welcome！You can enter：ping 192.168.1.1',' ']
        $('#in').val('') // 清空输入框
        _this.loading = false
      } else {
        if (ip === '' || ip === null) {
          this.total.push('>' + ip)
          $('#in').val('') // 清空输入框
          _this.loading = false
        } else {
          this.total.push('>' + ip)
          var start = ip.split(' ')[0]
          this.total.push("’" + start + "’" + '  不是内部或外部命令，也不是可运行的程序或批处理文件。')
          $('#in').val('') // 清空输入框
          this.total.push(' ')
          this.loading = false
        }
      }
    },
    autoFocus () {
      console.log("aaa");
      
      $('#in').focus()
    },
    scoll () {
      var _this = this
      this.positionTimer = setTimeout(() => {
        var card = $('#card')
        // console.log(card)
        // console.log(card[0].scrollTop)
        // console.log(card[0].scrollHeight)
        card[0].scrollTop = (card[0].scrollHeight + 1000000)
        clearTimeout(_this.positionTimer)
        _this.positionTimer = null
      }, 100, function () {
      })
    }
  }
}
</script>
