import { createStore } from 'vuex'

export default createStore({
  state: {
    hasRoutes: false,               // 是否绑定路由
    editableTabsValue: '/',    // 存放当前标签值
    editableTabs: [                 // 存放所有标签
      {
        title: '首页',
        name: '/index',
      }
    ]
  },
  getters: {
  },
  mutations: {
    // 添加标签页
    ADD_TABS: (state, tab)=>{
      if (state.editableTabs.findIndex(e => e.name === tab.path) === -1) {
        // 当前标签不存在，添加新标签到数组
        state.editableTabs.push({
          title: tab.name,
          name: tab.path
        });
      }
      // 已存在，将当前激活标签页设置为传入的标签路径
      state.editableTabsValue = tab.path
    },
    // 重置标签页
    RESET_TABS: (state) => {
      state.editableTabsValue = '/index';
      state.editableTabs = [
        {
          title: '首页',
          name: '/index'
        }
      ]
    },
    UPDATE_TABS: (state, tabs) => {
      state.editableTabs = tabs
    },
    UPDATE_TABS_VALUE: (state, activeName) => {
      state.editableTabsValue = activeName
    },
    SET_ROUTES_STATE: (state, hasRoutes) => {
      state.hasRoutes = hasRoutes
    }
  },
  actions: {
  },
  modules: {
  }
})
