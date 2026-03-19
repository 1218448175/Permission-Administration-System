<script setup>
import {defineProps, ref} from 'vue'
import requestUtil from "@/util/request";
import {ElMessage} from "element-plus";

// 接受父组件传来的参数user
const props = defineProps(
    {
      user: {
        type: Object,
        default: () => {
        },
        required: true
      }
    }
)

// 存放要修改的字段
const form = ref({
  id: -1,
  phonenumber: '',
  email: '',
})

// 对应表单的映射，与表单绑定
const userRef = ref(null)

// 将参数中的字段赋值给from
form.value = props.user;

// 绑定在表单的规则
const rules = ref({
  email: [{required: true, message: "邮箱地址不能为空", trigger: "blur"}, {
    type: "email",
    message: "请输入正确的邮箱地址",
    trigger: ["blur", "change"]
  }],
  phonenumber: [{required: true, message: "手机号码不能为空", trigger: "blur"}, {
    pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/,
    message: "请输入正确的手机号码",
    trigger: "blur"
  }],
});

// 提交函数
const handleSubmit = () => {

  // 表单验证阶段，异步
  userRef.value.validate(async (valid) => {
    if (valid) {
      // 访问后端接口
      let result = await requestUtil.post("user/save", form.value);
      let data = result.data;
      if (data.code == 200) {
        ElMessage.success("执行成功！")
        window.sessionStorage.setItem("currentUser", JSON.stringify(form.value))
      }
    }
  })
}
</script>

<template>
  <el-form ref="userRef" :model="form" :rules="rules" label-width="100px">
    <el-form-item label="手机号码：" prop="phonenumber">
      <el-input v-model="form.phonenumber" maxlength="11"/>
    </el-form-item>
    <el-form-item label="用户邮箱：" prop="email">
      <el-input v-model="form.email" maxlength="50"/>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="handleSubmit">保存</el-button>

    </el-form-item>
  </el-form>
</template>

<style scoped lang="scss">

</style>