import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@/assets/styles/reset.css'
import '@/assets/styles/border.css'
import SvgIcon from '@/icons'
import '@/router/permission'
// 国际化中文
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// createApp(App).use(store).use(router).use(ElementPlus).mount('#app')

// 抑制 ResizeObserver 无关警告
const originalError = console.error
console.error = function (...args) {
  // 关键修复：先判断 args[0] 是否为字符串，再调用 includes
  if (args && typeof args[0] === 'string' && args[0].includes('ResizeObserver loop completed with undelivered notifications')) {
    return // 过滤该警告
  }
  originalError.apply(console, args) // 使用 apply 传递完整的参数数组
}

const app = createApp(App)
SvgIcon(app)

app.use(store)
app.use(router)
app.use(ElementPlus, {
    locale: zhCn,
})
app.mount('#app')
