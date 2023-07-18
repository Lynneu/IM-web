import { createRouter, createWebHashHistory } from 'vue-router';
import UserLogin from '../views/login.vue';
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
  {
    path: '/userInfo',
    name: 'userInfo',
    component: () => import('@/views/userInfo.vue'),
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
