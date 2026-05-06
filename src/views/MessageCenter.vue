<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const matchId = ref(route.params.matchID)        // current conversation
const receiverId = ref(route.params.receiverID)     // user being chat with
const messages = ref([])
const newMessage = ref('')
const loading = ref(false)

//Fetch messages
async function fetchMessages() {
  if (!matchId.value) return

  try {
    const res = await fetch(`/api/matches/${matchId.value}/messages`)
    const data = await res.json()

    if (res.ok) {
      messages.value = data.messages
    }
  } catch (err) {
    console.error(err)
  }
}

//Send message
async function sendMessage() {
  if (!newMessage.value.trim()) return

  try {
    const res = await fetch('/api/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        receiver_id: receiverId.value,
        content: newMessage.value
      })
    })

    const data = await res.json()

    if (res.ok) {
      newMessage.value = ''
      fetchMessages() // refresh
    } else {
      alert(data.message)
    }
  } catch (err) {
    console.error(err)
  }
}

//Polling for "real-time"
onMounted(() => {
  fetchMessages()

  setInterval(() => {
    fetchMessages()
  }, 3000) 
})
</script>

<template>
  <div class="body">
    <div class="chatContainer">
      <h2>Messages</h2>
      <div class="chatBox">
        <div v-for="msg in messages" :key="msg.id" :class="['message', msg.sender_id === receiverId ? 'received' : 'sent']">
          <div class="content">{{ msg.content }}</div>
          <div class="time">
            {{ new Date(msg.created_at).toLocaleTimeString() }}
          </div>
        </div>
      </div>

      <div class="inputArea">
        <input v-model="newMessage" placeholder="Type a message..." @keyup.enter="sendMessage"/>
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.chat {
  min-height: 100vh;
  background: linear-gradient(to right, #6a0dad, #9b59b6);
  display: flex;
  justify-content: center;
  align-items: center;

  .chatBox {
    width: 70%;
    background: white;
    border-radius: 12px;
    padding: 1rem;

    .messages {
      height: 300px;
      overflow-y: auto;
      margin-bottom: 1rem;

      .message {
        max-width: 60%;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;

        &.sent {
          background: #6a0dad;
          color: white;
          margin-left: auto;
        }

        &.received {
          background: #eee;
        }

        .time {
          font-size: 0.7rem;
          margin-top: 4px;
        }
      }
    }

    .inputArea {
      display: flex;
      gap: 10px;

      input {
        flex: 1;
        padding: 10px;
      }

      button {
        background: #6a0dad;
        color: white;
        border: none;
        padding: 10px;
      }
    }
  }
}
</style>