<script setup>
import {defineProps, ref} from "vue";
import requestUtil, {getServerUrl} from "@/util/request";
import {ElMessage} from 'element-plus'
import {Plus} from '@element-plus/icons-vue'

const props = defineProps({
  user: {
    type: Object,
    default: () => {
    },
    required: true,
  }
})

const form = ref({
  id: -1,
  avatar: '',
})

const formRef = ref(null)

const imageUrl = ref('')

const headers = ref({
  Authorization: window.sessionStorage.getItem('token')
})

form.value = props.user

// 图片将要存放的路径
imageUrl.value = getServerUrl() + 'media/userAvatar/' + form.value.avatar

// 图像上传成功后的回调函数
const handleAvatarSuccess = (res) => {
  console.log('回调函数', form.value)
  // 更新前端头像显示的Url
  imageUrl.value = getServerUrl() + 'media/userAvatar/' + res.title
  // 同步表单中的图像字段，方便后续提交
  form.value.avatar = res.title
  console.log('回调函数，已修改', form.value)
}

// 图像校验函数
const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg'
  const isLt2M = file.size / 1024 / 1024 < 2
  console.log('上传前', form.value)

  if (!isJPG) {
    ElMessage.error('图像必须为jpg格式')
  }
  if (!isLt2M) {
    ElMessage.error('图像大小不能超过2M')
  }

  return isJPG && isLt2M
}

// 确认更换事件
const handleConfirm = async () => {
  console.log('确认',form.value)
  let result = await requestUtil.post("user/updateAvatar", form.value)
  let data = result.data

  if (data.code == 200) {
    ElMessage.success('执行成功！')
    window.sessionStorage.setItem('currentUser', JSON.stringify(data.user))
    window.location.reload()
  } else {
    ElMessage.error(data.errorInfo)
  }
}

</script>

<template>
  <el-form
      ref="fromRef"
      :model="form"
      label-width="100px"
      style="text-align: center; padding-bottom: 10px"
  >
    <el-upload
      class="avatar-uploader"
      name="avatar"
      :headers="headers"
      :action="getServerUrl()+'user/uploadImage'"
      :show-file-list="false"
      :on-success="handleAvatarSuccess"
      :before-upload="beforeAvatarUpload"
    >
      <img v-if="imageUrl" :src="imageUrl" class="avatar" />
      <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
    </el-upload>

    <el-button @click="handleConfirm">确认更换</el-button>

  </el-form>
</template>

<style>

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}

.avatar {
  width: 120px;
  height: 120px;
  display: block;
}


</style>