import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    websocket: null,
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
    SET_WEBSOCKET(state, websocket) {
      state.websocket = websocket;
    },
    clearUserState(state) {
      state.user = null;  // 假设你的用户状态是存储在 state.user 中的
      state.websocket = null;  // 同样的，你也可以在这里关闭 websocket 连接
    },
  },
  actions: {
    setUser({ commit }, user) {
      commit('SET_USER', user);
    },
    setWebsocket({ commit }, websocket) {
      commit('SET_WEBSOCKET', websocket);
    },
  },
  modules: {
  },
});
