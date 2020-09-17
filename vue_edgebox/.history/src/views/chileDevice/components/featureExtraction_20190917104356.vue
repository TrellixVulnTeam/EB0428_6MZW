<template>
  <el-main class="no-padding">
    <el-row>
      <!-- 基本信息 -->
      <el-col :span="{xs: 12, sm: 12,  md: 12, lg: 12, xl: 12}">
        <el-card>
          <el-form :model="baseForm" label-width="80px" label-position="left">
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
              <el-button type="text" size="small"></el-button>
            </el-form-item>
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <!-- 特征数据 -->
      <el-col :span="{xs: 12, sm: 12,  md: 12, lg: 12, xl: 12}">

      </el-col>
    </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      baseForm: {
        name: 'Lichang90011',
        type: '力创电表',
        position: 'E5-4F',
        templateName: '',
        serial: 'com3',
        dataBit: 8,
        baudRate: '9600',
        parity: 'o（奇校验）',
        stopBit: 2,
        timeout: '5s',
        cycle: '10s',
        address: '02'
      }
    }
  },
}
</script>

<style scoped>

</style>
