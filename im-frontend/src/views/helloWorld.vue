<template>
    <div>
      <h1>Test Chat</h1>
    
      <!-- Add Friend -->
      <div class="section">
        <h2>添加好友</h2>
        <input v-model="friendId" placeholder="friend's ID" />
        <button @click="addFriend">Add Friend</button>
      </div>
  
       <!-- Friends List -->
       <div class="section">
        <h2>好友列表</h2>
        <div v-if="friends.length">
          <div v-for="(friend, key) in friends" :key="key" class="friend-item">
            <router-link 
              :to="{
                name: 'privatechat', 
                params: { 
                  friendId: friend.id,
                  friendName: friend.username 
                }
              }"
            >
            <div>
              {{ friend.username }}
              <span v-if="friend.online == true" class="status-online">[在线]</span>
              <span v-if="friend.online == false" class="status-offline">[离线]</span>
            </div>
        </router-link>
          </div>
        </div>
        <div v-else>- No Friends -</div>
      </div>
  
    </div>
</template>

  
<script>
import { ref, reactive, computed, onMounted } from "vue";
import axios from 'axios';
import { useStore } from 'vuex'

export default {
  name: 'HelloWorld',
  setup() {
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
    const message = ref("");
    const receiveMessage = ref([])

    const fetchFriends = async () => {
      const userId = user.value.id
      console.log('yes')
      console.log(user.value)
      console.log(userId)
      const response = await axios.get(`http://localhost:8000/users/${userId}/friends`)
      friends.value = response.data
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
        const response = await axios.post("http://localhost:8000/users/", {
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
        await axios.put(`http://localhost:8000/users/${user.value.id}/friends/${friendId.value}`);
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
      message,
      receiveMessage,
      user,  // return user
      socket, // return websocket
      register,
      addFriend,
      sendMessage,
    };
  },
};
</script>

  
  <style scoped>
.section {
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
}
</style>