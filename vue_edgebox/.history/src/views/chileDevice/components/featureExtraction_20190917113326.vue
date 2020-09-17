<template>
  <el-main class="no-padding">
    <el-row :gutter="20" class="el-row-margin">
      <!-- 基本信息 -->
      <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
        <el-card>
          <h4 class="title-style">基本信息</h4>
          <el-form :model="baseForm" label-width="150px" label-position="left" class="feature-card">
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="类型:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="位置:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="模板名称:">
              <el-button type="text" size="small">去配置协议</el-button>
            </el-form-item>
            <el-form-item label="串口号:">
              <span>{{baseForm.serial}}</span>
            </el-form-item>
            <el-form-item label="数据位:">
              <span>{{baseForm.dataBit}}</span>
            </el-form-item>
            <el-form-item label="波特率:">
              <span>{{baseForm.baudRate}}</span>
            </el-form-item>
            <el-form-item label="奇偶校验:">
              <span>{{baseForm.parity}}</span>
            </el-form-item>
            <el-form-item label="停止位:">
              <span>{{baseForm.stopBit}}</span>
            </el-form-item>
            <el-form-item label="回复超时:">
              <span>{{baseForm.timeout}}</span>
            </el-form-item>
            <el-form-item label="读写周期:">
              <span>{{baseForm.cycle}}</span>
            </el-form-item>
            <el-form-item label="地址码:">
              <span>{{baseForm.address}}</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <!-- 特征数据 -->
      <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
        <el-card>
          <h4 class="title-style">特征数据</h4>
          <el-form
            :model="featureForm"
            label-width="150px"
            label-position="left"
            class="feature-card"
          >
            <el-form-item label="max:">
              <span>{{featureForm.max}}</span>
            </el-form-item>
            <el-form-item label="min:">
              <span>{{featureForm.min}}</span>
            </el-form-item>
            <el-form-item label="avg:">
              <span>{{featureForm.avg}}</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="el-row-margin table-row">
      <el-card>
        <h4 class="title-style">设备属性</h4>
        <el-table :data="tableData">
          <el-table-column label="NO." prop="index"></el-table-column>
          <el-table-column label="proerty" prop="proerty"></el-table-column>
          <el-table-column label="value" prop="value"></el-table-column>
        </el-table>
      </el-card>
    </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      baseForm: {
        name: "Lichang90011",
        type: "力创电表",
        position: "E5-4F",
        // templateName: '',
        serial: "com3",
        dataBit: 8,
        baudRate: "9600",
        parity: "o（奇校验）",
        stopBit: 2,
        timeout: "5s",
        cycle: "10s",
        address: "02"
      },
      featureForm: {
        max: 28,
        min: 22,
        avg: 25
      },
      tableData: [
        {
          index: 1,
          property: "Temperature",
          value: 28
        },
        {
          index: 2,
          property: "humidity",
          value: 40
        },
        {
          index: 1,
          property: "Temperature",
          value: 28
        },
        {
          index: 2,
          property: "humidity",
          value: 40
        },
        {
          index: 1,
          property: "Temperature",
          value: 28
        },
        {
          index: 2,
          property: "humidity",
          value: 40
        }
      ]
    };
  }
};
</script>

<style scoped>
.title-style {
  margin-bottom: 10px;
}

.table-row {
  margin-top: 20px;
}
</style>
