<template>
    <div>
      <button @click="backToPreviousPage">返回</button>
      <h2>个人信息修改</h2>
      <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="用户名">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="个性签名">
          <el-input v-model="form.signature"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('form')">提交</el-button>
        </el-form-item>
      </el-form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useStore } from 'vuex';
  import { ElMessage } from 'element-plus';
  
  export default {
    name: 'userInfo',
    setup() {
      const store = useStore();
      const form = ref({
        username: store.state.user.username,
        password: '',
        email: store.state.user.email,
        signature: ''
      });
  
      const backToPreviousPage = () => {
        // TODO: 返回上一界面的逻辑
      };
  
      const submitForm = async () => {
        const formData = form.value;
        // TODO: 调用后端的更新用户接口，传递formData，并处理返回的数据
        try {
          const response = await fetch(`/users/${store.state.user.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
          });
          if (!response.ok) throw new Error('Network response was not ok');
          const result = await response.json();
  
          if (result.username === formData.username && result.email === formData.email) {
            ElMessage.success('个人信息修改成功');
            // TODO: 更新Vuex中的用户状态
            store.commit('updateUser', result);
          } else {
            ElMessage.error('个人信息修改失败');
          }
        } catch (error) {
          console.error('Error:', error);
          ElMessage.error('服务器出现问题，请稍后再试');
        }
      };
  
      return { backToPreviousPage, form, submitForm };
    },
  };
  </script>
  