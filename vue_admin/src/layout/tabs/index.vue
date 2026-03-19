<template>
  <el-tabs
      v-model="editableTabsValue"
      type="card"
      class="demo-tabs"
      closable
      @tab-remove="removeTab"
      @tab-click="clickTab"
  >
    <el-tab-pane
        v-for="item in editableTabs"
        :key="item.name"
        :label="item.title"
        :name="item.name"
    >
    </el-tab-pane>
  </el-tabs>
</template>

<script setup>
import {ref, watch, onMounted } from 'vue'
import store from "@/store";
import {useRoute, useRouter} from 'vue-router'

const editableTabsValue = ref(store.state.editableTabsValue)
const editableTabs = ref(store.state.editableTabs)
const router = useRouter()

onMounted(async () => {
  // 等待路由表更新完成
  await router.isReady()
  router.push({ path: editableTabsValue.value }).catch(() => {
    router.push('/index')
  })
})

// 修改 clickTab 函数
const clickTab = (pane) => {
  // 1. 从 pane 实例中直接获取点击的 tab name (即路由路径)
  const activePath = pane.props.name

  // 2. 立即手动更新状态，确保 Vuex 和本地同步
  store.commit('UPDATE_TABS_VALUE', activePath)

  // 3. 执行跳转
  router.push({ path: activePath })

  console.log('当前跳转路径:', activePath)
}

const removeTab = (targetName) => {
  const tabs = editableTabs.value
  let activeName = editableTabsValue.value

  if (targetName === '/index') {
    return
  }

  if (activeName === targetName) {
    tabs.forEach((tab, index) => {
      if (tab.name === targetName) {
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activeName = nextTab.name
        }
      }
    })
  }

  editableTabsValue.value = activeName
  editableTabs.value = tabs.filter((tab) => tab.name !== targetName)

  store.commit('UPDATE_TABS', editableTabs.value)
  store.commit('UPDATE_TABS_VALUE', editableTabsValue.value)

  router.push({ path: activeName })

}

const route = useRoute()

watch(() => route.path, (newPath) => {
  // 当路由切换时（无论是点击 Tab 还是浏览器前进后退），同步选中的 Tab
  editableTabsValue.value = newPath
  store.commit('UPDATE_TABS_VALUE', newPath)
}, { immediate: true })

</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs--card > .el-tabs__header .el-tabs__item.is-active {
  background-color: lightgray;
}

.el-main {
  padding: 0;
}

.el-tabs__content{
  padding: 0 !important;;
}

</style>