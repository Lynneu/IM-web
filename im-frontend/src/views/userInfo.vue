<template>
    <div class="container">
      <el-button @click="backToPreviousPage" class="back-btn">返回</el-button>
      <el-card class="box-card" v-if="!isEditing">
        <template v-slot:header>
          <span>个人信息</span>
        </template>
        <p><strong>用户名: </strong>{{ username }}</p>
        <p><strong>邮箱: </strong>{{ email }}</p>
        <el-button @click="startEditing" type="primary">修改</el-button>
      </el-card>
      <el-card class="box-card" v-if="isEditing">
        <template v-slot:header>
          <span>修改个人信息</span>
        </template>
        <el-form ref="form" label-width="120px">
            <el-form-item label="用户名">
          <el-input v-model="editingUsername"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editingEmail"></el-input>
        </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus';
  
  export default {
    name: 'userInfo',
    setup() {
      const router = useRouter()
      const store = useStore();
      const username = ref(store.state.user.username);
      const password = ref('');
      const email = ref(store.state.user.email);
      const editingUsername = ref(store.state.user.username);
      const editingEmail = ref(store.state.user.email);
      const isEditing = ref(false);
  
      const backToPreviousPage = () => {
        // TODO: 返回上一界面的逻辑
        router.back();  // 返回前一页

      };
  
      const startEditing = () => {
        editingUsername.value = username.value;
        editingEmail.value = email.value;
        isEditing.value = true;
      };
  
      const submitForm = async () => {
        const form = { username: editingUsername.value, password: password.value, email: editingEmail.value };
        // 创建一个新的对象，只包含用户修改的字段
        const updatedFields = Object.entries(form).reduce((obj, [key, value]) => {
          // 如果用户已经输入了新的值，那么添加这个字段到新的对象中
          if (value) {
            obj[key] = value;
          }
          return obj;
        }, {});
  
        // 确保至少有一个字段被修改
        if (!Object.keys(updatedFields).length) {
          ElMessage.error('请至少修改一个字段');
          return;
        }
  
        // TODO: 调用后端的更新用户接口，传递formData，并处理返回的数据
        try {
          const response = await fetch(`http://localhost:8000/users/${store.state.user.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedFields),
          });
          console.log('updatedFields' + JSON.stringify(updatedFields))
          if (!response.ok) {
                const errorData = await response.json();
                console.error(errorData);
                throw new Error('Network response was not ok');
            }
          const result = await response.json();
  
          // 使用返回的状态码来判断请求是否成功
          if (response.status === 200) {
            ElMessage.success('个人信息修改成功');
            // 使用返回的数据来更新 Vuex 状态
            store.commit('updateUser', result);
            console.log(JSON.stringify(result, null, 2))
            console.log(store.state.user.username)
            console.log(store.state.user.email)
            console.log(store.state.user.password)
            username.value = editingUsername.value;
            email.value = editingEmail.value;
          } else {
            ElMessage.error('个人信息修改失败');
          }
        } catch (error) {
          console.error('Error:', error);
          ElMessage.error('用户名或邮箱不唯一!');
        } finally {
          isEditing.value = false;
        }
      };
  
      return { backToPreviousPage, username, password, email, editingUsername, editingEmail, submitForm, isEditing, startEditing };
    },
  };
  </script>
  
  <style scoped>
  .container {
    padding: 50px;
  }
  
  .box-card {
    margin-bottom: 20px;
  }
  
  .back-btn {
    margin-bottom: 20px;
  }
  </style>
  