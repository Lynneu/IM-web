<template>
  <el-container direction="vertical">
    <el-header style="text-align: right;">
      <el-dropdown>
        <el-button class="circular-button">
        <span v-if="user" style="text-align: center; font-size: large;">
          {{ user.username.slice(-1) }}
          
        </span>
      </el-button>
        <template v-slot:dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="changeinfo">个人信息
              <!-- <router-link :to="{ name: 'userInfo' }">个人信息</router-link> -->
            </el-dropdown-item>
            <el-dropdown-item @click="backtoLogin">注销</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="6">
          <h2>添加好友</h2>
          <el-card class="box-card">
            <el-form @submit.prevent="addFriend">
              <el-form-item label="用户名">
                <el-input v-model="friendName" placeholder="请输入用户名"></el-input>
              </el-form-item>
              <el-button type="primary" native-type="submit">添加好友</el-button>
            </el-form>
          </el-card>
        </el-col>
        <el-col :span="18">
          <h2>好友列表</h2>
          <el-card class="box-card">
            <el-table :data="friends" style="width: 100%" @row-click="goToChat">
              <el-table-column prop="username" label="用户名"></el-table-column>
              <el-table-column
                label="状态"
              >
                <template #default="scope">
                  <el-tag :type="scope.row.online ? 'success' : 'info'">{{ scope.row.online ? '在线' : '离线' }}</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>


<script>
import { ref, reactive, computed, onMounted } from "vue";
import axios from 'axios';
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'HelloWorld',
  setup() {
    const router = useRouter()
    const store = useStore()
    const user = computed(() => store.state.user)  // get user from store
    const socket = computed(() => store.state.websocket) // get websocket from store
    const friends = ref([]);
    const registerUser = reactive({
      username: '',
      email: '',
      password: '',
    });  
    const friendId = ref("");
    const friendName = ref("")
    const message = ref("");
    const receiveMessage = ref([])

    const goToChat = (row) => {
      router.push({
        name: 'privatechat', 
        params: { 
          friendId: row.id,
          friendName: row.username 
        }
      });
    };

    const fetchFriends = async () => {
      const userId = user.value.id
      console.log('yes')
      console.log(user.value)
      console.log(userId)
      const response = await axios.get(`http://localhost:8000/users/${userId}/friends`)
      friends.value = response.data
    }
    
    const backtoLogin = () => {
      console.log('logout')
      console.log(user.value)
      socket.value.close()
      store.commit('clearUserState');  // 调用 mutation 来清除用户状态
      console.log(user.value)
      
      router.push({ name: 'UserLogin' });
    }

    const changeinfo = () => {
      router.push({ name: 'userInfo' });
    }

    onMounted(async () => {
      await fetchFriends();
      if (socket.value) {
        socket.value.onmessage = (event) => {
          console.log("Message from server: ", event.data);
          const message = JSON.parse(event.data);

          switch (message.type) {
            case 'status': {
              // 更新好友的在线状态
              const friend = friends.value.find(friend => friend.id === message.content.user_id);
              if (friend) {
                friend.online = message.content.status === 'online';
              }
              break;
            }
            case 'text':
              // Handle received messages as before
              receiveMessage.value.push(event.data)
              break;
            default:
              console.log("Unknown message type:", message.type);
          }
        };
  
        socket.value.onclose = (event) => {
          console.log("Socket closed", event);
        };
      }
    });

    const register = async () => {
      try {
        const response = await axios.post("http://127.0.0.1:8000/users/", {
          username: registerUser.username,
          email: registerUser.email,
          password: registerUser.password,
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    const addFriend = async () => {
      try {
        if (!user.value) {
          throw new Error('User not logged in');
        }
        await axios.put(`http://localhost:8000/users/${user.value.id}/friends/${friendName.value}`);
        alert('Friend added successfully');
        await fetchFriends(); 
      } catch (error) {
        console.error(error);
      }
    };

    const sendMessage = () => {
      if (message.value.trim() !== '' && socket.value && socket.value.readyState === WebSocket.OPEN) {
        console.log(message.value);
        socket.value.send(JSON.stringify({
          receiver_id: friendId.value,
          content: message.value
        }));
        message.value = "";
      }
    };

    return {
      friends,
      registerUser,
      friendId,
      friendName,
      message,
      receiveMessage,
      user,  // return user
      socket, // return websocket
      register,
      addFriend,
      sendMessage,
      backtoLogin,
      changeinfo,
      goToChat
    };
  },
};
</script>

  
  <style scoped>
/* .section {
  margin-bottom: 2rem;
}

.friend-item, .message-item {
  border: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1rem;
}

.status-online {
  color: green;
}

.status-offline {
  color: red;
} */

.el-header {
  background-color: #337ecc;
  color: #333;
  line-height: 60px;
}

.friend-item {
  margin-bottom: 15px;
}

.circular-button {
  border-radius: 50%; /* 设置圆角为 50%，使按钮形状变为圆形 */
  width: 50px; /* 可根据需要修改 */
  height: 50px; /* 可根据需要修改 */
  display: flex; /* 用于设置按钮中的元素居中 */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  margin: 5px;
}
</style>