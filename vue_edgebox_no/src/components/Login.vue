<template>
    <el-main id="loginMain">

        <div class="box">
            <ul>
                <!-- <li>上</li>
                <li>下</li>
                <li>左</li>
                <li>右</li>
                <li>前</li>
                <li>后</li> -->
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
            </ul>
        </div>
        <el-card id="login">
            <div slot="header"><h1>EdgeBox账号登陆</h1></div>
            <el-form  class="el-form-input" ref="form" :model="form" :rules="rules">
                <el-form-item  prop="uName">
                    <el-input v-model="form.uName" placeholder="用户名"></el-input>
                </el-form-item>
                <el-form-item prop="pWord">
                    <!-- <el-input v-model="form.pWord" placeholder="密码" show-password></el-input> -->
                    <el-input type="password" v-model="form.pWord" placeholder="密码"></el-input>
                </el-form-item>
                <el-form-item prop="inner">
                    <el-row :gutter="15">
                        <el-col :span="15">
                            <el-input v-model="form.inner" maxlength="4" placeholder="验证码"></el-input>
                        </el-col>
                        <el-col :span="8">
                            <!-- <div @click="updateSidentify">
                                <Sidentify ref="Sidentify"></Sidentify>
                            </div> -->
                            <img :src="image_url" @click="refresh_verify_code" alt="点击刷新" style="width: 80px; height: 40px; float: right; cursor:pointer" />
                        </el-col>
                    </el-row>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" style="background-color: #246dff!important;border-color: #246dff!important;" @click="submitForm('form')">登录</el-button>
                </el-form-item>
                <el-form-item>
                    <el-checkbox style="float:left" v-model="form.remeberPWord">保持登录</el-checkbox>
                    <div style="float:right;">
                        <span class="activation" @click="activate_user">激活</span>
                        <span style="font-size:16px;margin:0px 0.3125rem;color:#333">|</span>
                        <span class="forget" @click="forget()">忘记密码</span>
                    </div>
                </el-form-item>
            </el-form>
            <el-form class="el-form-login">
                <el-form-item>
                    <div class="el-login-square">
                        <el-avatar shape="square" :size='41' icon="el-icon-user-solid"></el-avatar>
                    </div>
                    <div class="el-login-user">
                        <div class="el-login-name">{{form.uName}}</div>
                    </div>
                    <div class="el-login-switch"><div class="el-login-change">切换用户</div></div>
                    <!-- <div style="position:relative">
                        <div style="position:absolute;width:40%">
                            <el-avatar shape="square" :size='40' icon="el-icon-user-solid"></el-avatar>
                        </div>
                        <div style="position:absolute;width:73%">
                            <span style="font-size:1.5rem;">{{form.uName}}</span>
                        </div>
                    </div> -->
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" style="background-color: #246dff!important;border-color: #246dff!important;" @click="noPassLogin()">登录</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </el-main>
</template>

