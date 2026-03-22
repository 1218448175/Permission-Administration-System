<script setup>
import {defineProps, ref, watch} from 'vue'
import * as requestUtil from "@/util/request";
import {ElMessage} from "element-plus";

// 接收从父组件传来的参数
const props = defineProps(
    {
      id: {
        type: Number,
        default: -1,
        required: true,
      },
      dialogTitle: {
        type: String,
        default: '',
        required: true,
      },
      dialogVisible: {
        type: Boolean,
        default: false,
        required: true
      }
    }
)

// 表单双向绑定数据
const form = ref(
    {
        id: -1,
        username: "",
        password: "123456",
        status: 1,
        phonenumber: "",
        email: "",
        remark: ""
    }
)

// 表单绑定对象
const formRef = ref(null)

// 检查用户名是否重复
const checkUsername = async (rule, value, callback) => {
  if (form.value.id === -1) {
    console.log("提交的信息:", form.value)
    const res = await requestUtil.post("user/check", {'username': form.value.username})
    if (res.data.code === 500) {
      callback(new Error("用户名已存在!"))
    } else {
      callback()
    }
  } else {
    callback()
  }
}

// 表单规则
const rules = ref({
  username: [
    {required: true, message: '请输入用户名'},
    {required: true, validator: checkUsername, trigger: 'blur'}
  ],
  email: [{required: true, message: "邮箱地址不能为空", trigger: "blur"}, {
    type: "email",
    message: "请输入正确的邮箱地址",
    trigger: ["blur", "change"]
  }],
  phonenumber: [{required: true, message: "手机号码不能为空", trigger: "blur"}, {
    pattern: /^1[3456789][0-9]\d{8}$/,
    message: "请输入正确的手机号码",
    trigger: "blur"
  }],
})

// 初始化表单数据
const initFormData = async (id) => {
  const res = await requestUtil.get("user/action?id=" + id)
  form.value = res.data.user
}

// 检测到弹窗变化时，根据id判断是添加还是修改，然后填充弹窗
watch(
    () => props.dialogVisible,
    () => {
      let id = props.id
      if (id !== -1) {
        // 修改
        initFormData(id)
      } else {
        // 添加
        form.value = {
          id: -1,
          username: "",
          password: "123456",
          status: 1,
          phonenumber: "",
          email: "",
          remark: ""
        }
      }
    }
)

const emits = defineEmits(["update:modelValue", "initUserList"])

// 关闭弹窗时， 修改父组件的弹窗激活状态
const handleClose = () => {
  emits('update:modelValue', false)
}

// 确认提交表单，请求修改数据库
const handleConfirm = () => {
  // 异步验证表单
  formRef.value.validate(async (valid) => {
    if (valid) {
      let result = await requestUtil.post("user/save", form.value)
      let data = result.data
      if (data.code === 200) {
        ElMessage.success("执行成功")
        // 重置表单数据
        formRef.value.resetFields()
        // 刷新父组件列表
        emits('initUserList')
        // 关闭表单
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
  <!--作为添加和修改用户对话框页面-->
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
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" :disabled="form.id===-1?false:'disabled'"/>
        <el-alert
            v-if="form.id===-1"
            title="默认初始密码：123456"
            :closable="false"
            style="line-height: 10px;"
            type="success">
        </el-alert>
      </el-form-item>

      <el-form-item label="手机号" prop="phonenumber">
        <el-input v-model="form.phonenumber"/>
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email"/>
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio :label="1">正常</el-radio>
          <el-radio :label="0">禁用</el-radio>
        </el-radio-group>
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