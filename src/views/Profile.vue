<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const full_name = ref('')
const age = ref('')
const bio = ref('')
const location = ref('')
const interests = ref('')
const router = useRouter()

async function createProfile() {
  const response = await fetch('/api/profiles', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ full_name: full_name.value, age: age.value, bio: bio.value, location: location.value, interests: interests.value })
  })
  const data = await response.json()
  if (response.ok) {
    router.push('/login')
  } else {
    alert(data.message)
  }
}
</script>

<template>
    <div class="body">
        <h1>Create Profile</h1>
        <div class="profileCard">
            <div class="labelValue"><label><strong>Full Name</strong></label> <input v-model="full_name"/></div>
            <div class="labelValue"><label><strong>Date of Birth</strong></label> <input type="date" v-model="age"/></div>
            <div class="labelValue"><label><strong>Occupation</strong></label> <input v-model="bio"/></div>
            <div class="labelValue"><label><strong>Address</strong></label> <input v-model="location"/></div>
            <div class="labelValue"><label><strong>Interests</strong></label> <textarea v-model="interests"></textarea></div>
            <button class="create" @click="createProfile">Create Profile</button>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.body{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.profileCard{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 50%;
    height: 100vh;
    gap: 40px;
    background: #fff;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

button {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  color: white;
  background-color: #bd0084;
}

input, textarea{
    width: 40ch;
}
</style>