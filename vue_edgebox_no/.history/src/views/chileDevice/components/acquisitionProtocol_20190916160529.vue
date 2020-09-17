<template>
  <el-main class="no-padding">
    <el-row>
      <el-form :inline="true">
        <el-form-item label="接口类型:">
          <el-select size="small" v-model="interfaceType">
            <el-option
              v-for="item in typeList"
              :key="item.index"
              :value="item.index"
              :label="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="协议名称:">
          <el-select size="small" v-model="protocol">
            <el-option
              v-for="item in protocolList"
              :key="item.index"
              :value="item.index"
              :label="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item >
            <el-button type="primary" size="small">自定义</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-table :data="tableData">
        
        <el-table-column label="模板名称" prop="name"></el-table-column>
        <el-table-column label="协议名称" prop="protocol"></el-table-column>
        <el-table-column label="创建时间" prop="createTime"></el-table-column>
        <el-table-column label="描述" prop="description"></el-table-column>
        <el-table-column label="操作" width="80">
            <template v-slot="scope">
                <el-button type="text" size="small" @click="dialogFormVisible = true">应用</el-button>
            </template>
        </el-table-column>
        <el-table-column type="expand">
            <template v-slot="scope">
                <el-form  label-position="left" label-width="200px" >
                    <el-form-item  label="模板名称:">
                        <span>{{scope.row.name}}</span>
                    </el-form-item>
                    <el-form-item label="协议名称:">
                        <span>{{scope.row.protocol}}</span>
                    </el-form-item>
                    <el-form-item label="创建时间:">
                        <span>{{scope.row.createTime}}</span>
                    </el-form-item>
                    <el-form-item label="描述:">
                        <span>{{scope.row.description}}</span>
                    </el-form-item>
                </el-form>
            </template>
        </el-table-column>
    </el-table>
    <!-- 应用模板弹出框 -->
    <el-dialog title="应用" :visible.sync="dialogFormVisible" custom-class="chile-device-box dialog-form">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-form-item label="串口号:" prop="serial">
          <el-select size="small" style="width: 100%" v-model="form.serial" placeholder="请选择所属类别">
            <el-option v-for="item in serialList" :key="item.index" :label="item.value" :value="item.index">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据位:" prop="dataBit">
          <el-select size="small" style="width: 100%" v-model="form.dataBit" placeholder="请选择所属类别">
            <el-option v-for="item in bitList" :key="item.index" :label="item.value" :value="item.index">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="波特率:" prop="baudRate">
          <el-select size="small" style="width: 100%" v-model="form.baudRate" placeholder="请选择所属类别">
            <el-option v-for="item in baudRateList" :key="item.index" :label="item.value" :value="item.index">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="奇偶校验:" prop="parity">
          <el-select size="small" style="width: 100%" v-model="form.parity" placeholder="请选择所属类别">
            <el-option v-for="item in parityList" :key="item.index" :label="item.value" :value="item.index">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="停止位:" prop="stopBit">
          <el-select size="small" style="width: 100%" v-model="form.stopBit" placeholder="请选择所属类别">
            <el-option v-for="item in stopBitList" :key="item.index" :label="item.value" :value="item.index">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="回复超时:" prop="timeout">
          <el-input type="text" size="small" v-model="form.timeout"></el-input>
          <span>s</span>
        </el-form-item>
        <el-form-item label="读写周期:" prop="cycle" >
          <el-input type="text" size="small" v-model="form.cycle"></el-input>
          <el--button type="text">S</el--button>
        </el-form-item>
        <el-form-item label="地址码:" prop="address">
          <el-input type="text" size="small" v-model="form.address"></el-input>
        </el-form-item>
      </el-form>
      <el-row  slot="footer">
        <el-button type="primary" size="small">确定</el-button>
        <el-button type="default" size="small">取消</el-button>
      </el-row>
    </el-dialog>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      interfaceType: "", // 接口类型
      typeList: [
        // 接口类型列表
        {
          index: 0,
          value: "RS232接口类"
        },
        {
          index: 1,
          value: "以太网类型"
        },
        {
          index: 2,
          value: "专有类型"
        }
      ],
      serialList: [  // 串口号列表
        {
          index: 0,
          value: 'com0'
        },
        {
          index: 1,
          value: 'com1'
        },
        {
          index: 2,
          value: 'com2'
        },
        {
          index: 3,
          value: 'com3'
        },
        {
          index: 4,
          value: 'com4'
        },
        {
          index: 5,
          value: 'com5'
        }
      ],
      bitList: [  // 数据位列表
        {
          index: 0,
          value: 5
        },
        {
          index: 1,
          value: 6
        },
        {
          index: 2,
          value: 7
        },
        {
          index: 3,
          value: 8
        }
      ],
      baudRateList: [ // 波特率列表
        {
          index: 0,
          value: 300
        },
        {
          index: 1,
          value: 600
        },
        {
          index: 2,
          value: 1200
        },
        {
          index: 3,
          value: 2400
        },
        {
          index: 4,
          value: 4800
        },
        {
          index: 5,
          value: 9600
        }
      ],
      parityList: [ // 奇偶校验列表
        {
          index: 0,
          value: 'n (无校验)'
        },
        {
          index: 1,
          value: 'e (偶校验)'
        },
        {
          index: 2,
          value: 'o (奇校验)'
        }
      ],
      stopBitList: [ // 停止位列表
        {
          index: 0,
          value: 0
        },
        {
          index: 1,
          value: 2
        },
        {
          index: 2,
          value: 2
        }
      ],
      protocol: "", // 协议名称
      protocolList: [
        // 协议名称列表
        {
          index: "0",
          value: "Modbus-RTU"
        },
        {
          index: "2",
          value: "其他"
        }
      ],
      tableData: [
          {
              name: 'HC31A电表',
              protocol: 'ModBus',
              createTime: '2019-05-25 13:52:47',
              description: 'HC31A电表配置模板'
          },
          {
              name: 'HC31A电表',
              protocol: 'ModBus',
              createTime: '2019-05-25 13:52:47',
              description: 'HC31A电表配置模板'
          },
          {
              name: 'HC31A电表',
              protocol: 'ModBus',
              createTime: '2019-05-25 13:52:47',
              description: 'HC31A电表配置模板'
          }
      ],
      dialogFormVisible: false,
      form: {
          serial: '',
          dataBit: '',
          baudRate: '',
          parity: '',
          stopBit: '',
          timeout: '',
          cycle: '',
          address: ''
      },
      rules: {

      },
    };
  }
};
</script>

<style scoped>
</style>
