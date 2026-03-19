<template>
  <router-view/>
</template>

<script setup>
import {useRoute} from "vue-router";
import {onMounted, watch} from "vue";
import store from "@/store";

onMounted(() => {
  store.state.hasRoutes = false
})

const whiteList = ['/', '/index', '/login']

const route = useRoute()
watch(route, (to, from) => {
  console.log(to.name, to.path)
  if (whiteList.indexOf(to.path) === -1) {
    let obj = {
      name: to.name,
      path: to.path
    }

    store.commit('ADD_TABS', obj)
  }
}, {deep: true, immediate: true})
</script>

<style>
html, body, #app{
  height:100%
}

.app-container{
  padding: 20px;
}
</style>
