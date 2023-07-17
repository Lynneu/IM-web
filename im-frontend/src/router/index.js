import { createRouter, createWebHashHistory } from 'vue-router';
import UserLogin from '../views/login.vue';
import userFriends from '../views/conversations.vue';
import helloWorld from '../views/helloWorld.vue';

const routes = [
  {
    path: '/',
    name: 'UserLogin',
    component: UserLogin,
  },
  {
    path: '/helloworld',
    name: 'helloWorld',
    component: helloWorld,
  },
  {
    path: '/userRegister',
    name: 'UserRegister',
    component: () => import(/* webpackChunkName: "register" */ '../views/userRegister.vue')
  },
  
  // 如果有其他页面，你可以按照下面的格式添加：
  {
    path: '/conversations',
    name: 'userFriends',
    component: userFriends,
  },
  {
    path: '/privatechat/:friendId',
    name: 'privatechat',
    component: () => import('@/views/privatechat.vue'),
    props: true
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
