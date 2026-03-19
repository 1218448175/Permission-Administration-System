<script setup>
import {ref, defineProps} from "vue";
import {ElMessage} from "element-plus";
import requestUtil from '@/util/request'

const props = defineProps({
  user: {
    type: Object,
    default: () => {
    },
    required: true,
  }
})

const pwdRef = ref(null)

const form = ref({
  id: -1,
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

form.value = props.user

const equalToPassword = (rule, value, callback) => {
  if (form.value.newPassword !== value) {
    callback(new Error("两次输入的密码不一致"))
  } else {
    callback()
  }
}

const rules = ref({
  oldPassword: [{required: true, message: '旧密码不能为空', trigger: 'blur'}],
  newPassword: [{required: true, message: '新密码不能为空', trigger: 'blur'},{
    min: 6,
    max: 20,
    message: '长度在6到20之间',
    trigger: 'blur',
  }],
  confirmPassword: [{required: true, message: '确认密码不能为空', trigger: 'blur'},{
    required: true,
    validator: equalToPassword,
    trigger: 'blur',
  }],
})

const handleSubmit = () => {
  pwdRef.value.validate(async (valid) => {
    if (valid) {
      let result = await requestUtil.post("user/updateUserPwd", form.value)
      let data = result.data
      if (data.code == 200) {
        ElMessage.success("修改密码成功，下一次登录生效")
      } else {
       ElMessage.error(data.errorInfo)
      }
    }
  })
}

</script>

<template>
  <el-form ref="pwdRef" :model="form" :rules="rules" label-width="80px">
    <el-form-item label="旧密码：" prop="oldPassword">
      <el-input v-model="form.oldPassword" placeholder="请输入旧密码" type="password"/>
    </el-form-item>

    <el-form-item label="新密码" prop="newPassword">
      <el-input v-model="form.newPassword" placeholder="请输入新密码" type="password"/>
    </el-form-item>

    <el-form-item label="确认密码" prop="confirmPassword">
      <el-input v-model="form.confirmPassword" placeholder="请输入确认密码" type="password"/>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="handleSubmit">保存</el-button>
    </el-form-item>
  </el-form>
</template>

<style scoped lang="scss">

</style>