<script>
// import Layout from '../views/Layout.vue'
// import { checkNull } from '../until/checkRules'
import Sidentify from './components/Sidentify'
export default {
  data () {
    var validateName = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('用户名不能为空'))
      } else {
        callback()
      }
    }
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('密码不能为空'))
      } else {
        callback()
      }
    }
    var validateInner = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('验证码不能为空'))
      } else if (value.length != 4) {
        callback(new Error('验证码必须为四位'))
      } else {
        callback()
      }
    }
    return {
      SDTF: '',
      isLogin: false,
      image_url: '',
      routePath: 'gatewaySysInfo',
      form: {
        uName: '',
        pWord: '',
        inner: '',
        remeberPWord: false
      },
      rules: { // 表单验证
        uName: [
          // { required: true, message: '用户名不能为空', trigger: 'blur' },
          { required: true, validator: validateName, trigger: 'blur' }
          // { min: 3, max: 15, message: '长度在 3 到 15 个字符之间', trigger: 'blur' },
        ],
        pWord: [
          // { required: true, message: '密码不能为空', trigger: 'blur' },
          { required: true, validator: validatePass, trigger: 'blur' }
          // { min: 3, max: 15, message: '长度在 3 到 15 个字符之间', trigger: 'blur' },
        ],
        inner: [
          // { required: true, message: '验证码不能为空', trigger: 'blur' },
          { required: true, validator: validateInner, trigger: 'blur' }
          // { min: 3, max: 15, message: '长度在 3 到 15 个字符之间', trigger: 'blur' },
        ]
      }
    }
  },
  created () {
    console.log(this.$route.params.device)
    if (!localStorage.getItem('ReLogin')) {
      if (localStorage.getItem('tokenLogin')) {
        localStorage.removeItem('tokenLogin')
      }
    }
    document.onkeydown = e => {
      let _key = window.event.keyCode
      if (_key === 13) {
        if ($('.el-form-input').css('display') == 'block' && $('.el-form-login').css('display') == 'none') {
          this.submitForm('form')
        } else if ($('.el-form-input').css('display') == 'none' && $('.el-form-login').css('display') == 'block') {
          this.noPassLogin()
        } else {
          // console.log("你按了回车");
          // console.log($(".el-form-input").css("display"));
          // console.log($(".el-form-login").css("display"));
        }
      }
    }
    var _this = this
    $(document).off().click(function (e) {})
    $(document).click(function (e) {
      var idValue = $(e.target).attr('class') // 获取当前点击区域对象的id值

      if (idValue == 'el-login-switch') {

      } else if (idValue == 'el-login-name') {
        // console.log($('.el-login-switch').css('display'));

        if ($('.el-login-switch').css('display') == 'block') {
          $('.el-login-switch').css('display', 'none')
        } else {
          $('.el-login-switch').css('display', 'block')
        }
      } else if (idValue == 'el-login-change') {
        $('.el-login-switch').css('display', 'none')
        $('.el-form-input').css('display', 'block')
        $('.el-form-login').css('display', 'none')
        // this.$axios.get('/user/verify_code')
        // .then(response=>{
        //     // this.image_url = 'data:image/png;base64,' + response.data.error_msg['png']
        //     console.log(this.image_url);
        // });
        _this.$axios.get('apis/user/login/change')
          .then(response => {
            if (response.data.error_code === 0) {
              localStorage.removeItem('tokenLogin')
              _this.form.uName = response.data.error_msg['username']
              _this.refresh_verify_code()
            } else if (response.data.error_code === 1) {
              _this.$Message.ErrorMessage(_this, response.data.error_msg)
            } else {
              _this.$Message.ErrorAlert(_this, '未知错误')
            }
          })
      } else { // 不在该dateLabel点击区域内
        $('.el-login-switch').css('display', 'none')
      }
    })
    // this.isLogin = true
    // this.$router.push({path:"/"})
    this.$axios.get('apis/user/login')
      .then(response => {
        // console.log(response.data.error_msg);
        this.form.uName = response.data.error_msg['username']
        if (this.form.uName === '' || response.data.error_msg['is_login'] == false) {
          $('.el-form-input').css('display', 'block')
          $('.el-form-login').css('display', 'none')
          this.refresh_verify_code()
          // if(localStorage.getItem("token")){
          //     $(".el-form-input").css("display","none")
          //     $(".el-form-login").css("display","block")
          //     this.form.uName = localStorage.getItem('token')
          // }else{
          //     // this.$axios.get('user/verifyApi')
          //     this.refresh_verify_code()
          //     // this.$axios.get('/user/verify_code')
          //     // .then(response=>{
          //     //     // let blob = new Blob([response.data.error_msg['png']]);
          //     //     // let url = window.URL.createObjectURL(blob);
          //     //     // console.log(url);

          //     //     // this.image_url = url;
          //     // //     this.image_url = btoa(
          //     // //     new Uint8Array(response.data.error_msg['png'])
          //     // //       .reduce((data, byte) => data + String.fromCharCode(byte), '')
          //     // //   )
          //     //     this.image_url = 'data:image/png;base64,' + response.data.error_msg['png']
          //     //     console.log(this.image_url);

          //     //     // this.image_url = "http://127.0.0.1:8000" + response.data.url
          //     //     // this.image_url = "http://10.167.213.226:8000" + response.data.url
          //     // });
          // }
        } else if (this.form.uName != '' && response.data.error_msg['is_login'] == true) {
          $('.el-form-input').css('display', 'none')
          $('.el-form-login').css('display', 'block')
        } else {

        }
      })
  },
  mounted () {
    $('.el-login-switch').css('display', 'none')
    var box = document.querySelector('.box ul')
    // 鼠标按下事件
    document.onmousedown = function (event) {
      // 鼠标按下时初始位置
      var reg = /\-?[0-9]+\.?[0-9]*/g
      var trans = box.style.transform || '0,0'
      var arr = trans.match(reg)
      var transX = Number(arr[0])
      var transY = Number(arr[1])
      // 鼠标开始点下位置
      var startX = event.clientX - transX
      var startY = event.clientY + transY
      // 鼠标拖拽事件
      document.onmousemove = function (event) {
        // 鼠标移动后位置
        var x = event.clientX - startX
        var y = event.clientY - startY
        box.style.transform = 'rotateY(' + x + 'deg) rotateX(' + -y + 'deg)'
      }
      // 鼠标抬起事件
      document.onmouseup = function () {
        document.onmousemove = null
        document.onmouseup = null
      }
    }
  },
  methods: {
    submitForm (form) {
      // console.log(localStorage.getItem("ReLogin"));
      if (localStorage.getItem('ReLogin')) {
        this.routePath = this.$secre.changeSecret(localStorage.getItem('ReLogin'))
        if (localStorage.getItem('ReLogin') == '') {
          this.routePath = 'controlCenter'
        }
        localStorage.removeItem('ReLogin')
      }
      // console.log(this.routePath);
      var _this = this
      this.$refs[form].validate((valid) => {
        if (valid) {
          _this.$axios.post('apis/user/login', {
            'username': _this.form.uName,
            'password': _this.form.pWord,
            'verify_code': _this.form.inner,
            'keep_alive': _this.form.remeberPWord
          })
            .then(response => {
              if (response.data.error_code == 0) {
                var nowDate = new Date().getTime()
                _this.$cookie.setCookie('login', JSON.stringify({
                  'name': _this.form.uName,
                  'date': nowDate,
                  'isLogin': _this.form.remeberPWord,
                  'isUser': response.data.error_msg.is_superuser
                }), 10000)

                console.log(_this.$cookie.getCookie('login'))
                // console.log(unescape(_this.$cookie.getCookie("login")));

                _this.$cookie.delCookie('login')

                localStorage.setItem('tokenLogin', this.$secre.secretkey(JSON.stringify({
                  'name': _this.form.uName,
                  'date': nowDate,
                  'isLogin': _this.form.remeberPWord,
                  'isUser': response.data.error_msg.is_superuser
                })))

                // localStorage.removeItem('token')

                _this.$router.push(_this.routePath)
                setTimeout(function () {
                  console.log(window.location.href)
                  // window.location.href=window.location.href;
                }, 300)

                // window.location.href=window.location.href;
                // window.location.reload()
              } else if (response.data.error_code === 1) {
                _this.refresh_verify_code()
                _this.$Message.ErrorMessage(_this, response.data.error_msg)
              } else {
                _this.$Message.ErrorAlert(_this, '未知错误')
              }
            })
        } else {
          // console.log('error submit!!');
          return false
        }
      })
    },
    refresh_verify_code () {
      this.image_url = 'apis/user/verify_code/0.' + Math.floor(Math.random() * 1000000000)
      // this.$axios.get('user/verifyApi')
      // this.$axios.get('/user/verify_code')
      //     .then(response=>{
      //     // this.image_url = "http://127.0.0.1:8000" + response.data.url
      //     // this.image_url = "http://10.167.213.226:8000" + response.data.url
      //     this.image_url = 'data:image/png;base64,' + response.data.error_msg['png']
      // });
    },
    forget () {
      this.$router.push({
        name: 'Retrieve'
      })
    },
    updateSidentify () {
      this.$refs['Sidentify'].drawPic()
      this.SDTF = this.$refs['Sidentify'].identifyCode
    },
    activate_user () {
      var _this = this
      this.$axios.get('apis/user/send_activate_email/' + this.form.uName).then(
        response => {
          if (response.data.error_code == 0) {
            this.$Message.SuccessMessage(_this, response.data.error_msg)
          } else if (response.data.error_code == 1) {
            this.$Message.ErrorMessage(_this, response.data.error_msg)
          } else {
            this.$Message.ErrorMessage(_this, '未知错误')
          }
        }
      )
    },
    noPassLogin () {
      if (localStorage.getItem('ReLogin') != null) {
        console.log(localStorage.getItem('ReLogin'))
        this.routePath = this.$secre.changeSecret(localStorage.getItem('ReLogin'))
        if (localStorage.getItem('ReLogin') == '') {
          this.routePath = 'deviceList'
        }
        localStorage.removeItem('ReLogin')
      }
      var _this = this
      this.$axios.post('apis/user/login', {
        'username': _this.form.uName
        // "keep_login" : true
      }).then(response => {
        if (response.data.error_code == 0) {
          if (response.data.error_msg['is_login'] == true) {
            _this.$Message.SuccessMessage(_this, response.data.error_msg['msg'])
            var nowDate = new Date().getTime()
            localStorage.setItem('tokenLogin', this.$secre.secretkey(JSON.stringify({
              'name': _this.form.uName,
              'date': nowDate,
              'isLogin': false,
              'isUser': response.data.error_msg.is_superuser
            })))
            _this.$router.push({
              name: _this.routePath
            })
            // window.location.reload()
          } else {
            _this.$Message.ErrorMessage(_this, response.data.error_msg)
            $('.el-form-input').css('display', 'block')
            $('.el-form-login').css('display', 'none')
          }
        } else if (response.data.error_code == 1) {
          _this.$Message.ErrorMessage(_this, response.data.error_msg)
        } else {
          _this.$Message.ErrorMessage(_this, '未知错误')
        }
      })
    }
  },
  components: {
    // Layout
    Sidentify
  }
  // props:{
  //     isLogin:Boolean
  // },
}
</script>

