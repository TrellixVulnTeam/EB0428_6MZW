<template>
  <el-main class="no-padding">
    <el-row class="row-padding">
      <el-form :inline="true">
        <el-form-item label="接口类型:">
          <el-select v-model="interfaceType">
            <el-option
              v-for="item in typeList"
              :key="item.index"
              :value="item.index"
              :label="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="协议名称:">
          <el-select v-model="protocol">
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
      ]
    };
  }
};
</script>

<style scoped>
</style>
