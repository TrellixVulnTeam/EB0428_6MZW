<template>
  <el-main class="no-padding mount">
    <el-breadcrumb separator-class="el-icon-arrow-right">
    <el-select v-show="isagree" v-model="agreement" @change="changeAgree" size="mini" style="float:left;width:8%">
        <el-option value="FTP">FTP</el-option>
        <el-option value="HTTP">HTTP</el-option>
    </el-select>
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
      v-loading="loading" 
      :sort-method="sort">
        <el-table-column type="selection" width="80"></el-table-column>
        <el-table-column label="名称" min-width="30" :show-overflow-tooltip="true" prop="filename" sortable> 
            <template slot-scope="scope">
                <el-input class="add_input" placeholder="请输入文件夹名" v-show="scope.row.isShow" v-model="addFolder" @keyup.enter.native="addFold"></el-input>
                <span v-show="!scope.row.isShow" onselectstart="return false" class="dataName" @click="clickFile(scope.row)">{{scope.row.filename}}</span>
            </template>
        </el-table-column>
        <el-table-column label="大小" min-width="15" prop="size" align="center" sortable></el-table-column>
        <el-table-column label="修改日期" min-width="20" prop="change_time" align="center" sortable></el-table-column>
    </el-table>
  </el-main>
</template>

<script>
// import { log } from 'util'
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
        return{
            agreement:'HTTP',
            count:0,
            url:'',
            folderPath:'',
            folderName:'',
            addFolder:this.addFolderName,
            loading:false,
            isAdd:false,
            isagree:false,
            selIndex:[],
            dir:[],
            fileName:[],
            multipleSelection:[],
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
        // console.log(this.mount);
        // switch (this.mount) {
        //     case "all":
        //         // this.url = 'http://10.167.198.95:9090/yuancheng/rem_address/?agreement_type=ftp&ftp_host=10.167.198.95&ftp_name=python&ftp_password=123456&ftp_filename=/' //FTP
        //         this.url = "/apis/yuancheng/rem_address/?agreement_type=https&http_ip=http://10.167.198.95:8080/" //HTTP
        //         break;
        //     case "folder":
        //         this.url = "/apis/device/smtdataList/?file_data="
        //         break;
        //     default:
        //         break;
        // }
        // this.backHome()
    },
    mounted(){
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
        },
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
        addFolderName:String,
		isEnable:Boolean
    },
    methods:{
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
            this.loading = true
            this.$axios.get(this.url)
                .then(response =>{
                    this.timer()
                    $(".ceter_item").remove()
                    this.fileName = []
                    this.count = 0
                    this.dir = response.data.db
                    this.assignment()
                    this.loading = false
                })
                .catch(error =>{
                    console.log("connect fail！");
                    this.loading = false
                    this.sele()
                    if(this.isAdd == false){
                        this.backHome(this.url)
                    }
                })
        },
        //用于连接后台接口
        connData(now,address){
            // console.log("connData:"+address);
            this.loading = true
            this.$axios.get(this.url+address)
                .then(response =>{
                    this.timer()
                    for(var i = $(".ceter_item").length-1 ; i >= 0 ; i--){
                        if(i > now){
                            $(".ceter_item").eq(i).remove()
                            this.fileName.splice(i,1)
                        }
                    }
                    this.dir = response.data.db
                    this.assignment()
                    this.loading = false
                    this.count--
                })
                .catch(error =>{
                    console.log("connect fail！");
                    this.loading = false
                    this.sele()
                    // this.connData(now,address)
                })
        },
        //排序后刷新图标
        sort(){
            this.sele()
            this.chageCheck()
        },
        //更换url
        changeAgree(){
            if(this.agreement == "FTP"){
                this.url = '/apis/yuancheng/rem_address/?agreement_type=ftp&ftp_host=10.167.198.95&ftp_name=python&ftp_password=123456&ftp_filename=/' //FTP
            }else{
                this.url = "/apis/yuancheng/rem_address/?agreement_type=https&http_ip=http://10.167.198.95:8080/" //HTTP
            }
            this.backHome()
        },
        //更换多选框选中位置
        chageCheck(){
            // console.log(this.selIndex);
            for(var i = 0 ; i < this.dir.length ; i++){
                if(this.mount == "folder"){
                    // this.$refs.multipleTable.clearSelection()
                    // this.$refs.multipleTable.toggleRowSelection(this.multipleSelection,true)
                    // console.log('multipleSelection.index = '+this.multipleSelection.index);
                    if($(".el-table__row .el-checkbox .el-checkbox__original").eq(i).is(':checked')){
                        // console.log('true! i = ' + i);
                        this.selIndex[this.multipleSelection.index] = true
                        $(".el-table__row .el-checkbox").eq(this.multipleSelection.index).css("opacity","1")
                    }else{
                        // console.log('false! i = ' + i);
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
            // console.log(this.selIndex);
            
        },
        //更换图标
        sele(){
            // console.log($(".dataName").eq(0).text())
            $(".file").remove()
            $(".folder").remove()
            // console.log(this.dir);
            
                    
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
            // console.log('关闭定时器')
            // $('.el-table-column--selection').eq(1).append("<style>.el-table__body .el-table-column--selection::before{content:'\\E78A';}</style><span>aaa</span>");
        },
        //定时器
        timer () {
            // console.log('开启定时器')
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
                                if(_this.isEnable == false){
                                    _this.backHome()
                                }
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
                
            }else{
                $(".el-table__row .el-checkbox").css("opacity","0")
                isCheck = false
            }
            for(var i = 0 ; i < this.selIndex.length ; i++){
                if(isCheck == true){
                    this.selIndex[i] = true
                }else{
                    this.selIndex[i] = false
                }
            }
        },
        //用于判断鼠标是否移入表格行
        selHover(row, column, cell, event){
            // console.log(row.index);
            if(this.selIndex[row.index] == false){
                $(".el-table__row .el-checkbox").eq(row.index).css("opacity","1")
            }
            
        },
        //用于判断鼠标是否移出表格行
        selLeave(row, column, cell, event){
            if(this.selIndex[row.index] == false){
                $(".el-table__row .el-checkbox").eq(row.index).css("opacity","0")
            }
        },
        //用于判断某个多选框是否被选中
        selSelect(selection,row){
            // console.log(this.selIndex[row.index]);
            
            // console.log($(".el-table__row .el-checkbox .el-checkbox__original").eq(row.index).is(':checked'));
            if($(".el-table__row .el-checkbox .el-checkbox__original").eq(row.index).is(':checked')){
                this.selIndex[row.index] = true
                $(".el-table__row .el-checkbox").eq(row.index).css("opacity","1")
            }else{
                this.selIndex[row.index] = false
            }
        },
        //用于判断点击的是文件还是文件夹
        clickFile(row){
            // console.log(row.filetype);
            var _this = this
            if(row.filetype == "folder" && _this.isEnable == false){
                _this.loading = true
                var name = ""
                var blockName = row.filename
                _this.fileName.push(row.filename)
                for(var i = 0 ; i < _this.fileName.length ; i++){
                    if(name == ""){
                        name = _this.fileName[i] + '/'
                    }else{
                        name = name + _this.fileName[i] + "/"
                    }
                }
                // console.log(name);
                // console.log(_this.fileName);
                this.$axios.get(this.url+name)
                    .then(response =>{
                        this.dir = response.data.db
                        this.assignment()
                        $(".bottom_item").before("<span class='el-breadcrumb__item ceter_item'><span role='link' class='el-breadcrumb__inner'><span>" + blockName + "</span></span><i class='el-breadcrumb__separator el-icon-arrow-right'></i></span>")
                        var now = _this.count
                        // console.log(name);
                        // console.log(now);
                        $(".ceter_item").eq(now).on("click",function(){
                            // console.log(_this.isEnable);
                            
                            // console.log(now);
                            // console.log(name);
							if(_this.isEnable == false) _this.connData(now,name)
                        })
                        _this.count++
                        _this.loading = false
                    })
                    .catch(error =>{
                        console.log("connect fail！");
                        _this.loading = false
                        this.fileName.splice(this.fileName.length-1,1)
                        // console.log(_this.fileName);
                    })
                this.timer()
            }
        },
        //双击事件
        dbclickFile(row, column, cell, event){
            console.log(row.filetype);
            console.log(column.label);
            if(column.label == "名称" && row.isShow == false){
                this.clickFile(row)
            }
        },
        //行选中
        handleRowClick(row,column,event){
            if(this.mount == "folder" && row.isShow == false){
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
                // console.log($(".el-table__row .el-checkbox .el-checkbox__original").eq(row.index).is(':checked'));
                
                // console.log(this.folderPath);
            }
        },
        //更改多选框状态
        handleSelectionChange(val){
            if(this.mount == "folder"){
                if(val.length > 1){
                    // console.log('>1' + val);
                    
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
                    // console.log('<=1' + val);
                    if(this.multipleSelection != null){
                        // this.selSelect(null,this.multipleSelection)
                        //待测试
                        this.selIndex[this.multipleSelection.index] = true
                        $(".el-table__row .el-checkbox").eq(this.multipleSelection.index).css("opacity","1")
                    }else{
                        for(var i = 0 ; i < this.selIndex.length ; i++){
                            this.selIndex[i] = false
                        }
                    }
                }
            }
        },
        //回车创建文件夹
        addFold(){
            this.$emit('addFold',newVal)
        }
    }
}
</script>

<style>
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
        color: #0396ff;
    }
    .el-tabs--border-card .el-breadcrumb__item:hover span{
        color: #0396ff;
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
        /* padding-right:1.8em */
    }
    .dataName:hover{
        color: #0396ff;
    }
</style>
