<script setup>
import {defineProps, ref, watch} from "vue";
import * as requestUtil from "@/util/request";
import {ElMessage} from "element-plus";

// 接受来自父组件的参数
const props = defineProps(
    {
      id: {
        required: true,
        type: Number,
        default: -1,
      },
      roleDialogVisible: {
        required: true,
        type: Boolean,
        default: false,
      },
      sysRoleList: {
        required: true,
        type: Array,
        default: []
      },
    }
)

const form = ref(
    {
      checkedRoles: [],
      roleList: [],
      id: -1,
    }
)

const formRef = ref(null)

// 初始化组合框表单数据
const initFormData = async (id) => {
  const res = await requestUtil.get("role/listAll?id="+id)
  if (res.data.code === 200) {
    form.value.roleList = res.data.roleList
    form.value.id = id
  } else {
    console.log(res.data.msg)
  }
}

// 检测弹窗状态
watch(
    () => props.roleDialogVisible,
    () => {
      let id = props.id
      // 显示所有框均未选
      if (id !== -1) {
        form.value.checkedRoles = []
        props.sysRoleList.forEach(item => {
          form.value.roleList.push(item.id)
        })
        initFormData(id)
      }
    }
)

const emits = defineEmits(["update:modelValue", "initUserList"])


// 关闭弹窗
const handleClose = () => {
  emits("update:modelValue", false)
}

// 确认授权
const handleConfirm = () => {
  // 验证表单数据
  formRef.value.validate(async (valid) => {
    if (valid) {
      let result = await requestUtil.post("user/grantRole", {"user_id": form.value.id, "roleIds": form.value.checkedRoles})
      let data = result.data
      if (data.code === 200) {
        ElMessage.success('执行成功')
        emits("initUserList")
        handleClose()
      } else {
        ElMessage.error(data.msg)
      }
    } else {
      console.log('fail')
    }
  })
}
</script>

<template>
  <el-dialog
      model-value="roleDialogVisible"
      title="分配角色"
      width="30%"
      @close="handleClose"
  >
    <el-form
        ref = "formRef"
        :model="form"
        label-width="100px"
    >
      <el-checkbox-group v-model="form.checkedRoles">
        <el-checkbox v-for="role in form.roleList" :label="role.id" :key="role.id" :id="role.id" name="checkRoles">
          {{role.name}}
        </el-checkbox>
      </el-checkbox-group>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="handleConfirm">确认</el-button>
        <el-button @click="handleClose">取消</el-button>
      </span>
    </template>

  </el-dialog>
</template>

<style scoped lang="scss">

</style>