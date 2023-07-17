<template>
    <div class="register">
      <div class="register-container">
        <div class="register-main">
          <div class="register-header">
            <div>注册</div>
          </div>
          <div class="register-form">
            <div class="form-item">
              <input v-model="username" class="password-input" placeholder="请输入用户名"/>
            </div>
            <div class="form-item">
              <input v-model="email" class="password-input" placeholder="请输入邮箱"/>
            </div>
            <div class="form-item">
              <input v-model="password.value" class="password-input" placeholder="请输入密码" :type="password.visible ? 'text':'password'"/>
              <img class="password-image" @click="switchPasswordVisible" src="../assets/images/visible.png"/>
            </div>
            <div class="form-item">
              <button class="form-item-btn" @click="register">注册</button>
            </div>
            <div v-show="errorVisible" class="form-error">账号已存在!</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { reactive, toRefs } from 'vue'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  
  export default {
    name: 'UserRegister',
    setup() {
      const router = useRouter()
      const state = reactive({
        username: '',
        email: '',
        password: {
          visible: false,
          value: ''
        },
        errorVisible: false,
      })
  
      const switchPasswordVisible = () => {
        state.password.visible = !state.password.visible
      }
  
      const register = async () => {
        if (state.username.trim() !== '' && state.email.trim() !== '' && state.password.value.trim() !== '') {
          try {
            const response = await axios.post("http://localhost:8000/users/", {
              username: state.username,
              email: state.email,
              password: state.password.value,
            })
            console.log(response.data)
            router.replace({ path: '/' })
          } catch (error) {
            state.errorVisible = true
          }
        }
      }
  
      return {
        ...toRefs(state),
        switchPasswordVisible,
        register,
      }
    },
  }
  </script>
  
  <!-- styles are similar to login page -->
  
  <style scoped>
  .register {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .register-container {
    border-radius: 12px;
  }

  .register-main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .register-header {
    width: 300px;
    text-align: center;
    font-size: 30px;
    font-weight: 500;
    color: #409EFF;
  }

  .register-form {
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
    background-color: #409EFF;
    border: none;
    height: 35px;
    cursor: pointer;
    text-align: center;
    font-size: 14px;
    border-radius: 4px;
  }

  .form-error {
    color: #409EFF;
    margin-bottom: 22px;
  }

  .register-main .version {
    color: #FFFFFF;
  }

</style>
  