<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'

const auth = inject('auth')
const current_User = ref(null)
const profiles = ref([])
const loading = ref(false)
const error = ref(null)
const router = useRouter()

const currentProfile = async () => {
    loading.value = true
    error.value = null
    try {
        const userId = auth.user.value?.id
        if (!userId) {
            router.push('/login')
            return
        }
        const response = await fetch(`/api/profiles/${userId}`, {
            credentials: 'include'
        })
        if (!response.ok) throw new Error('Failed to fetch current user profile')
        const data = await response.json()
        current_User.value = data
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

const fetchProfiles = async () => {
    loading.value = true
    error.value = null
    try {
        const response = await fetch('/api/discover', {
            credentials: 'include'
        })
        if (!response.ok) throw new Error('Failed to fetch profiles')
        const data = await response.json()
        profiles.value = data.profiles
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

const likeUser = async (userID) => {
    try {
        const response = await fetch(`/api/profiles/${userID}/like`, {
            method: 'POST',
            credentials: 'include'
        })
        const data = await response.json()
        if (!response.ok) { alert(data.message); return }
        if (data.matched) alert("It's a match!")
        profiles.value = profiles.value.filter(p => p.user_id !== userID)
    } catch (err) { console.error(err) }
}

const passUser = async (userID) => {
    try {
        const response = await fetch(`/api/profiles/${userID}/pass`, {
            method: 'POST',
            credentials: 'include'
        })
        const data = await response.json()
        if (!response.ok) { alert(data.message); return }
        profiles.value = profiles.value.filter(p => p.user_id !== userID)
    } catch (err) { console.error(err) }
}

onMounted(() => {
    currentProfile()
    fetchProfiles()
})
</script>

<template>
    <div class="body">
        <p v-if="loading">Loading...</p>
        <p v-if="error">{{ error }}</p>

        <div class="userProfile" v-if="!loading && !error && current_User">
            <img :src="current_User.profile_picture" :alt="current_User.full_name">
            <div class="info">
                <h2 class="userTitle">Welcome, {{ current_User.full_name }}!</h2>
                <p class="Labels"><strong>Age: </strong> {{ current_User.age }}</p>
                <p class="Labels"><strong>Location: </strong> {{ current_User.location }}</p>
                <p class="Labels"><strong>Bio: </strong> {{ current_User.bio }}</p>
            </div>
        </div>

        <h1>Browse Potential Matches</h1>
        <div class="matches">
            <ul v-if="!loading && !error">
                <li v-for="profile in profiles.slice(0, 10)" :key="profile.user_id">
                    <div class="profile">
                        <img :src="profile.profile_picture" :alt="profile.full_name">
                        <div class="info">
                            <h3>{{ profile.full_name }}, {{ profile.age }}</h3>
                            <p>{{ profile.interests }}</p>
                            <p class="matchScore">Match Score: {{ profile.match_score }}</p>
                        </div>
                        <div class="actions">
                            <button class="likeBtn" @click="likeUser(profile.user_id)">Like</button>
                            <button class="dislikeBtn" @click="passUser(profile.user_id)">Pass</button>
                        </div>
                    </div>
                </li>
            </ul>
            <p v-if="!loading && profiles.length === 0">No more profiles to show!</p>
        </div>
    </div>
</template>

<style scoped lang="scss">
$primary: #6c7ae0;
$like: #59D972;
$dislike: #c93232;

.body { padding: 20px; }

.userProfile, .profile {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #fff;
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 15px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

img {
  width: 80px;
  height: 80px;
  border-radius: 10px;
  object-fit: cover;
}

.info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

button {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  color: white;
  &.likeBtn { background-color: $like; }
  &.dislikeBtn { background-color: $dislike; }
}

.actions { display: flex; gap: 10px; }
.matches { display: flex; flex-direction: column; gap: 15px; }
ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 15px; }
.userTitle { margin: 10px 0; }
.matchScore { color: $primary; font-weight: 500; }
</style>