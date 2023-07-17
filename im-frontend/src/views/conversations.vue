<template>
    <div class="friends">
      <div class="friend-list">
        <div v-if="friends.length">
          <router-link v-for="(friend, key) in friends" :key="key" :to="`/privatechat/${friend.id}`">
            <div class="friend">
              <div class="friend-name">{{ friend.username }}</div>
            </div>
          </router-link>
        </div>
        <div v-else class="no-friends">- 当前没有好友 -</div>
      </div>
      <div class="chat">
        <router-view/>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import { useStore } from 'vuex'
  import axios from 'axios'
  
  export default {
    name: 'userFriends',
    setup() {
      const friends = ref([])
      const store = useStore()
  
      const fetchFriends = async () => {
        //const userId = JSON.parse(localStorage.getItem('user')).id
        const userId = store.state.user.id  // get user from store
        const response = await axios.get(`http://localhost:8000/users/${userId}/friends`)
        friends.value = response.data
      }
  
      onMounted(fetchFriends)
  
      return {
        friends,
      }
    },
  }
  </script>
  
  
  <style scoped>
  .friends {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    color: #333333;
  }

  .friend-list {
    width: 220px;
  }

  .friend-list-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    background-color: white;
    border-right: #dbd6d6 1px solid;
  }

  .friend-list-content {
    flex: 1;
    overflow-y: auto;
    padding: 10px 0;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  .friend-list-content::-webkit-scrollbar {
    display: none;
  }

  .no-friend {
    text-align: center;
    color: #666666;
  }

  .friend {
    display: flex;
    padding: 10px 5px;
    cursor: pointer;
  }

  .unread-count {
    position: absolute;
    top: -10px;
    left: 30px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    color: white;
    background: #d02129;
  }

  .unread-count .unread {
    display: block;
    font-size: 12px;
    text-align: center;
    line-height: 18px;
  }

  .friend-message {
    flex: 1;
    padding-left: 5px;
    display: flex;
    width: 160px;
    flex-direction: column;
    justify-content: space-around;
  }

  .friend-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    text-align: right;
  }

  .friend-name {
    font-size: 12px;
    font-weight: 500;
  }

  .friend-time {
    width: 75px;
    color: #B9B9B9;
    display: flex;
    flex-direction: column;
  }

  .friend-bottom {
    display: flex;
    color: #666666;
  }

  .friend-content {
    display: flex;
    width: 160px;
    color: #b3b3b3;
  }

  .friend-content .text {
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    white-space: nowrap;
    word-break: break-all;
  }

  .friend-bottom .unread-text {
    color: #d02129;
    width: 35px !important;
  }

  .friend .avatar {
    width: 40px;
    height: 40px;
    position: relative;
  }

  .conversation .avatar img {
    width: 100%;
    border-radius: 10%;
  }

  .router-link-active {
    background: #eeeeee;
  }

  .action-box {
    width: 100px;
    height: 60px;
    background: #ffffff;
    border: 1px solid #cccccc;
    position: fixed;
    z-index: 100;
    border-radius: 5px;
  }

  .action-box .action-item {
    padding-left: 15px;
    line-height: 30px;
    font-size: 13px;
    color: #262628;
    cursor: pointer;
  }

  .action-box .action-item:hover {
    background: #dddddd;
  }

  .chat {
    flex: 1;
    display: flex;
  }

</style>