<style>
#app{
    min-width: 1200px;
}
#loginMain .el-card{
    position: relative;
    width: 422px;
    text-align:center;
    margin: 0 auto;
    margin-top: 5%;
    padding-bottom: 20px;
    padding-top: 30px;
    border: 1px solid #979797;
}
#loginMain .el-card__header{
    border: 0px;
}
#loginMain .el-card__header h1{
    /* font-size:30px; */
    font-size:1.5rem;
    color: #333;
}
#loginMain .el-card__body{
    padding:0px;
}
#loginMain .el-form-item{
    margin: 22px 50px;
}
#loginMain .el-button--primary{
    width: 100%;
}
#loginMain .activation:hover,.forget:hover{
    color: #246dff;
    cursor: pointer;
}
#loginMain .el-form-login{
    display: none;
}
#loginMain .el-form-input{
    display: block;
}
#loginMain .el-login-square{
    position:relative;
    width:14%;
    height:40px;
    float:left;
    margin-left: 13%;
}
#loginMain .el-login-user{
    position:relative;
    width:60%;
    float:left;
    font-size:1.5rem;
    cursor: pointer;
}
#loginMain .el-login-user:hover{
    background: #e1e1e1;
}
#loginMain .el-login-switch{
    position: absolute;
    width: 59.5%;
    margin-left: 27%;
    top: 100%;
    z-index: 1000;
    color: #246dff;
    cursor: pointer;
    border: 1px solid #d4d4d4;
    background: white;
}
#loginMain .el-login-switch:hover{
    background: #e1e1e1;
}

    * {margin: 0; padding: 0;}
    .box {width: 100%; height: 600px; margin: 0 auto;  position: absolute; perspective: 800px;}
    .box ul {list-style: none; width: 400px; height: 400px; transition: all 20s;animation:myfirst 20s;
                animation-iteration-count:infinite;position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: auto; transform-style: preserve-3d;}
    .box ul li {width: 400px; height: 400px;  text-align: center; line-height: 100px;
                position: absolute; font-size: 36px;}
    /* .box ul li:nth-child(1) {background: rgba(255, 0, 255, 0.5); transform: translateY(-200px) rotateX(90deg);}
    .box ul li:nth-child(2) {background: rgba(192, 157, 81, 0.5); transform: translateY(200px) rotateX(-90deg);}
    .box ul li:nth-child(3) {background: rgba(35, 130, 142, 0.5); transform: translateX(-200px) rotateY(-90deg);}
    .box ul li:nth-child(4) {background: rgba(41, 150, 126, 0.5); transform: translateX(200px) rotateY(90deg);}
    .box ul li:nth-child(5) {background: rgba(121, 17, 240, 0.5); transform: translateZ(200px);}
    .box ul li:nth-child(6) {background: rgba(47, 142, 35, 0.5); transform: translateZ(-200px) rotateY(180deg);} */
    .box ul li:nth-child(1) {background: radial-gradient(rgb(219, 52, 144), rgb(20, 197, 124), rgb(204, 25, 25)); transform: translateY(-200px) rotateX(90deg);}
    .box ul li:nth-child(2) {background: radial-gradient(rgb(34, 245, 44), rgb(248, 248, 73), rgb(93, 173, 238)); transform: translateY(200px) rotateX(-90deg);}
    .box ul li:nth-child(3) {background: linear-gradient(to right,rgb(20, 144, 202), rgb(172, 130, 130), rgb(81, 75, 163)); transform: translateX(-200px) rotateY(-90deg);}
    .box ul li:nth-child(4) {background: repeating-linear-gradient(45deg, rgb(219, 216, 9), rgb(184, 26, 26), rgba(63, 139, 63, 0.315)); transform: translateX(200px) rotateY(90deg);}
    .box ul li:nth-child(5) {background: repeating-linear-gradient(rgb(12, 28, 250), rgb(135, 218, 179), rgb(168, 19, 93)); transform: translateZ(200px);}
    .box ul li:nth-child(6) {background: radial-gradient(rgb(124, 16, 226), rgb(22, 197, 168), rgb(218, 146, 14)); transform: translateZ(-200px) rotateY(180deg);}

    .box ul:hover {transform:rotateX(360deg) rotateY(360deg);}

    @keyframes myfirst
    {
    /* from {transform:rotateX(360deg) rotateY(360deg);}
    to {transform:rotateX(0deg) rotateY(0deg);} */
    0% {transform:rotateX(0deg) rotateY(0deg);}
    50% {transform:rotateX(360deg) rotateY(360deg);}
    100% {transform:rotateX(0deg) rotateY(0deg);}
    }
</style>
