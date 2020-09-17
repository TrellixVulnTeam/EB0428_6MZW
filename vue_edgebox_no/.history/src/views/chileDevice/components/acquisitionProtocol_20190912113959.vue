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
        <el-table-column label="操作" width="100">
            <template v-slot="scope">
                <el-button type="text" size="small">应用</el-button>
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
    };
  }
};
</script>

<style scoped>
</style>
