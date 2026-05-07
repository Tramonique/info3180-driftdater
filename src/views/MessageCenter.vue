<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const auth = inject('auth')
const matchId = ref(route.params.matchID)
const receiverId = ref(parseInt(route.params.receiverID))
const messages = ref([])
const newMessage = ref('')

async function fetchMessages() {
  if (!matchId.value) return
  try {
    const res = await fetch(`/api/matches/${matchId.value}/messages`, {
      credentials: 'include'
    })
    const data = await res.json()
    if (res.ok) messages.value = data.messages
  } catch (err) {
    console.error(err)
  }
}

async function sendMessage() {
  if (!newMessage.value.trim()) return
  try {
    const res = await fetch('/api/messages', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        receiver_id: receiverId.value,
        content: newMessage.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      newMessage.value = ''
      fetchMessages()
    } else {
      alert(data.message)
    }
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  fetchMessages()
  setInterval(fetchMessages, 3000)
})
</script>

<template>
  <div class="body">
    <div class="chatContainer">
      <h2>Messages</h2>
      <div class="chatBox">
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['message', msg.sender_id === auth.user.value?.id ? 'sent' : 'received']"
        >
          <div class="senderName">{{ msg.sender_id === auth.user.value?.id ? 'You' : 'Them' }}</div>
          <div class="content">{{ msg.content }}</div>
          <div class="time">{{ new Date(msg.created_at).toLocaleTimeString() }}</div>
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
.body {
  padding: 20px;
}

.chatContainer {
  max-width: 700px;
  margin: auto;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chatBox {
  height: 400px;
  overflow-y: auto;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 8px;
}

.message {
  max-width: 60%;
  padding: 10px;
  border-radius: 10px;

  &.sent {
    background: #6a0dad;
    color: white;
    margin-left: auto;
    text-align: right;
  }

  &.received {
    background: #eee;
    color: #333;
    margin-right: auto;
  }

  .senderName {
    font-size: 0.75rem;
    font-weight: bold;
    margin-bottom: 3px;
    opacity: 0.8;
  }

  .time {
    font-size: 0.7rem;
    margin-top: 4px;
    opacity: 0.7;
  }
}

.inputArea {
  display: flex;
  gap: 10px;

  input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
  }

  button {
    background: #6a0dad;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
  }
}
</style>