<template>
    <div>
        <el-main class="no-padding mount">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-select v-if="isagree" v-model="agreement" @change="changeAgree" size="mini" style="float:left;width:7em;margin-right:10px">
                    <el-option value="FTP">FTP</el-option>
                    <el-option value="HTTP">HTTP</el-option>
                    <el-option value="EdgeBox">EdgeBox</el-option>
                </el-select>
                <el-button v-if="isagree" type="text" size="mini" style="float:left" @click="changeInfo()" plain>{{nowIp}}</el-button>
                <el-breadcrumb-item class="top_item"><i class="el-icon-s-home"></i></el-breadcrumb-item>
                <el-breadcrumb-item class="bottom_item"></el-breadcrumb-item>
            </el-breadcrumb>
            <el-table
            class="mount_table"
            ref="multipleTable"
            min-height="100%"
            highlight-current-row 
            @select-all="chage"
            @cell-mouse-enter="selHover"
            @cell-mouse-leave="selLeave"
            @select="selSelect"
            @selection-change="handleSelectionChange"
            @row-click="handleRowClick"
            @cell-dblclick="dbclickFile"
            :cell-class-name="tableCellClassName"
            :data="dir"
            :sort-method="sort">
                <el-table-column type="selection" width="80"></el-table-column>
                <el-table-column label="名称" min-width="30" :show-overflow-tooltip="true" prop="filename" :sortable="!isSelect"> 
                    <template slot="header">
                        <span style="line-height: 36px">名称</span>
                        <el-button v-if="isagree && isSelect" class="el-download" size="mini" @click="download('all')" icon="el-icon-download" :disabled="isDownload">下载</el-button>
                    </template>
                    <template slot-scope="scope">
                        <el-input class="add_input" placeholder="请输入文件夹名" v-if="scope.row.isShow" v-model="addFolder"></el-input>
                        <span v-if="!scope.row.isShow" onselectstart="return false" class="dataName" @click="clickFile(scope.row)">{{scope.row.filename}}</span>
                        <el-dropdown class="df" trigger="click">
                            <span class="df" @click="cilckDownload(scope.row)"></span>
                            <el-dropdown-menu class="down" slot="dropdown">
                                <el-dropdown-item>
                                    <el-button v-if="isagree" class="el-download" type="text" @click="clickFile(scope.row)">
                                        <i v-if="scope.row.filetype == 'folder'" class="el-icon-folder-opened"></i>
                                        <i v-else class="el-icon-download"></i>
                                        {{scope.row.filetype == "folder" ? "进入" : "下载"}}
                                    </el-button>
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                    </template>
                </el-table-column>
                <el-table-column label="大小" min-width="15" prop="size" align="center" sortable></el-table-column>
                <el-table-column label="修改日期" min-width="20" prop="change_time" align="center" sortable></el-table-column>
            </el-table>
        </el-main>
        <div v-if="http_edit" class='el-append-http'>
            <div class='el-http-input-div'></div>
            <div class='el-center-div'>
                <div class="el-select-http">
                    <span>请选择:</span>
                    <el-select @change="resetForm('acq_info')" v-model="agreement" size="mini" placeholder="请选择">
                        <el-option
                        v-for="(v,i) in http_type_list"
                        :key="i" 
                        :label="v"
                        :value="v">
                        </el-option>
                    </el-select>
                </div>
                <el-form v-loading="loading" @keyup.enter.native="submitForm('acq_info')" @submit.native.prevent :model="acq_info" :label-position="labelPosition" ref="acq_info" :rules="acq_rules">
                    <template v-if="agreement == 'HTTP'">
                        <el-form-item label="IP:" prop="http_ip">
                            <el-autocomplete type='text' size="small" v-model="acq_info.http_ip" :fetch-suggestions="querySearch" placeholder="*.*.*.*"></el-autocomplete>
                        </el-form-item>
                    </template>
                    <template v-else-if="agreement == 'FTP'">
                        <el-form-item label="IP:" prop="ftp_ip">
                            <el-input type='text' v-model="acq_info.ftp_ip" size="small" placeholder="*.*.*.*"></el-input>
                        </el-form-item>
                        <el-form-item label="User:" prop="ftp_user">
                            <el-input type='text' v-model="acq_info.ftp_user" size="small" placeholder="请输入用户名"></el-input>
                        </el-form-item>
                        <el-form-item label="PassWord:" prop="ftp_pass">
                            <el-input type='password' v-model="acq_info.ftp_pass" size="small" placeholder="请输入密码"></el-input>
                        </el-form-item>
                    </template>
                    <template v-else-if="agreement == 'EdgeBox'">
                        <!-- <el-form-item label="IP:" prop="http_ip">
                            <el-input type='text' v-model="acq_info.http_ip" size="small" placeholder="*.*.*.*"></el-input>
                        </el-form-item> -->
                    </template>
                </el-form>
                <div class='el-append-button'>
                    <el-button type='info' size="small" @click="http_edit = false">取消</el-button>
                    <el-button type='primary' size="small" @click="submitForm('acq_info')">确定</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss">
