<script setup>
import {useRoute} from "vue-router";
import {ref, watch} from "vue";
import {HomeFilled} from '@element-plus/icons-vue'

const route = useRoute()
const breadcrumbList = ref([])
const parentName = ref('')

const initBreadcrumbList = () => {
  breadcrumbList.value = route.matched;
  parentName.value = route.meta.parentName
  console.log(breadcrumbList)
}

watch(route, () => {
  initBreadcrumbList()
}, {deep: true, immediate: true})

</script>

<template>
  <el-icon>
    <HomeFilled/>
  </el-icon>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="(item,index) in breadcrumbList" :key="index">
      <span class="redirect" v-if="parentName && index>0">{{ parentName }}  / </span>
      <span class="no-redirect" v-if="index==breadcrumbList.length-1">{{ item.name }}</span>
      <span class="redirect" v-else>{{ item.name }}</span>
    </el-breadcrumb-item>

  </el-breadcrumb>
</template>

<style scoped lang="scss">
.no-redirect {
  cursor: text;
}

.redirect {
  color: #666;
  font-weight: 600;
  cursor: pointer;

  &:hover {
    color: #304156
  }
}
</style>