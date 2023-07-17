<template>
  <div>
    <h1>Test Chat</h1>

    <!-- User Registration -->
    <div>
      <h2>Register</h2>
      <input v-model="registerUser.username" placeholder="username" />
      <input v-model="registerUser.email" placeholder="email" />
      <input v-model="registerUser.password" placeholder="password" type="password" />
      <button @click="register">Register</button>
    </div>

    <!-- User Login -->
    <div>
      <h2>Login</h2>
      <input v-model="loginUser.username" placeholder="username" />
      <input v-model="loginUser.password" placeholder="password" type="password" />
      <button @click="login">Login</button>
    </div>

    <!-- Add Friend -->
    <div>
      <h2>Add Friend</h2>
      <input v-model="friendId" placeholder="friend's ID" />
      <button @click="addFriend">Add Friend</button>
    </div>

    <!-- Send Message -->
    <div>
      <h2>Send Message</h2>
      <input v-model="friendId" placeholder="friend's ID" />
      <input v-model="message" placeholder="message" />
      <button @click="sendMessage">Send Message</button>
    </div>

     <!-- Receive Message -->
     <div>
      <h2>Receive Message</h2>
      <text>{{ receiveMessage }}</text>
    </div>

  </div>
</template>

<script>
import { ref, reactive, computed } from "vue";
import axios from 'axios';

export default {
  name: 'HelloWorld',
  setup() {
    const registerUser = reactive({
      username: '',
      email: '',
      password: '',
    });
    
    const loginUser = reactive({
      username: '',
      password: '',
    });

    const friendId = ref("");
    const message = ref("");
    const receiveMessage = ref("")
    let socket = null;

    const user = computed(() => {
      // Get user from localStorage and parse it
      const storedUser = localStorage.getItem('user');
      return storedUser ? JSON.parse(storedUser) : null;
    });

    const register = async () => {
      try {
        const response = await axios.post("http://localhost:8000/users/", {
          username: registerUser.username,
          email: registerUser.email,
          password: registerUser.password,
        });
        console.log(response.data);
        connectSocket(response.data.id);
      } catch (error) {
        console.error(error);
      }
    };

    const login = async () => {
      try {
        const response = await axios.post("http://localhost:8000/login", {
          username: loginUser.username,
          password: loginUser.password,
        });
        localStorage.setItem('user', JSON.stringify(response.data));
        connectSocket(response.data.id);
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
      } catch (error) {
        console.error(error);
      }
    };

    const connectSocket = (userId) => {
      socket = new WebSocket("ws://localhost:8000/ws/" + userId);

      socket.onopen = () => {
        console.log("success!")
      }
      socket.onmessage = (event) => {
        console.log("Message from server: ", event.data);
        receiveMessage.value += event.data;
      };
      socket.onclose = (event) => {
      console.log("Socket closed", event);
};

    };

    const sendMessage = () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
          receiver_id: friendId.value,
          content: message.value
        }));
        message.value = "";
      }
    };

    return {
      registerUser,
      loginUser,
      friendId,
      message,
      receiveMessage,
      register,
      login,
      addFriend,
      sendMessage,
    };
  },
};
</script>