$blue: #0396ff;
    .mount .folder::before{
        font-family: element-icons!important;
        position: absolute;
        display: block;
        top: 25%;
        right: 25px;
        font-size: 25px;
    }
    .mount .file::before{
        font-family: element-icons!important;
        position: absolute;
        display: block;
        top: 25%;
        right: 25px;
        font-size: 25px;
    }
    .mount .tooltip_css::before{
        content: "\E794";
        font-family: element-icons!important;
        font-size:25px;
        float:right;
    }
    .mount .el-table-column--selection .cell {
        float: right;
    }
    .mount .el-table__header .el-table-column--selection .cell{
        text-align: center;
    }
    .mount .el-table__body .cell{
        height: 2em;
        line-height: 2em;
    }
    .mount  .el-table__body .el-tooltip{
        max-width: 85%;
    }
    .mount .el-table__body .el-checkbox{
        opacity: 0;
        top: 7px;
    }
    .mount .el-table__body .el-checkbox__inner{
        width: 12px;
        height: 12px;
    }
    .mount .el-tabs--border-card .el-tabs__content{
        padding: 0px;
    }
    .el-tabs--border-card .el-tabs__content .el-breadcrumb{
        cursor:pointer;
    }
    .el-tabs--border-card .el-tabs__content .el-breadcrumb .el-icon-arrow-right{
        font-size: 25px;
        margin-left: 6px;
        margin-right: 0px;
    }
    .el-tabs--border-card .el-tabs__content .el-breadcrumb .el-icon-s-home{
        position: relative;
        font-size:20px;
        bottom:3px;
    }
    .el-tabs--border-card .el-tabs__content .el-breadcrumb__inner span{
        position: relative;
        bottom: 4px;
    }
    .el-tabs--border-card .el-breadcrumb{
        padding-top: 15px;
    }
    .el-tabs--border-card .el-breadcrumb__item{
        padding-left: 15px;
    }
    .el-tabs--border-card .el-breadcrumb__item:hover i{
        color: $blue;
    }
    .el-tabs--border-card .el-breadcrumb__item:hover span{
        color: $blue;
    }
    .add_input input{
        width: 80%;
        height: 2em
    }
    .dataName{
        cursor: pointer;
        -webkit-user-select:none;
        -moz-user-select:none;
        -ms-user-select:none;
        user-select:none;
    }
    .dataName:hover{
        color: $blue;
    }
    .df{
        position: absolute;
        top: 0px;
        right: 0px;
        width: 24px;
        height: 100%;
        cursor: pointer;
    }
    .el-download{
        float: right;
    }
    .el-http-input-div{
        position: absolute;
        width: 100%;
        top: 0;
        left: 0;
        height: 100%;
        opacity: 0.2;
        z-index: 2;
        background: #050505;
    }
    .el-center-div{
        position: absolute;
        padding: 20px 0;
        top: 20px;
        width: 70%;
        left: 15%;
        z-index: 2;
        color: #5d5c5c;
        border-radius: 4px;
        text-align: center;
        background: #ffffff;
    }
    .el-center-div .el-input--small , .el-autocomplete{
        width: 67%;
    }
    .el-center-div .el-input--suffix{
        width: 8.1em
    }
    .el-input--suffix input{
        background: #fff93159;
    }
    .el-autocomplete .el-input--small{
        width: 100%;
    }
    .el-center-div .el-append-button{
        padding-top: 20px;
    }
    .el-center-div .el-form{
        width: 40%;
        text-align: right;
        margin: 0 auto;
    }
    .el-select-http{
        position: absolute;
        font-size: 13px;
        margin-left: 10px;
        margin-top: 10px;
        top: 0px;
    }
    .el-select-http span{
        margin-right: 10px;
        background-image: linear-gradient(to right, red, orange, yellow, green, blue, green, yellow, orange, red, orange, yellow, green, blue, green, yellow, orange, red);    
        -webkit-text-fill-color: transparent;
        -webkit-background-clip: text;
        -webkit-background-size: 200% 100%;
        animation: bgp 5s infinite linear;
    }
    @-webkit-keyframes bgp{
        0%{
            background-position: 0 0;
        }
        100%{
            background-position: -100% 0;
        }
    }
