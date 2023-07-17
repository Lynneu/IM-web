// main.js
import { createApp, reactive } from 'vue'
import App from './App.vue'
import router from './router'  // 引入路由配置
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import store from './store'

const socket = reactive({ instance: null })

createApp(App)
  .use(router) // 使用路由
  .use(ElementPlus)
  .use(store)
  .provide('socket', socket)
  .mount('#app')
