<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const full_name = ref('')
const age = ref('')
const bio = ref('')
const location = ref('')
const interests = ref('')
const photo = ref(null)
const router = useRouter()

function fileUpload(event){
  photo.value = event.target.files[0]
}

async function createProfile() {
  try{
    const response = await fetch('/api/profiles', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ full_name: full_name.value, age: age.value, bio: bio.value, location: location.value, interests: interests.value })
    })

    const data = await response.json()
    if (!response.ok) {
      alert(data.message)
      return
    }

    const user_id = data.user_id
  
    if(photo.value){
      const formData = new FormData()
      formData.append('photo', photo.value)

      const responsePicture = await fetch('/api/profiles/${user_id}/photo',{
        method: 'POST',
        body: formData
      })

      const dataPicture = await responsePicture.json()

      if (!responsePicture.ok){
        alert(dataPicture.message)
        return
      }
    }
    router.push('/login')
  } catch(error){
    console.error(error)
    alert('Something went wrong')
  }
}
</script>

<template>
    <div class="body">
        <h1>Create Profile</h1>
        <div class="profileCard">
            <div class="labelValue"><label><strong>Full Name</strong></label> <input v-model="full_name"/></div>
            <div class="labelValue"><label><strong>Date of Birth</strong></label> <input type="number" v-model.number="age"/></div>
            <div class="labelValue"><label><strong>Occupation</strong></label> <input v-model="bio"/></div>
            <div class="labelValue"><label><strong>Address</strong></label> <input v-model="location"/></div>
            <div class="labelValue"><label><strong>Interests</strong></label> <textarea v-model="interests"></textarea></div>
            <div class="labelValue"><label><strong>Picture of Yourself</strong></label> <input type="file" @change="fileUpload"/></div>
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