</style>

<script>
import { log } from 'util'
export default {
    filters: {
        ellipsis (value) {
        if (!value) return ''
        if (value.length > 8) {
            return value.slice(0,8) + '...'
        }
        return value
        }
    },
    data(){
        var validator_http_ip = (rule, value, callback) => {
            if(!value) return callback(new Error("IP不能为空"))
            if(!(/^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)(\:\d{1,5})?$/.test(value))) return callback(new Error("IP格式错误"))
            callback()
        };
        var validator_ftp_ip = (rule, value, callback) => {
            if(!value) return callback(new Error("IP不能为空"))
            if(!(/^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)(\:\d{1,5})?$/.test(value))) return callback(new Error("IP格式错误"))
            callback()
        };
        var validator_ftp_user = (rule, value, callback) => {
            if(!value) return callback(new Error("用户名不能为空"))
            callback()
        };
        var validator_ftp_pass = (rule, value, callback) => {
            if(!value) return callback(new Error("密码不能为空"))
            callback()
        };
        return{
            agreement:'HTTP',
            labelPosition: "right",
            count:0,
            url:'',
            nowIp: '',
            download_url: '',
            folderPath:'',
            folderName:'',
            click_download: [],
            inteface_value:{},
            inteface_download:{},
            initScroll: 0,
            initTop: 0,
            addFolder:this.addFolderName,
            loading:true,
            isAdd:false,
            isagree:false,
            isSelect: false,
            isDownload: false,
            http_edit: false,
            http_type_list:["FTP","HTTP","EdgeBox"],
            acq_info:{
                http_ip: "",
                ftp_ip: "",
                ftp_user: "",
                ftp_pass: ""
            },
            acq_rules: {
                http_ip: [{required: true, validator: validator_http_ip, tigger: "blur"}],
                ftp_ip: [{required: true, validator: validator_ftp_ip, tigger: "blur"}],
                ftp_user: [{required: true, validator: validator_ftp_user, tigger: "blur"}],
                ftp_pass: [{required: true, validator: validator_ftp_pass, tigger: "blur"}],
            },
            selIndex:[],
            dir:[],
            fileName:[],
            checkFile:[],
            multipleSelection:[],
            querySear:[],
            topicData:[{
                    type: 'Create',
                    topic: '/data/EdgeBox/gateway/create/....',
                    description: '创建'
                },
                {
                    type: 'Update',
                    topic: '/data/EdgeBox/gateway/update/....',
                    description: '更新'
                },
                {
                    type: 'Delete',
                    topic: '/data/EdgeBox/gateway/delete/....',
                    description: '删除'
                }
            ]
        }
    },
    created(){
        this.initMount()
    },
    mounted(){
        var _this = this
        setTimeout(() => {
            $(".ul").scroll(() => {
                for(let i = 0; i < $(".down").length; i++){
                    if($(".down").eq(i).css("display") == "block"){
                        $(".down").eq(i).css("top",_this.initScroll - ($(".ul").scrollTop() - _this.initTop))
                    }
                }
            })
        }, 200);
    },
    watch:{
        //监听子组件数据发生改变后向父组件传值
        addFolder:{
            handler:function(newVal,oldVal){
                this.$emit('addFolderProp',newVal)
            },
            deep:true,
            immediate: true
        },
        addFolderName:{
            handler:function(newVal,oldVal){
                this.addFolder = newVal
            },
            deep:true,
            immediate: true
        }
    },
    computed:{
    },
    destroyed () {
        clearInterval(this.positionTimer)// 清除定时器
        this.positionTimer = null
        console.log('关闭定时器')
        this.isAdd = true
    },
    props:{
        mount:String,
        addFolderName:String
    },
    methods:{
        initMount(){
            this.loading = true
            switch (this.mount) {
                case "all":
                    if(localStorage.getItem("http_acq")) this.acq_info.http_ip = JSON.parse(this.$secre.changeSecret(localStorage.getItem("http_acq")))["newHttp"]
                    if(localStorage.getItem("ftp_acq")){
                        this.acq_info.ftp_ip = JSON.parse(this.$secre.changeSecret(localStorage.getItem("ftp_acq")))["newFtp"]
                        this.acq_info.ftp_user = JSON.parse(this.$secre.changeSecret(localStorage.getItem("ftp_acq")))["newUser"]
                        this.acq_info.ftp_pass = JSON.parse(this.$secre.changeSecret(localStorage.getItem("ftp_acq")))["newPass"]
                    }
                    if(this.acq_info.http_ip == null || this.acq_info.http_ip == "" || this.acq_info.http_ip == undefined){
                        this.loading = false
                        this.changeInfo()
                        return false
                    }
                    this.url = "/apis/remotely/mount/" //HTTP
                    this.inteface_value = {
                        "agreement_type" : this.$secre.secretkey("https"),
                        "http_ip" : this.$secre.secretkey(this.acq_info.http_ip)
                    }
                    break;
                case "folder":
                    this.url = "/apis/remotely/interface/?file_dirs="
                    break;
                default:
                    break;
            }
            this.backHome()
        },
        //从后台接口赋值
        assignment(){
            for(var i = 0 ; i < this.dir.length ; i++){
                if(!this.dir[i].hasOwnProperty("isShow"))this.dir[i]["isShow"] = false
                if(this.dir[i]["filetype"] == "folder"){
                    if(this.mount == "all" && this.agreement == "HTTP"){
                        this.dir[i]["filename"] = this.dir[i]["filename"].substring(0,this.dir[i]["filename"].length-1)
                    }
                }
                $(".el-table__row .el-checkbox").eq(i).css("opacity","0")
                this.selIndex[i] = false
            }
        },
        //用于连接后台接口
        backHome(){
            var _this = this
            this.loading = true
            
            this.$axios.post(this.url,this.inteface_value)
            .then(response =>{
                if(_this.agreement == "HTTP"){
                    let his = []
                    let boo = false
                    if(localStorage.getItem("http_acq")){
                        his = (JSON.parse(this.$secre.changeSecret(localStorage.getItem("http_acq")))["history"])
                        his.forEach((v,i) => {
                            if(v.name == _this.acq_info.http_ip) boo = true
                        })
                        if(boo == false){
                            his.push({"name" : _this.acq_info.http_ip})
                        }
                        localStorage.setItem("http_acq", this.$secre.secretkey(JSON.stringify({
                            "newHttp" : _this.acq_info.http_ip,
                            "history" : his
                        })))
                    }else{
                        his.push({"name" : _this.acq_info.http_ip})
                        localStorage.setItem("http_acq", this.$secre.secretkey(JSON.stringify({
                            "newHttp" : _this.acq_info.http_ip,
                            "history" : [{
                                "name" : _this.acq_info.http_ip,
                            }]
                        })));
                    }
                    _this.nowIp = _this.acq_info.http_ip
                    _this.querySear = his
                }else if(_this.agreement == "FTP"){
                    let his = []
                    let boo = false
                    if(localStorage.getItem("ftp_acq")){
                        his = (JSON.parse(this.$secre.changeSecret(localStorage.getItem("ftp_acq")))["history"])
                        his.forEach((v,i) => {
                            if(v.name == _this.acq_info.ftp_ip) boo = true
                        })
                        if(boo == false){
                            his.push({
                                "name" : _this.acq_info.ftp_ip
                            })
                        }
                        localStorage.setItem("ftp_acq", this.$secre.secretkey(JSON.stringify({
                            "newFtp" : _this.acq_info.ftp_ip,
                            "newUser" : _this.acq_info.ftp_user,
                            "newPass" : _this.acq_info.ftp_pass,
                            "history" : his
                        })))
                    }else{
                        his.push({"name" : _this.acq_info.ftp_ip})
                        localStorage.setItem("ftp_acq", this.$secre.secretkey(JSON.stringify({
                            "newFtp" : _this.acq_info.ftp_ip,
                            "newUser" : _this.acq_info.ftp_user,
                            "newPass" : _this.acq_info.ftp_pass,
                            "history" : [{
                                "name" : _this.acq_info.ftp_ip
                            }]
                        })));
                    }
                    _this.nowIp = _this.acq_info.ftp_ip
                } else if(_this.agreement == "EdgeBox"){
                    _this.nowIp = "EdgeBox"
                }
                this.timer()
                $(".ceter_item").remove()
                this.count = 0
                this.dir = response.data.db
                this.assignment()
                this.loading = false
                this.http_edit = false
            }).catch(error =>{
                this.changeInfo()
                this.sele()
            })
        },
        //用于连接后台接口
        connData(now,address){
            this.loading = true
            var count2 = 0
            for(var i = $(".ceter_item").length-1 ; i >= 0 ; i--){
                if(i > now){
                    $(".ceter_item").eq(i).remove()
                    this.fileName.splice(i,1)
                    this.count--
                    count2++
                }
            }
            this.getPath()
            this.$axios.post(this.url,this.inteface_value)
                .then(response =>{
                    this.timer()
                    this.dir = response.data.db
                    this.assignment()
                    this.loading = false
                })
                .catch(error =>{
                    this.count = this.count + count2
                    console.log("connect fail！");
                    this.loading = false
                    this.sele()
                })
        },
        //排序后刷新图标
        sort(){
            this.sele()
            this.chageCheck()
        },
        //更换url
        changeAgree(){
            if(this.agreement === "FTP" || this.agreement === "HTTP") this.url = "/apis/remotely/mount/"
            if(this.agreement === "FTP"){
                if(localStorage.getItem("ftp_acq")){
                    this.acq_info.ftp_ip = JSON.parse(this.$secre.changeSecret(localStorage.getItem("ftp_acq")))["newFtp"]
                    this.acq_info.ftp_user = JSON.parse(this.$secre.changeSecret(localStorage.getItem("ftp_acq")))["newUser"]
                    this.acq_info.ftp_pass = JSON.parse(this.$secre.changeSecret(localStorage.getItem("ftp_acq")))["newPass"]
                }
                if((this.acq_info.ftp_ip == "" || this.acq_info.ftp_ip == null || this.acq_info.ftp_ip == undefined) ||
                    (this.acq_info.ftp_user == "" || this.acq_info.ftp_user == null || this.acq_info.ftp_user == undefined) ||
                    (this.acq_info.ftp_pass == "" || this.acq_info.ftp_pass == null || this.acq_info.ftp_pass == undefined)) return this.changeInfo()
                this.inteface_value = {
                    "agreement_type" : this.$secre.secretkey("ftp"),
                    "ftp_host" : this.$secre.secretkey(this.acq_info.ftp_ip),
                    "ftp_name" : this.$secre.secretkey(this.acq_info.ftp_user),
                    "ftp_password" : this.$secre.secretkey(this.acq_info.ftp_pass),
                    "ftp_filename" : this.$secre.secretkey("/")
                }
            }else if(this.agreement == "HTTP"){
                if(localStorage.getItem("http_acq")){
                    this.acq_info.ftp_ip = JSON.parse(this.$secre.changeSecret(localStorage.getItem("http_acq")))["newHttp"]
                }
                if(this.acq_info.http_ip == "" || this.acq_info.http_ip == null || this.acq_info.http_ip == undefined) return this.changeInfo()
                this.inteface_value = {
                    "agreement_type" : this.$secre.secretkey("https"),
                    "http_ip" : this.$secre.secretkey(this.acq_info.http_ip)
                }
            }else if(this.agreement == "EdgeBox"){
                this.url = "/apis/remotely/interface/" //EdgeBox
                this.inteface_value = {
                    "file_dirs" : this.$secre.secretkey("Download"),
                }
            }
            this.fileName = []
            this.checkFile = []
            this.download_url = ''
            this.backHome()
        },
        //更换多选框选中位置
        chageCheck(){
            for(var i = 0 ; i < this.dir.length ; i++){
                if(this.mount == "folder"){
                    if($(".el-table__row .el-checkbox .el-checkbox__original").eq(i).is(':checked')){
                        this.selIndex[this.multipleSelection.index] = true
                        $(".el-table__row .el-checkbox").eq(this.multipleSelection.index).css("opacity","1")
                    }else{
                        this.selIndex[i] = false
                        $(".el-table__row .el-checkbox").eq(i).css("opacity","0")
                    }
                }else{
                    if($(".el-table__row .el-checkbox .el-checkbox__original").eq(i).is(':checked')){
                        this.selIndex[i] = true
                        $(".el-table__row .el-checkbox").eq(i).css("opacity","1")
                    }else{
                        this.selIndex[i] = false
                        $(".el-table__row .el-checkbox").eq(i).css("opacity","0")
                    }
                }
            }
        },
        //更换图标
        sele(){
            $(".file").remove()
            $(".folder").remove()
                    
            for(var i = 0 ; i < this.dir.length ; i++){
                $(".el-tooltip").eq(i).parent().addClass('tooltip_css');
                for(var j = 0 ; j < this.dir.length ; j++){
                    if($(".dataName").eq(j).text() == this.dir[i]['filename']){
                        if(this.dir[i]['filetype'] == "file"){
                            $('.el-table__row .el-table-column--selection').eq(j).append("<a class='file'></a>")
                        }else if(this.dir[i]['filetype'] == "folder"){
                            $('.el-table__row .el-table-column--selection').eq(j).append("<a class='folder'></a>")
                        }
                    }else if(this.mount == "folder" && this.dir[i]['filename'] == ''){
                            $('.el-table__row .el-table-column--selection').eq(j).append("<a class='folder'></a>")
                    }
                }
            }
            $(".el-tooltip").eq(this.dir.length).parent().addClass('tooltip_css');
            $('.file').append("<style>.file::before{content:'\\E78B';}</style>");
            $('.folder').append("<style>.folder::before{content:'\\E78A';}</style>");
            clearInterval(this.positionTimer)// 清除定时器
            this.positionTimer = null
        },
        //定时器
        timer () {
            // 这是一个定时器
            var _this = this
            if(this.positionTimer == null){
                this.positionTimer = setInterval(() => {
                    if(this.loading == false){
                        this.sele()
                        if(this.isAdd == false){
                            if(this.mount == "folder"){
                                $(".el-table__header .el-checkbox").eq(0).hide()
                                $(".mount_table th").eq(1).on("click",function() {
                                    _this.sort()
                                })
                                this.isagree = false;
                            }else{
                                $(".mount_table th").eq(1).on("click",function() {
                                    _this.sort()
                                })
                                $(".mount_table th i").eq(1).on("click",function() {
                                    _this.sort()
                                })
                                this.isagree = true;
                            }
                            
                            $(".top_item").on("click",function(){
                                _this.fileName = []
                                _this.checkFile = []    
                                _this.getPath()
                                _this.backHome()
                            });
                            this.isAdd = true
                        }
                    }
                }, 100)
            }else{
                this.sele()
            }
        },
        //用于获取选中的表格行的索引
        tableCellClassName({row, column, rowIndex, columnIndex}){//注意这里是解构
            //利用单元格的 className 的回调方法，给行列索引赋值
            row.index=rowIndex;
            column.index=columnIndex;
        },
        //用于判断全选框是否选中
        chage(){
            var isCheck = false
            if($(".el-table__header .el-checkbox__original").is(':checked')){
                $(".el-table__row .el-checkbox").css("opacity","1")
                isCheck = true
                this.isSelect = true
            }else{
                $(".el-table__row .el-checkbox").css("opacity","0")
                isCheck = false
                this.isSelect = false
            }
            this.checkFile = []
            for(var i = 0 ; i < this.selIndex.length ; i++){
                if(isCheck == true){
                    this.checkFile.push({"name" : this.dir[i].filename})
                    this.selIndex[i] = true
                }else{
                    this.selIndex[i] = false
                }
            }
        },
        //用于判断鼠标是否移入表格行
        selHover(row, column, cell, event){
            if(this.selIndex[row.index] == false){
                $(".el-table__row .el-checkbox").eq(row.index).css("opacity","1")
            }
            $(".el-table__row .el-checkbox").eq(row.index).parents("td").css("color","#409EFF")
        },
        //用于判断鼠标是否移出表格行
        selLeave(row, column, cell, event){
            if(this.selIndex[row.index] == false){
                $(".el-table__row .el-checkbox").eq(row.index).css("opacity","0")
            }
            $(".el-table__row .el-checkbox").eq(row.index).parents("td").css("color","")
        },
        //用于判断某个多选框是否被选中
        selSelect(selection,row){
            var _this = this
            if($(".el-table__row .el-checkbox .el-checkbox__original").eq(row.index).is(':checked')){
                this.selIndex[row.index] = true
                this.isSelect = true
                $(".el-table__row .el-checkbox").eq(row.index).css("opacity","1")
                this.checkFile.push({"name" : row.filename})
            }else{
                this.checkFile.forEach((v,i) =>{
                    if(v.name == row.filename) _this.checkFile.splice(i, 1)
                })
                this.selIndex[row.index] = false
            }
        },
        //用于判断点击的是文件还是文件夹
        clickFile(row){
            var _this = this
            if(row.filetype == "folder"){
                _this.loading = true
                _this.fileName.push(row.filename)
                _this.checkFile = []
                _this.getPath()
                var blockName = row.filename
                this.$axios.post(this.url,this.inteface_value)
                    .then(response =>{
                        this.dir = response.data.db
                        this.assignment()
                        $(".bottom_item").before("<span class='el-breadcrumb__item ceter_item'><span role='link' class='el-breadcrumb__inner'><span>" + blockName + "</span></span><i class='el-breadcrumb__separator el-icon-arrow-right'></i></span>")
                        var now = _this.count
                        $(".ceter_item").eq(now).on("click",function(){
                            _this.connData(now)
                        })
                        _this.count++
                        _this.loading = false
                    })
                    .catch(error =>{
                        console.log("connect fail！");
                        _this.loading = false
                        this.fileName.splice(this.fileName.length-1,1)
                    })
                this.timer()
            }else{
                this.click_download.push({"name" : row.filename})
                this.download(row)
            }
        },
        //双击事件
        dbclickFile(row, column, cell, event){
            if(column.label == "名称"){
                this.clickFile(row)
            }
        },
        //行选中
        handleRowClick(row,column,event){
            if(this.mount == "folder"){
                this.folderName = row.filename
                this.folderPath = ""
                for(var i = 0 ; i < this.fileName.length ; i++){
                    if(this.folderPath == ""){
                        this.folderPath = this.fileName[i] + '/'
                    }else{
                        this.folderPath = this.folderPath + this.fileName[i] + "/"
                    }
                }
                this.$refs.multipleTable.toggleRowSelection(row)
            }
        },
        //更改多选框状态
        handleSelectionChange(val){
            if(this.mount == "folder"){
                if(val.length > 1){
                    this.$refs.multipleTable.clearSelection()
                    for(var i = 0 ; i < this.selIndex.length ; i++){
                        this.selIndex[i] = false
                        $(".el-table__row .el-checkbox").eq(i).css("opacity","0")
                    }
                    this.$refs.multipleTable.toggleRowSelection(val.pop(),true)
                    this.selIndex[val.pop()] = true
                    $(".el-table__row .el-checkbox").eq(val.pop()).css("opacity","1")
                }else{
                    this.multipleSelection = val.pop()
                    if(this.multipleSelection != null){
                        //待测试
                        this.selIndex[this.multipleSelection.index] = true
                        $(".el-table__row .el-checkbox").eq(this.multipleSelection.index).css("opacity","1")
                    }else{
                        for(var i = 0 ; i < this.selIndex.length ; i++){
                            this.selIndex[i] = false
                        }
                    }
                }
            }else{
                if(val.length == 0) this.isSelect = false
            }
        },
        getPath(){
            var name = ""
            if(this.fileName.length > 0){
                for(var i = 0 ; i < this.fileName.length ; i++){
                    if(name == ""){
                        name = "/" + this.fileName[i] + '/'
                    }else{
                        name = name + this.fileName[i] + "/"
                    }
                }
            }
            if(this.agreement == "HTTP"){
                this.inteface_value.http_ip = this.$secre.secretkey(this.acq_info.http_ip + name)
                this.inteface_download.http_ip = this.$secre.secretkey(this.acq_info.http_ip + name)
            } else if (this.agreement == "FTP"){
                this.inteface_value.ftp_filename = this.$secre.secretkey((name == "" ? "/" : name)) 
                this.inteface_download.ftp_filename = this.$secre.secretkey((name == "" ? "/" : name))
            }
        },
        download(row){
            var _this = this
            _this.isDownload = true
            if(_this.agreement === "HTTP" || _this.agreement === "FTP") _this.download_url = "/apis/remotely/mount/"
            if(_this.agreement === "HTTP"){
                _this.inteface_download = {
                    "agreement_type" : _this.$secre.secretkey("https"),
                    "http_ip" : _this.$secre.secretkey(_this.acq_info.http_ip),
                    "download" : _this.click_download.length > 0 ? _this.$secre.secretkey(JSON.stringify(_this.click_download)) : _this.$secre.secretkey(JSON.stringify(_this.checkFile))
                }
            }else if(_this.agreement === "FTP"){
                _this.inteface_download = {
                    "agreement_type" : _this.$secre.secretkey("ftp"),
                    "ftp_host" : _this.$secre.secretkey(_this.acq_info.ftp_ip),
                    "ftp_name" : _this.$secre.secretkey(_this.acq_info.ftp_user),
                    "ftp_password" : _this.$secre.secretkey(_this.acq_info.ftp_pass),
                    "ftp_filename" : _this.$secre.secretkey("/"),
                    "download" : _this.click_download.length > 0 ? _this.$secre.secretkey(JSON.stringify(_this.click_download)) : _this.$secre.secretkey(JSON.stringify(_this.checkFile))
                }
            }else if(_this.agreement === "EdgeBox"){

            }
            _this.getPath()
            this.$axios.post("/apis/remotely/mount/",_this.inteface_download)
            .then(res => {
                if(res.data.status_code == 0){
                    _this.$Message.SuccessMessage(_this, res.data.db)
                }else if(res.data.status_code == 1){
                    _this.$Message.ErrorMessage(_this, res.data.db)
                }else{
                    _this.$Message.ErrorMessage(_this, "未知错误")
                }
            }).catch(error => {
            })
            _this.click_download = []
            _this.isDownload = false
        },
        cilckDownload(row){
            var _this = this
            setTimeout(() => {
                for(let i = 0; i < $(".down").length; i++){
                    if($(".down").eq(i).css("display") == "block"){
                        _this.initScroll = $(".down").eq(i).position().top
                        _this.initTop = $(".ul").scrollTop()
                    }
                }
            }, 200);
        },
        submitForm(formName){
            var _this = this
            
            this.$refs[formName].validate((valid) => {
                if(valid){
                    if(_this.agreement == "HTTP" || _this.agreement == "FTP") _this.url = "/apis/remotely/mount/"
                    if(_this.agreement == "HTTP"){
                        _this.inteface_value = {
                            "agreement_type" : _this.$secre.secretkey("https"),
                            "http_ip" : _this.$secre.secretkey(_this.acq_info.http_ip)
                        }
                    }
                    if(_this.agreement == "FTP"){
                        if(/^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$/.test(this.acq_info.ftp_pass)) this.acq_info.ftp_pass = this.$secre.changeSecret(this.acq_info.ftp_pass)
                        _this.inteface_value = {
                            "agreement_type" : _this.$secre.secretkey("ftp"),
                            "ftp_host" : _this.$secre.secretkey(_this.acq_info.ftp_ip),
                            "ftp_name" : _this.$secre.secretkey(_this.acq_info.ftp_user),
                            "ftp_password" : _this.$secre.secretkey(_this.acq_info.ftp_pass),
                            "ftp_filename" : _this.$secre.secretkey("/")
                        }
                    }
                    if(_this.agreement == "EdgeBox"){
                        _this.url = "/apis/remotely/interface/"
                        _this.inteface_value = {
                            "file_dirs" : _this.$secre.secretkey("Download")
                        }
                    }
                    _this.backHome()
                } else {
                    return false
                }
            })
        },
        resetForm(form){
            this.$refs[form].clearValidate()
        },
        changeInfo(){
            if(localStorage.getItem("ftp_acq")){
                this.acq_info.ftp_pass = this.$secre.secretkey(JSON.parse(this.$secre.changeSecret(localStorage.getItem("ftp_acq")))["newPass"])
            }
            this.loading = false
            this.http_edit = true
        },
        querySearch(queryString, cb) {
            var restaurants = this.querySear;
            var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
            if(this.querySear.length <= 0 || results == undefined) return cb(results)
            let list = []
            for(let i = 0; i < results.length; i++){
                list.push({
                    "value" : results[i].name
                })
            }
            // 调用 callback 返回建议列表的数据
            cb(list);
        },
        createFilter(queryString) {
            return (restaurant) => {
                return (restaurant.name.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
            };
        },
    }
}
</script>
