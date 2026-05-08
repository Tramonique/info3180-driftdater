<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'

const full_name = ref('')
const age = ref('')
const gender = ref('')
const bio = ref('')
const location = ref('')
const interests = ref('')
const photo = ref(null)
const router = useRouter()
const auth = inject('auth')

function fileUpload(event) {
    photo.value = event.target.files[0]
}

const userId = auth.user.value?.id

async function editProfile() {
    if (!userId) {
        router.push('/login')
        return
    }

    const updateData = {}

    if (full_name.value.trim())
        updateData.full_name = full_name.value
    if (age.value)
        updateData.age = age.value
    if (bio.value.trim())
        updateData.bio = bio.value
    if (location.value)
        updateData.location = location.value
    if (interests.value)
        updateData.interests = interests.value
    if (gender.value)
        updateData.gender = gender.value
    if(Object.keys(updateData).length === 0){
        buildErrorMessage.value = 'Need to update a field'
        return
    }

    try{
        const response = await fetch(`/api/profiles/${user_id}`, {
            method: 'PUT',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        })

        const data = await response.json()
        if (!response.ok) {
            alert(data.message)
            return
        }

        if (photo.value && user_id) {
            const formData = new FormData()
            formData.append('photo', photo.value)

            const responsePicture = await fetch(`/api/profiles/${user_id}/photo`, {
                method: 'POST',
                credentials: 'include',
                body: formData
            })

            const dataPicture = await responsePicture.json()

            if (!responsePicture.ok) {
                alert(dataPicture.message)
                return
            }
        }

        router.push('/dashboard')
    } catch (error) {
        console.error(error)
        alert('Something went wrong')
    }
}
</script>

<template>
    <div class="body">
        <h1>Create Profile</h1>
        <div class="profileCard">
            <div class="labelValue"><label><strong>Full Name</strong></label> <input v-model="full_name" /></div>
            <div class="labelValue"><label><strong>Age</strong></label> <input type="number" v-model.number="age" /></div>
            <div class="labelValue"><label><strong>Gender</strong></label> 
                <select v-model="gender">
                    <option value="Female">Female</option>
                    <option value="Male">Male</option>
                    <option value="Non-binary">Non-binary</option>
                    <option value="Other">Other</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                </select>
            </div>
            <div class="labelValue"><label><strong>Occupation</strong></label> <input v-model="bio" /></div>
            <div class="labelValue"><label><strong>Location</strong></label> <input v-model="location" /></div>
            <div class="labelValue"><label><strong>Interests</strong></label> <textarea v-model="interests"></textarea></div>
            <div class="labelValue"><label><strong>Picture of Yourself</strong></label> <input type="file" @change="fileUpload" /></div>
            <button class="create" @click="editProfile">Edit Profile</button>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.body {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    min-height: 100vh;
}

.profileCard {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 50%;
    max-width: 800px;
    min-width: 500px;
    gap: 50px;
    background: #fff;
    padding: 40px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
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

.labelValue{
    display: flex;
    flex-direction: row;
    gap: 20px;
}

input, textarea, select {
    width: 40ch;
}

/*Tablet layout*/
@media (max-width: 1024px) {
    h1 { font-size: 3rem; }

    .profileCard {
        width: 65%;
        min-width: unset;
        padding: 35px;
    }

    label { font-size: 1.6rem; }

    button { width: 60%; }
}

/*Phone Layout */
@media (max-width: 600px) {
    .body {
      gap: 20px;
      padding: 15px;
    }

    h1 { font-size: 2.3rem; }

    .profileCard {
      width: 100%;
      border-radius: 8px;
    }

    label { font-size: 1.2rem; }

    input, textarea {
      padding: 5px;
      font-size: 0.95rem;
    }

    button {
      width: 100%;
      font-size: 1rem;
    }
}
</style>