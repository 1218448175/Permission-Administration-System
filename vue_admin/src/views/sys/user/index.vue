<script setup>
import {ref} from "vue";
import * as requestUtil from "@/util/request";
import {getServerUrl} from "@/util/request";
import {Search, Delete, DocumentAdd, Edit, Tools, RefreshRight} from '@element-plus/icons-vue'
import Dialog from './components/dialog.vue'
import {ElMessage} from "element-plus";
import RoleDialog from "./components/roleDialog.vue";

// 删除操作部分
// 删除按钮状态,true为未激活
const delBtnStatus = ref(true)

// 绑定在table组件上的变量，包含被选中的行
const multipleSelection = ref([])

// 复选框处理函数
const handleSelectionChange = (selection) => {
  console.log(selection)
  multipleSelection.value = selection
  delBtnStatus.value = selection.length === 0
}

// 删除函数
const handleDelete = async (id) =>{
  // 统一传数组到后端
  let ids = []
  if (id) {
    ids.push(id)
  } else {
    // 遍历勾选的数据，加入数组
    multipleSelection.value.forEach(row => {
      ids.push(row.id)
    })
  }

  // 通过del方式请求后端
  const res = await requestUtil.del("user/action", ids)
  const data = res.data
  if (data.code === 200) {
    ElMessage.success('删除成功')
    // 刷新列表
    initUserList()
  } else {
    ElMessage.error(data.msg)
  }
}

/*用户信息弹窗*/
// 是否弹窗
const dialogVisible = ref(false)

// 弹窗标题
const dialogTitle = ref("")

const id = ref(-1)

/*角色弹窗*/
const sysRoleList = ref([])

const roleDialogVisible = ref(false)

// 通过id判断添加还是修改
const handleDialogValue = (userId) => {
  if (userId) {
    id.value = userId;
    dialogTitle.value = "用户修改"
  } else {
    id.value = -1;
    dialogTitle.value = "用户添加"
  }
  dialogVisible.value = true
}

// 角色弹窗处理函数
const handleRoleDialogValue = (userId, roleList) => {
  console.log('userId:', userId)
  console.log('roleList', roleList)
  id.value = userId
  sysRoleList.value = roleList
  roleDialogVisible.value = true
}

// 用户信息数据部分
const tableData = ref([])

const total = ref(0)

// 请求时携带的对象
const queryForm = ref({
  query: '',
  pageNum: 1,
  pageSize: 10
})

// 重置密码
const handleResetPassword = async (id) => {
  const res = await requestUtil.get("user/resetPassword?id=" + id)
  if (res.data.code === 200) {
    ElMessage.success('密码重置成功')
    initUserList()
  } else {
    ElMessage.error(res.data.msg)
  }
}

// 处理状态改变
const statusChangeHandle = async (row) => {
  let res = await requestUtil.post("user/status", {id: row.id, status: row.status})
  if (res.data.code === 200) {
    ElMessage({
      type: "success",
      message: '执行成功'
    })
  } else {
    ElMessage({
      type: "error",
      message: res.data.msg
    })
    initUserList()
  }
}

// 初始化列表
const initUserList = async() =>{
  const res = await requestUtil.post("user/search", queryForm.value)
  tableData.value = res.data.userList
  total.value = res.data.total
}

// 每页大小改变
const handleSizeChange = (pageSize) => {
  queryForm.value.pageSize = pageSize
  queryForm.value.pageNum = 1
  initUserList()
}

// 当前页改变
const handleCurrentChange = (pageNum) => {
  queryForm.value.pageNum = pageNum
  initUserList()
}

initUserList()

</script>

<template>
  <div class="app-container">
    <el-row :gutter="20" class="header">
      <el-col :span="7">
        <el-input placeholder="请输入用户名..." v-model="queryForm.query" clearable></el-input>
      </el-col>
      <el-button type="primary" :icon="Search" @click="initUserList">搜索</el-button>
      <el-button type="success" :icon="DocumentAdd" @click="handleDialogValue()">新增</el-button>
      <el-popconfirm title="您确定批量删除这些记录吗？" @confirm="handleDelete(null)">
        <template #reference>
          <el-button type="danger" :disabled="delBtnStatus" :icon="Delete">批量删除</el-button>
        </template>
      </el-popconfirm>
      <Dialog v-model="dialogVisible" :dialogVisible="dialogVisible" :id="id" :dialogTitle="dialogTitle"
        @initUserList="initUserList"></Dialog>
      <RoleDialog :id="id" :sysRoleList="sysRoleList" :roleDialogVisible="roleDialogVisible" v-model="roleDialogVisible"
       @initUserList="initUserList"></RoleDialog>
    </el-row>

    <el-table :data="tableData" stripe style="width: 100%" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <el-table-column prop="avatar" label="头像" width="80" align="center">
        <template v-slot="scope">
          <img :src="getServerUrl()+'media/userAvatar/'+scope.row.avatar" width="50" height="50" alt=""/>
        </template>
      </el-table-column>
      <el-table-column prop="username" label="用户名" width="100" align="center"/>
      <el-table-column prop="roles" label="拥有角色" width="200" align="center">
        <template v-slot="scope">
          <el-tag size="small" type="warning" v-for="item in scope.row.roleList"> {{ item.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="email" label="邮箱" width="200" align="center"/>
      <el-table-column prop="phonenumber" label="手机号" width="120" align="center"/>
      <el-table-column prop="status" label="状态？" width="200" align="center">
        <template v-slot="{row}">
          <el-switch v-model="row.status" @change="statusChangeHandle(row)" active-text="正常"
                     inactive-text="禁用" :active-value="1" :inactive-value="0"></el-switch>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="200" align="center"/>
      <el-table-column prop="login_date" label="最后登录时间" width="200" align="center"/>
      <el-table-column prop="remark" label="备注"/>
      <el-table-column prop="action" label="操作" width="400" fixed="right" align="center">
        <template v-slot="scope">
          <el-button type="primary" :icon="Tools" @click="handleRoleDialogValue(scope.row.id,scope.row.roleList)">分配角色
          </el-button>

          <el-popconfirm v-if="scope.row.username!=='python222'" title="您确定要对这个用户重置密码吗？"
                         @confirm="handleResetPassword(scope.row.id)">
            <template #reference>
              <el-button type="warning" :icon="RefreshRight">重置密码</el-button>
            </template>
          </el-popconfirm>

          <el-button type="primary" v-if="scope.row.username!=='python222'" :icon="Edit"
                     @click="handleDialogValue(scope.row.id)"></el-button>
          <el-popconfirm v-if="scope.row.username!=='python222'" title="您确定要删除这条记录吗？"
                         @confirm="handleDelete(scope.row.id)">
            <template #reference>
              <el-button type="danger" :icon="Delete"/>
            </template>
          </el-popconfirm>


        </template>
      </el-table-column>

    </el-table>

    <el-pagination
      v-model:current-page="queryForm.pageNum"
      v-model:page-size="queryForm.pageSize"
      :page-sizes="[100, 200, 300, 400]"
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