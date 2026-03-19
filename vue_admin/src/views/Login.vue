<template>
<div class="login">
  <el-form ref="loginRef" :model="loginForm" :rules="loginRules" class="login-form">
    <h3 class="title">后台管理系统</h3>

    <el-form-item prop="username">
      <el-input
          v-model="loginForm.username"
          type="text"
          size="large"
          auto-complete="off"
          placeholder="账号"
      >
        <template #prefix>
          <svg-icon icon="user"/>
        </template>
      </el-input>
    </el-form-item>

    <el-form-item prop="password">
      <el-input
          v-model="loginForm.password"
          type="password"
          size="large"
          auto-complete="off"
          placeholder="密码"
      >
        <template #prefix>
          <svg-icon icon="password"/>
        </template>
      </el-input>
    </el-form-item>

    <el-form-item prop="code">
      <el-input
          v-model="loginForm.code"
          size="large"
          auto-complete="off"
          placeholder="验证码"
          style="width: 63%"
          @keyup.enter="handleLogin"
      >
        <template #prefix>
          <svg-icon icon="validCode"/>
        </template>
      </el-input>
      <div class="login-code">
        <img :src="codeUrl" @click="getCode" class="login-code-img"/>
      </div>
    </el-form-item>

    <el-checkbox v-model="loginForm.rememberMe" style="margin:0 0 25px 0;">记住密码</el-checkbox>

    <el-form-item style="width:100%;">
      <el-button
          size="large"
          type="primary"
          style="width:100%;"
          @click.prevent="handleLogin"
      >
        <span>登 录</span>
      </el-button>
    </el-form-item>
  </el-form>
</div>
</template>

<script setup>
  import {ref} from 'vue'
  import requestUtil from '@/util/request'
  import qs from 'qs'
  import {ElMessage} from 'element-plus'
  import Cookies from 'js-cookie'
  import { encrypt, decrypt } from "@/util/jsencrypt";
  import { createRouter, createWebHistory } from "vue-router";
  import router from "@/router";

  const loginForm = ref({
    username:'',
    password:'',
    rememberMe:false,
    code: '',
    uuid: '',
  })

  const loginRules = {
    username : [{required:true, trigger:"blur", message:'请输入你的账号'}],
    password : [{required:true, trigger:"blur", message:'请输入密码'}]
  }

  const loginRef = ref(null)

  // 验证码url
  const codeUrl = ref('')

  // 向后端请求验证码和uuid
  const getCode = async () => {
    const res = await requestUtil.get("user/captcha")
    loginForm.value.uuid = res.data.uuid
    codeUrl.value = res.data.base64str
  }

  getCode()

  const handleLogin = () =>{
    loginRef.value.validate(async (valid) =>{
      if (valid) {
        let result = await requestUtil.post("user/login?" + qs.stringify(loginForm.value))
        let data = result.data
        if (data.code == 200) {
          ElMessage.success(data.info)
          window.sessionStorage.setItem("token", data.token)
          const currentUser = data.user
          currentUser.roles = data.roles
          window.sessionStorage.setItem("currentUser", JSON.stringify(currentUser))   //.parse转换为JSON对象
          window.sessionStorage.setItem("menuList", JSON.stringify(data.menuList))
          // 如果勾选了记住密码，则在Cookies中设置记住用户名和密码
          if (loginForm.value.rememberMe){
            Cookies.set('username', loginForm.value.username, {expires: 30})    // expires: 过期时间设为30天
            Cookies.set('password', encrypt(loginForm.value.password), {expires: 30})
            Cookies.set('rememberMe', loginForm.value.rememberMe, {expires: 30})
          }else{
            // 否则移除
            Cookies.remove('username')
            Cookies.remove('password')
            Cookies.remove('rememberMe')
          }
          router.replace('/')
        } else {
          ElMessage.error(data.info)
        }
      }else{
        console.log('验证失败')
      }
    })
  }

  function getCookie() {
    const username = Cookies.get('username')
    const password = Cookies.get('password')
    const rememberMe = Cookies.get('rememberMe')
    loginForm.value = {
      username: username === undefined ? loginForm.value.username : username,
      password: password === undefined ? loginForm.value.password : decrypt(password),
      rememberMe: rememberMe === undefined ? false : Boolean(rememberMe),
    }
  }

  getCookie()

</script>

<style lang="scss" scoped>
a{
  color:white
}
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-image: url("../assets/images/login_background_2.jpg");
  background-size: cover;
}
.title {
  margin: 0 auto 30px auto;
  text-align: center;
  color: #707070;
}
.login-form {
  border-radius: 6px;
  background: #ffffff;
  width: 400px;
  padding: 25px 25px 5px 25px;
  .el-input {
    height: 40px;
    input {
      display: inline-block;
      height: 40px;
    }
  }
  .input-icon {
    height: 39px;
    width: 14px;
    margin-left: 0;
  }
}
.login-tip {
  font-size: 13px;
  text-align: center;
  color: #bfbfbf;
}
.login-code {
  width: 33%;
  height: 40px;
  float: right;
  img {
    cursor: pointer;
    vertical-align: middle;
  }
}
.el-login-footer {
  height: 40px;
  line-height: 40px;
  position: fixed;
  bottom: 0;
  width: 100%;
  text-align: center;
  color: #fff;
  font-family: Arial,serif;
  font-size: 12px;
  letter-spacing: 1px;
}
.login-code-img {
  height: 40px;
  padding-left: 12px;
}
</style>