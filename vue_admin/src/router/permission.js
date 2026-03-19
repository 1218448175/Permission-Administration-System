import router from '@/router/index'
import store from '@/store'
import {routes} from "vue-router/auto-routes";

//路由守卫功能
router.beforeEach(async (to, from , next) => {
    // 白名单
    const whiteList = ['/login']
    // 获取菜单列表和路由激活状态
    let menuList = JSON.parse(window.sessionStorage.getItem('menuList'))
    let hasRoutes = store.state.hasRoutes
    // 判断是否有token
    let token = window.sessionStorage.getItem('token')
    if (token) {
        if (!hasRoutes) {
            // 绑定路由（改为异步等待）
            await bindRoute(menuList)
            // 标志为true
            store.commit("SET_ROUTES_STATE", true)
            // 关键：动态路由注册后，重新执行当前导航（避免跳转未注册的路由）
            return next({ ...to, replace: true })
        }
        // 有token则放行
        next()
    } else {
        // 无token,判断是否在白名单
        if (whiteList.includes(to.path)) {
            next()
        } else {
            next('/login')
        }
    }
})

// 动态绑定路由
const bindRoute = async (menuList) => {
    let newRoutes = router.options.routes
    // 遍历菜单列表
    menuList.forEach(menu => {
        if (menu.children) {
            // 如果有子菜单，则为子菜单生成路由
            menu.children.forEach(m => {
                let route = menuToRoute(m, menu.name)
                if (route) {
                    // 将生成的路由放到第一个根路由的children中
                    newRoutes[0].children.push(route)
                }
            })
        }
    })
    // 重新添加到路由
    newRoutes.forEach(route => {
        router.addRoute(route)
    })
}

// 菜单转为路由规则
const menuToRoute = (menu, parentName) => {
    if (!menu.component) {
        // 如果菜单无组件路径，则不生成路由
        return null
    } else {
        // 生成路由规则
        let route = {
            name: menu.name,
            path: menu.path,
            meta: {
                parentName: parentName  // 元信息，记录父菜单名称
            }
        }
        route.component = () => import('@/views/' + menu.component + '.vue')
        return route
    }
}
