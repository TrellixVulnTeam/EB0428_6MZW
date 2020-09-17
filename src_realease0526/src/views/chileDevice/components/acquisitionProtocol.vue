<template>
  <el-main class="no-padding">

    <el-row>
      <el-form :inline="true" v-loading="loading"  :model="form1" ref="form1">
        <el-form-item
          prop="typeSelected"
          :rules="[
              {  required: true, message: '请先选择设备协议名称!',trigger: 'blur',},
          ]"
        >
            <el-cascader
            :options="protocolList"
            :clearable="true"
            :show-all-levels="false"
            v-model="form1.typeSelected"
            size="small" placeholder="按协议名称查找模板"
            @change="catchange"></el-cascader>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" size="small" @click="submitFormCreate('form1')"  >新增协议模板</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-table :data="tableData" ref="refTable" @row-click="clickTable">

        <el-table-column label="模板名称" prop="name"></el-table-column>
        <el-table-column label="协议名称" prop="protocol">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.protocol === 'Modbus-RTU'" size="medium">{{ scope.row.protocol }}</el-tag>
            <el-tag v-else-if="scope.row.protocol === 'Modbus-TCP'" size="medium" type="success">{{ scope.row.protocol }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="createTime"></el-table-column>
        <el-table-column label="描述" prop="description"></el-table-column>
        <el-table-column label="操作" width="80">
            <template v-slot="scope">
                <el-button type="text" size="small" @click="templateApply(scope.row)">
                  <span v-if="form1.typeSelected === '' && tableData.length === 1">重新应用</span>
                  <span v-else-if="form1.typeSelected !==''">应用</span>
                </el-button>
            </template>
        </el-table-column>
        <el-table-column type="expand"  >
            <template  v-slot="scope">
               <el-row  v-for="(key , i) in scope.row.info " :key ="Number(i)">
                  <el-col v-for="(val , j) in key " :key ="Number(j)" :span="6" >
                    <json-viewer
                      :value="val"
                      :expand-depth="1"
                      copyable
                      boxed
                      sort
                    ></json-viewer>
                  </el-col>
                  <br>
               </el-row>
            </template>
        </el-table-column>
    </el-table>

    <!-- 新增设备模板 TCP RTU 配置 -->
    <div class="dialogfrommodel">
      <el-dialog   :title="'新增设备模板('+form1.typeSelected[1]+')'" :visible.sync="dialogFormCreate"  width= "800px">
        <el-form  label-position="top"  :model="dynamicValidateForm"  ref="dynamicValidateForm" inline-message= true	>
          <el-table :data="dynamicValidateForm.domains" class="table" style="width: 100%">
            <el-table-column label="功能码" prop="function_code" min-width="10%">
                <template slot-scope="scope">
                    <el-form-item   :prop="'domains.' + scope.$index + '.function_code'"
                    :rules="[
                          { required: true, message: '必填!', trigger: ['blur','change'] },
                    ]">
                      <el-select size="small" v-model="scope.row.function_code" placeholder="03">
                        <el-option v-for="item in appforms.function_code" :key="item.index" :label="item.value" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="起始寄存器" prop="start_register" min-width="12%">
              <!-- <el-input size="small" ></el-input> -->
                <template slot-scope="scope">
                    <el-form-item   :prop="'domains.' + scope.$index + '.start_register'"
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]"
                    >
                      <el-input size="small" maxlength="4" oninput="value=value.replace(/[^0-9^A-F^a-f]/g, '')" v-model="scope.row.start_register" placeholder="0x0001" ></el-input>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="寄存器个数" prop="register_num" min-width="12%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.register_num'"
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                      <el-input size="small"  maxlength="4" oninput="value=value.replace(/[^0-9^A-F^a-f]/g, '')" v-model="scope.row.register_num" placeholder="0x0001" ></el-input>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="属性名" prop="property" min-width="18%">
                <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.property'"
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                      <el-input size="small" v-model="scope.row.property" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="property" ></el-input>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="数据格式" prop="format" min-width="18%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.format'"
                    :rules="[
                          { required: true, message: '必填!', trigger: ['blur','change'] },
                    ]">
                      <el-select size="small" v-model="scope.row.format" placeholder="16进制输出">
                        <el-option v-for="item in appforms.format" :key="item.index" :label="item.value" :value="item.index">
                        </el-option>
                      </el-select>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label='规则计算' prop="rule" min-width="20%">
              <template slot-scope="scope"  >
                <el-form-item  :prop="'domains.' + scope.$index + '.rule'" >
                  <div v-if="scope.row.format === 1 || scope.row.format === 3 ">
                      <el-select size="small" style="width: 50px" v-model="scope.row.rule.sign" placeholder="+">
                      <el-option v-for="item in appforms.rule" :key="item.index" :label="item.value" :value="item.value">
                      </el-option>
                      </el-select>
                      <el-input size="small" type="number" style="width: 90px"  v-model="scope.row.rule.number" placeholder="100" ></el-input>
                  </div>
                  <div v-else >
                    <el-select size="small" disabled style="width: 50px" v-model="scope.row.rule.sign" placeholder="+">
                        <el-option v-for="item in appforms.rule" :key="item.index" :label="item.value" :value="item.value">
                        </el-option>
                      </el-select>
                      <el-input  disabled size="small" oninput="value=value.replace(/[^\d]/g, '')" style="width: 90px" v-model="scope.row.rule.number" placeholder="100" ></el-input>
                  </div>

                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label='' prop="rule" min-width="8%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.property'" >
                      <el-button size= "small" type="danger" icon="el-icon-delete" @click="removeDomain(scope.row)" plain></el-button>
                    </el-form-item>
                </template>
            </el-table-column>
          </el-table>
        </el-form>
        <el-row  slot="footer">
          <el-button type="primary" @click="addDomain('dynamicValidateForm')" size="small" plain>新增属性</el-button>
          <el-button type="primary" @click="submitForm('dynamicValidateForm')" size="small">保存</el-button>
        </el-row>
      </el-dialog>
    </div>
    <div class="dialogfrommodel1 dialogfrommodel">
      <el-dialog   :title="'新增设备模板('+form1.typeSelected[1]+')'" :visible.sync="dialogFormCreateMQTT"  width= "680px">
        <el-form  label-position="left"  :model="mqttform"   ref="mqttform" inline-message= true>
          <el-table :data="mqttform.domains" class="table" style="width: 100%">
            <el-table-column label="字段名称" prop="property" min-width="22%" >
              <template slot-scope="scope">
                <el-form-item  :prop="'domains.' + scope.$index + '.property'" :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                  <el-input size="small"  v-model="scope.row.property" oninput="value=value.replace(/[^0-9/^A-Z^a-z]/g, '')" placeholder="property" ></el-input>
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="设置别名" prop="as_name" min-width="22%">
                <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.as_name'"
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                      <el-input size="small"  v-model="scope.row.as_name" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="as name" ></el-input>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="字段类型" prop="type" min-width="22%" >
              <template slot-scope="scope">
                <el-form-item  :prop="'domains.' + scope.$index + '.type'" >
                  <el-radio-group v-model="scope.row.type" size="small">
                    <el-radio-button label="root">根数据</el-radio-button>
                    <el-radio-button label="node">节点数据</el-radio-button>
                  </el-radio-group>
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="是否为空" prop="is_null" min-width="10%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.is_null'" >
                      <el-select size="small" v-model="scope.row.is_null" placeholder="是">
                        <el-option v-for="item in appforms.NULL_type" :key="item.index" :label="item.value" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                </template>
            </el-table-column>

            <el-table-column label='' prop="as_name" min-width="8%">
              <template slot-scope="scope">
                  <el-button size= "small" type="danger" icon="el-icon-delete" @click="removemqttform(scope.row)" plain></el-button>
                </template>
            </el-table-column>

          </el-table>
       </el-form>
        <el-row  slot="footer">
          <el-button type="primary" @click="addDomain('mqttform')" size="small" plain>新增字段</el-button>
          <el-button type="primary" @click="submitForm('mqttform')" size="small">保存</el-button>
        </el-row>
      </el-dialog>
    </div>

    <!--SMT-->
    <el-dialog class="SMT" :title="'新增设备模板(SMT-'+form1.typeSelected[2]+')'" :visible.sync="dialogFormCreateSMT"  width= "680px">
      <el-form label-position="left" :model="smt_data" ref="smt_data" :rules="smt_rules">
        <el-form-item label="数据来源：" prop="local_dataFrom">
          <el-select @change="resetFormSMT()" v-model="smt_data.local_dataFrom" placeholder="请选择数据来源">
            <el-option label="local files" value="local files"></el-option>
            <el-option label="shared files" value="shared files"></el-option>
            <el-option label="database" value="database"></el-option>
          </el-select>
        </el-form-item>
        <template v-if="smt_data.local_dataFrom == 'local files'">
          <el-form-item label="选择文件种类：" prop="local_fileType">
            <el-select v-model="smt_data.local_fileType" placeholder="请选择文件种类">
              <el-option v-for="(item,index) in smt_data_get.lo_fileType" :key="index" :label="item.type" :value="item.type"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="选择本地文件：">
            <!-- <el-upload
              class="upload-demo"
              action="http://127.0.0.1:8080/until"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :before-remove="beforeRemove"
              multiple
              :limit="3"
              :on-exceed="handleExceed"
              :file-list="fileList">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload> -->
            <el-button type="primary" @click="selectFolder()">选择文件夹</el-button>
            {{folderName}}
          </el-form-item>
          <el-form-item label="输入正则表达式：" prop="local_regular" :rules="[
                          { required: true, message: '请输入正则表达式!', trigger: 'blur' },
                    ]">
            <el-tooltip class="item" effect="dark" :enterable='false' placement="top">
              <div slot="content">
                  常用正则表达式规则：<br/>
                  ^： 从文件名开头匹配。<br/>
                  $： 匹配到文件名结尾。<br/>
                  .： 匹配一个任意字符，除了换行符，当re.DOTALL标记被指定时，则可以匹配包括换行符的任意字符。<br/>
                  \.： 匹配一个'.'字符。<br/>
                  [...]： 匹配单字符。用来表示一组字符,单独列出：[amk] 匹配 'GEVENT_LIST'，'m'或'k'。<br/>
                  [^...]：匹配单字符。不在[]中的字符：[^abc] 匹配除了a,b,c之外的字符。<br/>
                  *： 匹配0个或多个的前一个字符规则, 例如a*表示匹配0个或多个a。<br/>
                  +： 匹配1个或多个的前一个字符规则, 例如a*表示匹配1或多个a。<br/>
                  {n}：匹配n个的前一个字符规则, 例如a{3}表示匹配aaa。<br/>
                  {n,m}：匹配n~m个的前一个字符规则, 例如a{1,3}表示匹配a或aa或aaa。<br/>
                  \w： 匹配一个字母或数字。<br/>
                  \W： 匹配一个非字母且非数字的字符。<br/>
                  \s： 匹配一个任意空白字符， 如\t或\n或\r或\f等不可见的字符。<br/>
                  \S： 匹配一个非任意空白字符， 除\t或\n或\r或\f等不可见的字符之外的字符。<br/>
                  \d： 匹配一个数字。<br/>
                  \D： 匹配一个非数字的字符。<br/>
                  ()： 提取字符串。</div>
              <el-input class="smt_input" v-model="smt_data.local_regular" placeholder="请输入正则表达式"></el-input>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="读写周期：" prop="local_io" :rules="[
                          { required: true, message: '请输入读写周期!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" type="text" v-model="smt_data.local_io" @input="numRules(smt_data.local_dataFrom)" placeholder="请输入读写周期">
              <template slot="append">min</template>
            </el-input>
          </el-form-item>
        </template>
        <template v-else-if="smt_data.local_dataFrom == 'shared files'">
          <el-form-item label="主机名：" prop="shared_host" :rules="[
                          { required: true, message: '请输入主机名!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.shared_host" placeholder="请输入主机IP"></el-input>
          </el-form-item>
          <el-form-item label="端口：" prop="shared_port" :rules="[
                          { required: true, message: '请输入端口!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.shared_port" placeholder="请输入端口号"></el-input>
          </el-form-item>
          <el-form-item label="用户名：" prop="shared_user" :rules="[
                          { required: true, message: '请输入用户名!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.shared_user" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码：" prop="shared_pass" :rules="[
                          { required: true, message: '请输入密码!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.shared_pass" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-form-item label="选择文件种类：" prop="shared_fileType">
            <el-select v-model="smt_data.shared_fileType" placeholder="请选择文件种类">
              <el-option v-for="(item,index) in smt_data_get.sha_fileType" :key="index" :label="item.type" :value="item.type"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="文件夹名：" prop="shared_folder" :rules="[
                          { required: true, message: '请输入文件夹名!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.shared_folder" placeholder="请输入文件夹名"></el-input>
          </el-form-item>
          <el-form-item label="正则表达式：" prop="shared_regular" :rules="[
                          { required: true, message: '请输入正则表达式!', trigger: 'blur' },
                    ]">
            <el-tooltip class="item" effect="dark"  placement="top" :enterable='false'>
              <div slot="content">
                  常用正则表达式规则：<br/>
                  ^： 从文件名开头匹配。<br/>
                  $： 匹配到文件名结尾。<br/>
                  .： 匹配一个任意字符，除了换行符，当re.DOTALL标记被指定时，则可以匹配包括换行符的任意字符。<br/>
                  \.： 匹配一个'.'字符。<br/>
                  [...]： 匹配单字符。用来表示一组字符,单独列出：[amk] 匹配 'GEVENT_LIST'，'m'或'k'。<br/>
                  [^...]：匹配单字符。不在[]中的字符：[^abc] 匹配除了a,b,c之外的字符。<br/>
                  *： 匹配0个或多个的前一个字符规则, 例如a*表示匹配0个或多个a。<br/>
                  +： 匹配1个或多个的前一个字符规则, 例如a*表示匹配1或多个a。<br/>
                  {n}：匹配n个的前一个字符规则, 例如a{3}表示匹配aaa。<br/>
                  {n,m}：匹配n~m个的前一个字符规则, 例如a{1,3}表示匹配a或aa或aaa。<br/>
                  \w： 匹配一个字母或数字。<br/>
                  \W： 匹配一个非字母且非数字的字符。<br/>
                  \s： 匹配一个任意空白字符， 如\t或\n或\r或\f等不可见的字符。<br/>
                  \S： 匹配一个非任意空白字符， 除\t或\n或\r或\f等不可见的字符之外的字符。<br/>
                  \d： 匹配一个数字。<br/>
                  \D： 匹配一个非数字的字符。<br/>
                  ()： 提取字符串。</div>
              <el-input class="smt_input" v-model="smt_data.shared_regular" placeholder="请输入正则表达式"></el-input>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="读写周期：" prop="shared_io" :rules="[
                          { required: true, message: '请输入读写周期!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" type="text" v-model="smt_data.shared_io" @input="numRules(smt_data.local_dataFrom)" placeholder="请输入读写周期">
              <template slot="append">min</template>
            </el-input>
          </el-form-item>
        </template>
        <template v-else-if="smt_data.local_dataFrom == 'database'">
          <el-form-item label="数据库类型：" prop="data_type">
            <el-select v-model="smt_data.data_type" placeholder="请选择数据库类型">
              <el-option v-for="(item,index) in smt_data_get.da_type" :key="index" :label="item.type" :value="item.type"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="选择文件种类：" prop="data_fileType">
            <el-select v-model="smt_data.data_fileType" placeholder="请选择文件种类">
              <el-option v-for="(item,index) in smt_data_get.da_fileType" :key="index" :label="item.type" :value="item.type"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="用户名：" prop="data_user" :rules="[
                          { required: true, message: '请输入用户名!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.data_user" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码：" prop="data_pass" :rules="[
                          { required: true, message: '请输入密码!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.data_pass" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-form-item label="IP地址：" prop="data_IP" :rules="[
                          { required: true, message: '请输入IP地址!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.data_IP" placeholder="请输入IP地址"></el-input>
          </el-form-item>
          <el-form-item label="端口：" prop="data_port" :rules="[
                          { required: true, message: '请输入端口!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.data_port" placeholder="请输入端口号"></el-input>
          </el-form-item>
          <el-form-item label="数据库名：" prop="data_name" :rules="[
                          { required: true, message: '请输入数据库名!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.data_name" placeholder="请输入数据库名"></el-input>
          </el-form-item>
          <el-form-item label="sql语句：" prop="data_sql" :rules="[
                          { required: true, message: '请输入sql语句!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" v-model="smt_data.data_sql" placeholder="请输入sql语句"></el-input>
          </el-form-item>
          <el-form-item label="读写周期：" prop="data_io" :rules="[
                          { required: true, message: '请输入读写周期!', trigger: 'blur' },
                    ]">
            <el-input class="smt_input" type="text" v-model="smt_data.data_io" @input="numRules(smt_data.local_dataFrom)" placeholder="请输入读写周期">
              <template slot="append">min</template>
            </el-input>
          </el-form-item>
        </template>
      </el-form>
      <el-row  slot="footer">
        <el-button type="primary" @click="resetFormSMT('smt_data')" size="small">重置</el-button>
        <el-button type="primary" @click="submitFormSMT('smt_data')" size="small">保存</el-button>
      </el-row>
    </el-dialog>

    <!-- 应用模板弹出框 -->
    <el-dialog :title="'协议接口配置('+select_template+')'"
        :visible.sync="dialogFormRtu" width="680px" custom-class="chile-device-box dialog-form"
    >
      <modbus-rtu-form  :templatename ="select_template"
        @CloseDialog="closeDialogRtu" >
      </modbus-rtu-form>

    </el-dialog>
     <el-dialog :title="'协议接口配置('+select_template+')'"
        :visible.sync="dialogFormTcp" width="680px" custom-class="chile-device-box dialog-form"
    >
      <modbus-tcp-form  :templatename ="select_template"
        @CloseDialog="closeDialogTcp" >
      </modbus-tcp-form>

    </el-dialog>
    <div class="dialogFormtemplate">
    <el-dialog title="模板保存" :visible.sync="dialogFormCreatedesc" width="560px">
      <el-radio-group v-model="templateForm.type" size="small">
        <el-radio-button label="template">保存至通用模板库(默认)</el-radio-button>
        <el-radio-button label="one">不保存,只对该设备可用</el-radio-button>
      </el-radio-group>
      <div style="margin: 20px;"></div>
      <el-form  label-position="left" label-width="100px" :model="templateForm" :rules="tmp_rules"  ref="templateForm">
        <el-form-item
          class = "el-form-item1"
          prop="template_name"
          label="模板名"
        >
          <el-input v-model="templateForm.template_name" placeholder="template name"></el-input>
      </el-form-item>
      <el-form-item
          class = "el-form-item1"
          prop="remark"
          label="模板描述"
        >
          <el-input v-model="templateForm.remark" placeholder="template desc"></el-input>
      </el-form-item>
      </el-form>
       <el-row  slot="footer">
        <el-button type="primary" @click="dialogFormCreatedesc = false" size="small" plain>取消</el-button>
        <el-button type="primary"  size="small" @click="saveTemp('templateForm')">确认</el-button>
      </el-row>
    </el-dialog>
    </div>
    
    <el-dialog title="选择文件夹" :visible.sync="dialogFormSelectFolder">


      <folder :mount="mount" :addFolderName="addFolderName" v-on:addFolderProp="addFolderProp" ref="folder"></folder>
      
      
      <el-row  slot="footer">
        <el-button :disabled="isEnable" type="primary" style="float:left" @click="openAdd(true)" size="small">新增文件夹</el-button>
        <el-col class="sele_col" :span="9">
          <el-input size="small" v-model="addFolderName" style="width:80%" type="text"></el-input>
          <i class="el-icon-success" @click="addFolder()"></i>
          <i class="el-icon-error" @click="openAdd(false)"></i>
        </el-col>
        <el-button type="primary" @click="dialogFormSelectFolder = false" size="small" plain>取消</el-button>
        <el-button type="primary"  size="small" @click="seleFolder()">选择文件夹</el-button>
      </el-row>
    </el-dialog>
  </el-main>
</template>


<script>
import { checkNull } from '../../../until/checkRules'
import modbusRtuForm from '../components/modbusRtuForm.vue'
import modbusTcpForm from '../components/modbusTcpForm.vue'
import folder from '../../remotely/components/mount'

export default {
  data () {
    // 检测模板名是否已经存在
    var dulatemplatename = (rule, value, callback) => {
      // 验证用户名是否存在.  一会再写
      if (value.length < 2) {
        callback(new Error('长度在 2 到 15 个字符之间'))
      } else if (value.length > 15) {
        callback(new Error('长度在 2 到 15 个字符之间'))
      } else {
        this.$axios.post('/apis/device/template?select=1', {
          select_templatename: value
        })
          .then(response => {
            if (response.data.is_indb === 1) {
              callback(new Error('该模板名称已经存在！'))
            } else {
              callback()
            }
          })
      }
    }
    return {
      fileList:[{
        name:"",
        url:""
      }],
      subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
      tmp_rules: { // 表单验证
        template_name: [
          { required: true, message: '请输入设备模板名称!', trigger: 'blur' },
          { validator: dulatemplatename, trigger: 'blur' }
        ],
        remark: [
          { required: true, message: '请输入该设备模板的描述信息!', trigger: 'blur' },
          { min: 5, max: 30, message: '长度在 5 到 30 个字符之间', trigger: 'blur' }
        ]
      },
      appforms: {
        function_code: [
          { index: 0, value: '03' },
          { index: 1, value: '04' }
        ],
        format: [
          { index: 0, value: '2进制输出' },
          { index: 1, value: '10进制输出' },
          { index: 2, value: '16进制输出' },
          { index: 3, value: 'IEEE-754输出' }
        ],
        NULL_type: [
          { index: 0, value: '是' },
          { index: 1, value: '否' }
        ],
        rule: [
          { index: 0, value: '+' },
          { index: 1, value: '-' },
          { index: 2, value: '*' },
          { index: 3, value: '/' }
        ]
      },
      dynamicValidateForm: {
        domains: [{
          function_code: '',
          start_register: '',
          register_num: '',
          property: '',
          format: '',
          rule: {
            sign: '',
            number: ''
          }
        }]

      },
      mqttform: {
        domains: [{
          property: '',
          type: 'root',
          is_null: '是',
          as_name: ''
        }] },
      templateForm: {
        template_name: '',
        remark: '',
        type: 'template'
      },
      isEnable:false,
      tip_disabled:true,
      dialogFormCreate: false,
      dialogFormCreateMQTT: false,
      dialogFormCreatedesc: false,
      dialogFormCreateSMT: false,
      dialogFormSelectFolder:false,
      loading: false,
      select_template: '',
      mount:"folder",
      folderName:'',
      addFolderName:'',
      addFolderPath:'',
      form1: {
        typeSelected: ''
      },
      smt_rules: { // 表单验证
        local_dataFrom: [
          { required: true, message: '请选择数据来源!', trigger: 'change' },
        ],
        local_fileType: [
          { required: true, message: '请选择文件类型!', trigger: 'change' },
        ],
        shared_fileType: [
          { required: true, message: '请选择文件类型!', trigger: 'change' },
        ],
        shared_folder: [
          { required: true, message: '请选择文件夹!', trigger: 'change' },
        ],
        data_fileType: [
          { required: true, message: '请选择文件类型!', trigger: 'change' },
        ],
        data_type: [
          { required: true, message: '请选择数据库类型!', trigger: 'change' },
        ],
      },
      smt_data:[{
          local_file:[{
            local_dataFrom:["local files","shared files","database"],
            local_fileType:'',
            local_regular:'',
            local_io:''
          }],
          shared_files:[{
            shared_host:'',
            shared_port:'',
            shared_user:'',
            shared_pass:'',
            shared_folder:'',
            shared_regular:'',
            shared_io:'',
            shared_fileType:'',
          }],
          databa:[{
            data_type:'',
            data_user:'',
            data_pass:'',
            data_ip:'',
            data_port:'',
            data_name:'',
            data_sql:'',
            data_io:'',
            data_fileType:'',
          }]
        }],
      smt_data_get:[{
            lo_fileType:[{}],
            sha_fileType:[{}],
            da_fileType:[{}],
            da_type:[{}],
        }],
      protocolList: [],
      tableData: [],
      // dialogFormVisible: false,
      dialogFormTcp: false,
      dialogFormRtu: false,
      rules: {
        typeSelected: [
          {
            required: true, validator: checkNull, trigger: 'blur'
          }
        ]
      }
    }
  },
  components: {
    modbusRtuForm,
    modbusTcpForm,
    folder,
  },
  created () {
    this.getData()
  },
  mounted(){
    $(".sele_col").hide()
  },
  methods: {
    templateApply (row) {
      this.select_template = row.name
      switch (row.protocol) {
        case 'Modbus-TCP':
          this.dialogFormTcp = true
          break
        case 'Modbus-RTU':
          this.dialogFormRtu = true
          break
      }
    },
    clickTable (row, index, e) {
      this.$refs.refTable.toggleRowExpansion(row)
    },
    catchange () {
      if (this.form1.typeSelected.length === 0) {
        this.$axios.get('apis/device/template', {
          params: {
            subdevice: this.subdevice_name
          }
        })
          .then(response => {
            this.tableData = response.data.db
          // console.log(this.tableData)
          })
          .catch(function (error) {
            console.log(error)
          })
      } else {
        this.$axios.get('apis/device/template', {
          params: {
            typeSelected: this.form1.typeSelected
          }
        }).then(response => {
          this.tableData = response.data.db
        })
          .catch(function (error) {
            console.log(error)
          })
      }
    },
    getData () {
      this.$axios.get('apis/device/protocol/') // 设备协议清单
        .then(response => {
          this.protocolList = response.data.db
          // console.log(this.protocolList);
          
        })
      this.$axios.get('apis/device/template', {
        params: {
          subdevice: this.subdevice_name
        }
      })
        .then(response => {
          this.tableData = response.data.db
        // console.log(this.tableData)
        })
        .catch(function (error) {
          console.log(error)
        })
        
    },
    closeDialogTcp (val) {
      this.dialogFormTcp = val
    },
    closeDialogRtu (val) {
      this.dialogFormRtu = val
    },
    saveTemp (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.dialogFormCreate = false
          this.dialogFormCreatedesc = false
          this.$axios.post('apis/device/template/create/', {
            code_list: this.dynamicValidateForm.domains,
            template_name: this.templateForm.template_name,
            template_remark: this.templateForm.remark,
            type: this.templateForm.type,
            accordname: this.form1.typeSelected
          })
            .then(function (response) {
              console.log(response.data.message)
              _this.resetForm(formName)
              _this.resetForm('dynamicValidateForm')
            })
            .catch(function (error) {
              console.log(error)
            })
          this.$axios.get('apis/device/template', {
            params: {
              typeSelected: this.form1.typeSelected
            }
          }).then(response => {
            _this.tableData = response.data.db
          })
            .catch(function (error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    submitForm (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.dialogFormCreatedesc = true
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    submitFormCreate (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(this.form1.typeSelected[1])
          switch (this.form1.typeSelected[1]) {
            case 'Modbus-TCP':
            case 'Modbus-RTU':
              this.dialogFormCreate = true
              break
            case 'MQTT':
              this.dialogFormCreateMQTT = true
              break
            case 'SMT':
              this.$axios.get('/shebei/smtdataList/', {
                  params: {
                    file_type: this.form1.typeSelected[2]
                  }
                })
                .then(response => {
                  this.dialogFormCreateSMT = true
                  this.smt_data_get.lo_fileType = response.data.db['file_type']
                  this.smt_data_get.sha_fileType = response.data.db['file_type']
                  this.smt_data_get.da_fileType = response.data.db['file_type']
                  this.smt_data_get.da_type = response.data.db['db_type']
                })
                .catch(function (error) {
                  console.log(error)
                })
              break
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    submitFormSMT (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.resetFormSMT("smt_data")
          this.dialogFormCreateSMT = false
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetFormSMT (formName) {
      var _this = this
      if(formName == "smt_data"){
        this.smt_data = [{
            local_file:[{
              local_dataFrom:["local files","shared files","database"],
              local_fileType:'',
              local_regular:'',
              local_io:''
            }],
            shared_files:[{
              shared_host:'',
              shared_port:'',
              shared_user:'',
              shared_pass:'',
              shared_folder:'',
              shared_regular:'',
              shared_io:'',
              shared_fileType:'',
            }],
            databa:[{
              data_type:'',
              data_user:'',
              data_pass:'',
              data_ip:'',
              data_port:'',
              data_name:'',
              data_sql:'',
              data_io:'',
              data_fileType:'',
            }]
        }]
        this.smt_data_get = [{
              lo_fileType:[{}],
              sha_fileType:[{}],
              da_fileType:[{}],
              da_type:[{}],
          }]
        this.$axios.get('/shebei/smtdataList/', {
            params: {
              file_type: this.form1.typeSelected[2]
            }
          })
          .then(response => {
            this.smt_data_get.lo_fileType = response.data.db['file_type']
            this.smt_data_get.sha_fileType = response.data.db['file_type']
            this.smt_data_get.da_fileType = response.data.db['file_type']
            this.smt_data_get.da_type = response.data.db['db_type']
          })
          .catch(function (error) {
            console.log(error)
          })
      }
      this.$refs['smt_data'].clearValidate()
    },
    resetForm (formName) {
      this.dynamicValidateForm = {
        domains: [{
          function_code: '',
          start_register: '',
          register_num: '',
          property: '',
          format: '',
          rule: {
            sign: '',
            number: ''
          }
        }],
        template_name: '',
        remark: ''
      }
    },
    removemqttform (item) {
      var index = this.mqttform.domains.indexOf(item)
      if (this.mqttform.domains.length !== 1) {
        this.mqttform.domains.splice(index, 1)
      }
    },
    removeDomain (item) {
      var index = this.dynamicValidateForm.domains.indexOf(item)
      if (this.dynamicValidateForm.domains.length !== 1) {
        this.dynamicValidateForm.domains.splice(index, 1)
      }
    },
    addDomain (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (formName === 'mqttform') {
            this.mqttform.domains.push(
              {
                property: '',
                type: 'root',
                is_null: '是',
                as_name: ''
              }
            )
          } else if (formName === 'dynamicValidateForm') {
            this.dynamicValidateForm.domains.push({
              function_code: this.dynamicValidateForm.domains[0].function_code,
              start_register: '',
              register_num: '',
              property: '',
              format: '',
              rule: {
                sign: '',
                number: ''
              }
            })
          }
        } else {
          console.log('no add!!')
          return false
        }
      })
    },
    //文件上传处理
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${ file.name }？`);
    },
    //用正则表达式控制输入只能为数字或小数点
    numRules(dataForm){
      // console.log(dataForm);
      switch (dataForm) {
        case "local files":
          this.smt_data.local_io=this.smt_data.local_io.replace(/[^\d^\.]+/g, '')
          console.log(this.smt_data.local_io);
          if(this.smt_data.local_io.length>5){
            
          //   if(this.smt_data.local_io > 99999){
          //     this.smt_data.local_io = 99999
          //   }else{
              this.smt_data.local_io=this.smt_data.local_io.slice(0,5)
          //   }
          }
          break;
        case "shared files":
          this.smt_data.shared_io=this.smt_data.shared_io.replace(/[^\d^\.]+/g, '')
          console.log(this.smt_data.shared_io);
          if(this.smt_data.shared_io.length>5){
            
          //   if(this.smt_data.shared_io > 99999){
          //     this.smt_data.shared_io = 99999
          //   }else{
              this.smt_data.shared_io=this.smt_data.shared_io.slice(0,5)
          //   }
          }
          break;
        case "database":
          this.smt_data.data_io=this.smt_data.data_io.replace(/[^\d^\.]+/g, '')
          console.log(this.smt_data.data_io);
          if(this.smt_data.data_io.length>5){
            
          //   if(this.smt_data.data_io > 99999){
          //     this.smt_data.data_io = 99999
          //   }else{
              this.smt_data.data_io=this.smt_data.data_io.slice(0,5)
          //   }
          }
          break;
      
        default:
          break;
      }
    },
    //打开文件夹选择窗口
    selectFolder(){
      this.dialogFormSelectFolder = true
    },
    //选中文件夹
    seleFolder(){
        this.dialogFormSelectFolder = false
        // console.log(this.$refs['folder'].folderPath);
        // console.log(this.$refs['folder'].folderName);
        this.folderName = this.$refs['folder'].folderPath + this.$refs['folder'].folderName
        // console.log(this.folderName);
    },
    //打开新增输入框
    openAdd(boo){
      if(boo == true){
        $(".sele_col").show()
        $(".sele_col input").focus()
        this.$refs['folder'].dir.push({
          filetype:'folder',
          filename:'add',
          isShow:true
        })
        this.$refs['folder'].assignment()
        this.$refs['folder'].sele()
        this.$refs['folder'].timer()
        document.getElementsByClassName('mount')[0].scrollTop = document.getElementsByClassName('mount')[0].scrollHeight
        this.isEnable = true;
      }else{
        this.$refs['folder'].dir.splice([this.$refs['folder'].dir.length-1],1)
        this.$refs['folder'].isShow=false
        this.$refs['folder'].isTooltip=true
        $(".sele_col").hide()
        this.isEnable = false;
        this.addFolderName = ''
      }
    },
    //新增文件夹
    addFolder(){
      var _this = this
      _this.addFolderPath = ''
      for(var i = 0 ; i < _this.$refs['folder'].fileName.length ; i++){
        _this.addFolderPath = _this.addFolderPath + _this.$refs['folder'].fileName[i] + '/'
      }
      if(_this.addFolderName == ''){
        // console.log('文件名不能为空！');
        _this.$Message.WarningMessage(_this, '文件名不能为空！')
      }else if(_this.addFolderPath == ''){
        // console.log('当前路径不能创建文件夹！');
        _this.$Message.WarningMessage(_this, '当前路径不能创建文件夹！')
      }else{
        _this.$axios.get('shebei/smtdataList/?file_mkdir=' + (_this.addFolderPath + _this.addFolderName))
            .then(response =>{
              if(response.data.db != null){
                _this.$refs['folder'].dir = response.data.db
                _this.$refs['folder'].timer()
                _this.$Message.SuccessMessage(_this, '文件夹创建成功！')
                _this.isEnable = false;
                $(".sele_col").hide()
                _this.$refs['folder'].dir['isShow'] = false
                _this.addFolderName = ''
              }else{
                _this.$Message.ErrorMessage(_this, response.data.Error)
              }
            })
            .catch(error =>{
              console.log("connect fail！");
              _this.$Message.ErrorMessage(_this, 'connect fail！')
            })
      }
    },
    //接收子组件的传值，更新父组件的值
    addFolderProp:function(data){
      this.addFolderName = data
    }
  }

}
</script>

<style >
  .dialogFormtemplate .el-dialog__body{
    padding: 20px 20px 0px;
  }
  .dialogfrommodel .el-dialog__body {
    padding: 10px 20px
  }
  .dialogfrommodel .el-table .cell {
    padding-left: 0px;
  }
  .dialogfrommodel .el-form-item {
    margin-bottom: 0px
  }
  .dialogfrommodel .el-form-item1 {
    margin-bottom: 20px;

  }

  .el-table__expanded-cell[class*=cell] {
    padding: 20px 30px;
    background-color: #1e466b21;
  }
  .el-col-6 {
    padding: 7px;
  }
  .el-input__inner {
    padding: 0 4px;
  }
  .dialog-form .el-dialog__body {
      padding: 10px 20px 15px 20px;
  }
  .dialogfrommodel .el-radio-button__orig-radio:checked+.el-radio-button__inner {
      color: #FFF;
      background-color: #08c78f;
      border-color: #08c78f;
      -webkit-box-shadow: -1px 0 0 0 #08c78f;
      box-shadow: -1px 0 0 0 #08c78f;
  }




  .SMT .el-form-item__label{
    width: 21%;
  }
  .SMT .el-select{
    width: 79%;
  }
  .SMT .el-select .el-input{
    width: 100%;
  }
  .SMT input{
    text-align: center;
    width: 100%;
  }
  .SMT .smt_input{
    width: 79%;
  }
  .SMT .readWrite{
    position: absolute;
    right: 20px;
  }
  .SMT .el-dialog__wrapper .el-dialog{
    width: 60%;
  }
  .el-dialog__body .mount{
    max-height: 35em
  }
  .sele_col .el-icon-success{
    font-size: 20px;
    cursor: pointer;
    color: #1aba53;
  }
  .sele_col .el-icon-error{
    font-size: 20px;
    cursor: pointer;
    color: #c23232;
  }
</style>