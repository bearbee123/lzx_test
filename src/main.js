// 导入Vue对象
import Vue from 'vue'
// 导入App.vue组件，.vue可省略不写
import App from './App.vue'
// 导入router目录下所有路由
import a from './router'
//将vuex挂在
import store from"./store/index"

// 阻止启动生产消息（启动时console多显示一条信息）
Vue.config.productionTip = false

// 创建Vue实例
new Vue({
  // 配置router，完整写法router : a
  router: a,
  store,
  render: h => h(App)
}).$mount('#app') // 挂载id='app'
