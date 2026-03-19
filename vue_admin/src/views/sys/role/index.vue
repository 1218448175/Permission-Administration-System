<script setup>
import {Delete, DocumentAdd, Edit, Search, Tools} from "@element-plus/icons-vue";
import {ref} from "vue";
import * as requestUtil from "@/util/request";
import {ElMessage} from "element-plus";
import Dialog from "./components/dialog.vue"
import MenuDialog from "./components/menuDialog.vue"

// 请求时携带的参数
const queryForm = ref({
  query: '',
  pageNum: 1,
  pageSize: 10,
})

// 表单绑定数据
const tableData = ref([])

const total = ref(0)

// 弹窗绑定参数
const id = ref(-1)

const dialogVisible = ref(false)

const dialogTitle = ref('')

// 权限菜单弹窗绑定参数
const menuDialogVisible = ref(false)

// 刷新角色列表
const initRoleList = async () => {
  let res = await requestUtil.post("role/search", queryForm.value)
  tableData.value = res.data.roleList
  total.value = res.data.total
}


// 删除按钮状态
const delBtnStatus = ref(true)

// 删除角色的id列表
const multipleSection = ref([])

// 处理角色信息弹窗事件
const handleDialogValue = (roleId) => {
  if (roleId) {
    dialogTitle.value = "角色修改"
    id.value = roleId
  } else {
    dialogTitle.value = "角色添加"
    id.value = -1
  }
  dialogVisible.value = true
}

// 处理删除事件
const handleDelete = async (id) => {
  let ids = []
  if (id) {
    // 删除单条数据
    ids.push(id)
  } else {
    // 删除多条数据
    multipleSection.value.forEach(item => {
      ids.push(item.id)
    })
  }

  // 请求后端修改数据库
  const res = await requestUtil.del("role/action", ids)
  if (res.data.code === 200) {
    ElMessage.success('执行成功')
    initRoleList()
  } else {
    ElMessage.error(res.data.msg)
  }
}

// 处理复选框变化事件
const handleSelectionChange = (selection) => {
  console.log('勾选了')
  multipleSection.value = selection
  delBtnStatus.value = selection.length === 0
}

// 处理为角色分配权限弹窗事件
const handleMenuDialogValue = (roleId) => {
  if (roleId) {
    id.value = roleId
  }
  menuDialogVisible.value = true
}

// 处理当前页号变化事件
const handleCurrentChange = (pageNum) => {
  queryForm.value.pageNum = pageNum
  initRoleList()
}

//处理每页大小变化事件
const handleSizeChange = (pageSize) => {
  queryForm.value.pageSize = pageSize
  queryForm.value.pageNum = 1
  initRoleList()
}

initRoleList()

</script>

<template>
  <div class="app-container">

    <el-row :gutter="20" class="header">
      <el-col :span="7">
        <el-input placeholder="请输入角色名..." v-model="queryForm.query" clearable></el-input>
      </el-col>
      <el-button type="primary" :icon="Search" @click="initRoleList">搜索</el-button>
      <el-button type="success" :icon="DocumentAdd" @click="handleDialogValue()">新增</el-button>
      <el-popconfirm title="您确定批量删除这些记录吗？" @confirm="handleDelete(null)">
        <template #reference>
          <el-button type="danger" :disabled="delBtnStatus" :icon="Delete">批量删除</el-button>
        </template>
      </el-popconfirm>
      <Dialog v-model="dialogVisible" :dialogVisible="dialogVisible" :id="id" :dialogTitle="dialogTitle"
              @initRoleList="initRoleList"></Dialog>
      <MenuDialog :id="id" v-model="menuDialogVisible" :menuDialogVisible="menuDialogVisible"
                  @initRoleList="initRoleList"></MenuDialog>
    </el-row>
    <el-table
        :data="tableData"
        stripe
        style="width: 100%"
        @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <el-table-column prop="name" label="角色名" width="100" align="center"/>
      <el-table-column prop="code" label="权限字符" width="200" align="center"/>
      <el-table-column prop="create_time" label="创建时间" width="200" align="center"/>
      <el-table-column prop="remark" label="备注"/>
      <el-table-column prop="action" label="操作" width="400" fixed="right" align="center">
        <template v-slot="scope">
          <el-button type="primary" :icon="Tools" @click="handleMenuDialogValue(scope.row.id)">分配权限</el-button>

          <el-button v-if="scope.row.code!='admin'" type="primary" :icon="Edit"
                     @click="handleDialogValue(scope.row.id)"/>

          <el-popconfirm v-if="scope.row.code!='admin'" title="您确定要删除这条记录吗？" @confirm="handleDelete(scope.row.id)">
            <template #reference>
              <el-button type="danger" :icon="Delete"/>
            </template>
          </el-popconfirm>

        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        v-model:currentPage="queryForm.pageNum"
        v-model:page-size="queryForm.pageSize"
        :page-sizes="[10, 20, 30, 40,50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
    />
  </div>
</template>

<style lang="scss" scoped>

.header {
  padding-bottom: 16px;
  box-sizing: border-box;
}

.el-pagination {
  float: right;
  padding: 20px;
  box-sizing: border-box;
}

::v-deep th.el-table__cell {
  word-break: break-word;
  background-color: #f8f8f9 !important;
  color: #515a6e;
  height: 40px;
  font-size: 13px;

}

.el-tag--small {
  margin-left: 5px;
}
</style>