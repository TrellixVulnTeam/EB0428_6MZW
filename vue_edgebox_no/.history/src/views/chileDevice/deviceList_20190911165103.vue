<template>
  <el-main class="no-padding">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">子设备列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
        <el-button type="primary" size="small">新增</el-button>
        <el-button size="small" disabled>批量删除</el-button>
        <el-button size="small" disabled>批量禁用</el-button>
        <el-button size="small" disabled>批量启用</el-button>
         <el-input placeholder="请输入内容" size="small" v-model="searchDevice" class="pull-right search-input">
             <el-button type="primary" slot="append" icon="el-icon-search"></el-button>
         </el-input>
    </el-row>
    <el-table :data="tableData" stripe>
        <el-table-column label="名称" prop="name"></el-table-column>
        <el-table-column label="类型" prop="type"></el-table-column>
        <el-table-column label="位置" prop="location"></el-table-column>
        <el-table-column label="型号" prop="model"></el-table-column>
        <el-table-column label="描述" prop="description"></el-table-column>
        <el-table-column label="最近上线时间" prop="time"></el-table-column>
        <el-table-column label="启用/禁用" prop="operating"></el-table-column>
        <el-table-column label="状态" prop="status"></el-table-column>
        <el-table-column label="操作">
            <template>
                <el-button type="text" size="small">
                    删除
                </el-button>
            </template>
        </el-table-column>
    </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        searchDevice: '', // 搜索设备名称
    };
  }
};
</script>

<style scoped>
</style>
