<template>
    <div class="login">
      <div class="login-container">
        <div class="login-main">
          <div class="login-header">
            <div>登录</div>
          </div>
          <div class="login-form">
            <div class="form-item">
              <input v-model="username" class="password-input" placeholder="请输入用户名"/>
            </div>
            <div class="form-item">
              <input v-model="password.value" class="password-input" placeholder="请输入密码" :type="password.visible ? 'text':'password'"/>
              <img class="password-image" @click="switchPasswordVisible" src="../assets/images/visible.png"/>
            </div>
            <div class="form-item">
              <button class="form-item-btn" @click="login">登录</button>
            </div>
           <div class="form-item">
            <!-- 注册按钮 -->
            <button class="form-item-btn" @click="goToRegister">注册</button>
           </div>
            <div v-show="errorVisible" class="form-error">账号或密码错误!</div>
          </div>
          <div class="version">{{ version }}</div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { reactive, toRefs } from 'vue'
  import { useRouter } from 'vue-router'
  import { useStore } from 'vuex'  // import useStore
  import axios from 'axios'
  
  export default {
    name: 'UserLogin',
    setup() {
      const router = useRouter()
      const store = useStore()
      const state = reactive({
        version: '0.1.0',
        username: '',
        password: {
          visible: false,
          value: ''
        },
        errorVisible: false,
        globalData: {
          currentUser: null
        },
      })
      // 注册按钮的点击事件处理函数
    const goToRegister = () => {
      router.replace({ path: './userRegister' })
    }
      const switchPasswordVisible = () => {
        state.password.visible = !state.password.visible
      }
  
      const login = async () => {
        if (state.username.trim() !== '' && state.password.value.trim() !== '') {
          try {
            const response = await axios.post("http://localhost:8000/login", {
              username: state.username,
              password: state.password.value,
            })
            console.log(response.data)
            // localStorage.setItem('user', JSON.stringify(response.data))

            store.dispatch('setUser', response.data);

            connectSocket(response.data.id)
            // router.replace({ path: './helloWorld' })
          } catch (error) {
            state.errorVisible = true
          }
        }
      }
  
      const connectSocket = (userId) => {
        const websocket = new WebSocket("ws://localhost:8000/ws/" + userId)
      websocket.onopen = () => {
        console.log("success!")
        store.dispatch('setWebsocket', websocket)  // save websocket in store
        router.replace({ path: './helloWorld' })
      }
}
      return {
        ...toRefs(state),
        switchPasswordVisible,
        login,
        goToRegister
      }
    },
  }
  </script>
  

  <style scoped>
  .login {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .login-container {
    border-radius: 12px;
  }

  .login-main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .login-header {
    width: 300px;
    text-align: center;
    font-size: 30px;
    font-weight: 500;
    color: #d02129;
  }

  .login-form {
    width: 300px;
  }

  .form-item {
    position: relative;
    margin: 30px 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .selected-area {
    width: 280px;
    display: flex;
    align-items: center;
    padding: 5px 10px;
    border: 1px solid #DCDFE6;
    border-radius: 4px;
    cursor: pointer;
  }

  .selected-area .selected-content {
    display: flex;
    align-items: center;
    flex-grow: 1;
    height: 37px;
  }

  .selected-area .selected-content img {
    width: 35px;
    height: 35px;
    margin-right: 15px;
    border-radius: 50%;
  }

  .selected-area .selected-icon {
    width: 20px;
    height: 20px;
    margin-right: 5px;
  }

  .selected-area .rotate {
    transform-origin: center;
    transform: rotate(180deg);
  }

  .dialog-area {
    position: absolute;
    top: 55px;
    left: 0;
    width: 300px;
    background: #FFFFFF;
    border: 1px solid #DCDFE6;
    z-index: 99;
  }

  .dialog-list-item {
    width: 100%;
    margin: 15px 0;
    padding-left: 10px;
    display: flex;
    align-items: center;
    cursor: pointer;
  }

  .dialog-list-item-avatar {
    width: 35px;
    height: 35px;
    margin-right: 15px;
    border-radius: 50%;
  }

  .password-input {
    width: 280px;
    height: 37px;
    display: flex;
    align-items: center;
    padding: 5px 10px;
    border: 1px solid #DCDFE6;
    border-radius: 4px;
  }

  .password-image {
    width: 25px;
    height: 25px;
    position: absolute;
    top: 15px;
    right: 15px;
    cursor: pointer;
  }

  .form-item-btn {
    width: 100%;
    color: #FFFFFF;
    background-color: #d02129;
    border: none;
    height: 35px;
    cursor: pointer;
    text-align: center;
    font-size: 14px;
    border-radius: 4px;
  }

  .form-error {
    color: #d02129;
    margin-bottom: 22px;
  }

  .login-main .version {
    color: #FFFFFF;
  }

</style>
  
  