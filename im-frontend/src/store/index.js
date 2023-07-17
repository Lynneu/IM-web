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
