<script setup>
import {defineProps, ref, watch} from 'vue'
import * as requestUtil from "@/util/request";
import {ElMessage} from "element-plus";

const props = defineProps(
    {
      id: {
        required: true,
        default: -1,
        type: Number,
      },
      dialogTitle: {
        required: true,
        default: '',
        type: String,
      },
      dialogVisible: {
        required: true,
        default: false,
        type: Boolean,
      }
    }
)

const form = ref({
  id: -1,
  name: "",
  code: "",
  remark: "",
})

const rules = ref({
  name: [
    {required: true, message: '请输入角色名称'}
  ],
  code: [
    {required: true, message: '请输入权限字符'}
  ]
})

const formRef = ref(null)

const emits = defineEmits(["update:modelValue", "initRoleList"])

const initFormData = async (id) => {
  const res = await requestUtil.get("role/action?id=" + id)
  form.value = res.data.role
}

watch(
    () => props.dialogVisible,
    () => {
      let id = props.id
      if (id !== -1) {
        initFormData(id)
      } else {
        form.value = {
          id: -1,
          name: "",
          code: "",
          remark: ""
        }
      }
    }
)

const handleClose = () => {
  emits("update:modelValue", false)
}

const handleConfirm = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      let res = await requestUtil.post("role/save", form.value)
      let data = res.data
      if (data.code === 200) {
        ElMessage.success('执行成功')
        formRef.value.resetFields()
        emits("initRoleList")
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
    model-value="dialogVisible"
    :title="dialogTitle"
    width="30%"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="角色名称" prop="name">
        <el-input v-model="form.name"/>
      </el-form-item>

      <el-form-item label="权限字符" prop="code">
        <el-input v-model="form.code"/>
      </el-form-item>

      <el-form-item label="备注" prop="remark">
        <el-input v-model="form.remark" type="textarea" :rows="4"/>
      </el-form-item>

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