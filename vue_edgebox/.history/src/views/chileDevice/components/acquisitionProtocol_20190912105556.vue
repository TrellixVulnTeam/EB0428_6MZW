<template>
  <el-main>
    <el-row class="row-padding">
      <el-form>
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
              v-for="item in typeList"
              :key="item.index"
              :value="item.index"
              :label="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
    </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      interfaceType: "",
      typeList: [
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
      protocol: '', // 协议名称
    };
  }
};
</script>

<style scoped>
</style>
