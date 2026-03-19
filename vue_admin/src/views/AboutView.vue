<template>

  <el-button type="primary" @click="handleLogin">测试登录</el-button>
  <br><br>
  <el-button type="success" @click="handleUserList">测试获取用户信息列表</el-button>

</template>

<script setup>
import requestUtil from "@/util/request"

//处理登录
const handleLogin=async()=>{
  let result = await requestUtil.get('user/jwt_test')
  let data = result.data
  if (data.code==200){
    const token = data.token
    console.log('登录成功：token='+token)
    window.sessionStorage.setItem('token', token)
  }else{
    console.log('登录出错')
  }
}

//获取用户数据
const handleUserList=async()=>{
  let result = await requestUtil.get('user/test')
  let data = result.data
  if (data.code==200){
    const userList = data.data
    console.log('userList='+userList)
  }else{
    console.log('访问页面出了问题')
  }
}

</script>

