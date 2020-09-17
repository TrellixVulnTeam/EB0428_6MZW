<template>
    <div id="retrieve">
        <el-row>
            <el-col :span="18" :offset="3">
                <el-steps style="margin-top: 4rem" :active="steps" finish-status="success" align-center>
                    <el-step title="确认身份"></el-step>
                    <el-step title="修改密码"></el-step>
                    <el-step title="完成"></el-step>
                </el-steps>
            </el-col>
            <el-col :span="8" :offset="8">
                <el-form class="el-form-confirm" ref="retrieveForm" :model="retrieveForm" :rules="rules">
                    <el-form-item label="用户名" label-width="120px" prop="userName">
                        <el-input v-model="retrieveForm.userName" placeholder="请输入忘记密码的用户名"></el-input>
                    </el-form-item>
                    <el-form-item label="身份证后六位" label-width="120px" prop="IDCard">
                        <el-input v-model="retrieveForm.IDCard" placeholder="请输入身份证后六位" maxlength="6"></el-input>
                    </el-form-item>
                    <el-form-item label="手机号" label-width="120px" prop="telephone">
                        <el-input v-model="retrieveForm.telephone" placeholder="请输入手机号" maxlength="11"></el-input>
                    </el-form-item>
                    <el-form-item label="邮箱" label-width="120px" prop="mail">
                        <el-input v-model="retrieveForm.mail" placeholder="请输入邮箱"></el-input>
                    </el-form-item>
                    <el-form-item style="text-align:center">
                        <el-button class="back-btn btn-min-width" type="primary" @click="cancel()">取消</el-button>
                        <el-button class="btn-min-width" type="primary" style="background-color: #246dff!important;border-color: #246dff!important;" @click="submitForm('retrieveForm')">下一步</el-button>
                    </el-form-item>
                </el-form>
                <el-form class="el-form-update" ref="updateForm" :model="updateForm" :rules="updateRules">
                    <el-form-item>
                        <span style="font-size:18px">用户名：{{retrieveForm.userName}}</span>
                    </el-form-item>
                    <el-form-item label="新密码" label-width="120px" prop="passWord">
                        <el-input v-model="updateForm.passWord" placeholder="请输入新密码" maxlength="6" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="确认新密码" label-width="120px" prop="confirmPassWord">
                        <el-input v-model="updateForm.confirmPassWord" placeholder="请再次输入新密码" maxlength="6" show-password></el-input>
                    </el-form-item>
                    <el-form-item style="text-align:center">
                        <el-button class="btn-min-width" type="primary" @click="cancel()">上一步</el-button>
                        <el-button class="btn-min-width" type="primary" style="background-color: #246dff!important;border-color: #246dff!important;" @click="submitForm('updateForm')">下一步</el-button>
                    </el-form-item>
                </el-form>
                <div class="updateSuccess" style="margin: 3rem auto;">
                    <el-button type="success" @click="cancel()" round>密码修改成功！返回登录页</el-button>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    data(){
        var validateName = (rule, value, callback) => {
            if(value === ''){
                callback(new Error("用户名不能为空"));
            }else{
                callback();
            }
        };
        var validateTelephone = (rule, value, callback) => {
            if(value === ''){
                callback(new Error("手机号不能为空"));
            }else if(!(/^1[3456789]\d{9}$/.test(value))){
                callback(new Error("手机号格式不正确"));
            }else{
                callback();
            }
        };
        var validateMail = (rule, value, callback) => {
            if(value === ''){
                callback(new Error("邮箱不能为空"));
            }
            // else if(!(/^([a-zA-Z]|[0-9])(\w|\-|\.)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/.test(value))){
            else if(!(/^([a-zA-Z]|[0-9])(\w|\-|\.)+@(\S)+\.([a-zA-Z]{2,4})$/.test(value))){
                callback(new Error("邮箱格式不正确"));
            }
            else{
                callback();
            }
        };
        var validateIDCard = (rule, value, callback) => {
            if(value === ''){
                callback(new Error("身份证后六位不能为空"));
            }else if(!(/[0-9]+[0-9a-zA-Z]$/.test(value))){
                callback(new Error("身份证号码格式不正确"));
            }else if(value.length < 6){
                callback(new Error("请输入身份证后六位"));
            }else{
                callback();
            }
        };
        var validatePassWord = (rule, value, callback) => {
            if(value === ''){
                callback(new Error("请输入密码"));
            }else{
                callback()
            }
        };
        var validateConfirmPassWord = (rule, value, callback) => {
            if(value === ''){
                callback(new Error("请再次输入密码"))
            }else if(value != this.updateForm.passWord){
                callback(new Error("两次密码不一致"))
            }else{
                callback()
            }
        };
        return{
            steps:0,
            retrieveForm:{
                userName: "jackie",
                telephone: "18565700228",
                mail: "jackie.h.zhou@mail.foxconn.com",
                IDCard: "123456"
            },
            updateForm:{
                passWord:'',
                confirmPassWord:''
            },
            rules:{
                userName:[
                    {required: true, validator: validateName, trigger: 'blur' }
                    // {required: true, message: "用户名不能为空", trigger: 'blur' }
                ],
                telephone:[
                    {required: true, validator: validateTelephone, trigger: 'blur' }
                    // {required: true, message: "手机号不能为空", trigger: 'blur' }
                ],
                mail:[
                    {required: true, validator: validateMail, trigger: 'blur' }
                    // {required: true, message: "邮箱不能为空", trigger: 'blur' }
                ],
                IDCard:[
                    {required: true, validator: validateIDCard, trigger: 'blur' }
                    // {required: true, message: "身份证后六位不能为空", trigger: 'blur' }
                ],
            },
            updateRules:{
                passWord:[
                    {required: true, validator: validatePassWord, tigger: "blur"}
                ],
                confirmPassWord:[
                    {required: true, validator: validateConfirmPassWord, tigger: "blur"}
                ]
            }
        }
    },
    components:{
    },
    methods:{
        submitForm(form){
            var _this = this
            this.$refs[form].validate((valid) =>{   
                if(valid){
                    if(form == "retrieveForm"){
                        this.$axios.post("/user/forget_password",{
                            "username": _this.retrieveForm.userName,
                            "user_id_six": _this.retrieveForm.IDCard,
                            "phone_number": _this.retrieveForm.telephone,
                            "email": _this.retrieveForm.mail
                        }).then(response => {
                            if(response.data.error_code == 0){
                                _this.steps++
                                $(".el-form").css("display","none")
                                if(_this.steps == 0){
                                    $(".el-form-confirm").eq(0).css("display","block")
                                }else if(_this.steps == 1){
                                    $(".el-form-update").eq(0).css("display","block")
                                }else if(_this.steps == 2){
                                    $(".updateSuccess").eq(0).css("display","block")
                                }
                            }else if(response.data.error_code == 1){
                                _this.$Message.WarningMessage(this, response.data.error_msg)
                                return false
                            }else{
                                _this.$Message.WarningMessage(this, "未知错误")
                                return false
                            }
                        })
                    }else if(form == "updateForm"){
                        this.$axios.post("/user/mend_password", {
                            "username": _this.retrieveForm.userName,
                            "new_password": _this.updateForm.confirmPassWord
                        }).then(response =>{
                            if(response.data.error_code == 0){
                                _this.$Message.WarningMessage(this, "密码修改成功")
                                _this.steps++
                                $(".el-form").css("display","none")
                                if(_this.steps == 0){
                                    $(".el-form-confirm").eq(0).css("display","block")
                                }else if(_this.steps == 1){
                                    $(".el-form-update").eq(0).css("display","block")
                                }else if(_this.steps == 2){
                                    $(".updateSuccess").eq(0).css("display","block")
                                }
                            }else if(response.data.error_code == 0){
                                _this.$Message.WarningMessage(this, response.data.error_msg)
                                return false
                            }else{
                                _this.$Message.WarningMessage(this, "未知错误")
                                return false
                            }
                        })
                    }
                }else{
                    return false;
                }
            })
        },
        cancel(){
            if(this.steps <= 0){
                this.$router.go(-1)
            }else if(this.steps == 2){
                this.$router.push({
                    name: "Login"
                })
            }else{
                this.steps--
                $(".el-form").css("display","none")
                if(this.steps == 0){
                    $(".el-form-confirm").eq(0).css("display","block")
                }else if(this.steps == 1){
                    $(".el-form-update").eq(0).css("display","block")
                }else{

                }
            }
        }
    }
}
</script>

<style>
#retrieve .el-form-item__label{
    text-align: left;
}
#retrieve .back-btn{
    background-color: #999!important;
    border-color: #999!important;
}
#retrieve .btn-min-width{
    min-width: 96px;
}
#retrieve .el-form{
    margin: 3rem auto;
}
#retrieve .el-form-confirm{
    display: block;
}
#retrieve .el-form-update{
    display: none;
}
#retrieve .updateSuccess{
    display: none;
    text-align: center;
}
</style>