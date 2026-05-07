<script setup>
import { ref, onMounted, computed } from 'vue'

const location = ref('')
const minimum_age = ref('')
const maximum_age = ref('')
const interests = ref('')

const profiles = ref([])
const loading = ref(false)
const error = ref(null)

const limitedProfiles = computed(() => {
    return profiles.value.slice(0, 10)
})

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

const searchProfiles = async () => {
    loading.value = true
    error.value = null
    try {
        const params = new URLSearchParams()
        if (location.value) params.append('location', location.value)
        if (minimum_age.value) params.append('age_min', minimum_age.value)
        if (maximum_age.value) params.append('age_max', maximum_age.value)
        if (interests.value) params.append('interests', interests.value)

        const response = await fetch(`/api/search?${params.toString()}`, {
            credentials: 'include'
        })
        if (!response.ok) throw new Error('Failed to search profiles')
        const data = await response.json()
        profiles.value = data.profiles
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

const resetFilters = () => {
    location.value = ''
    minimum_age.value = ''
    maximum_age.value = ''
    interests.value = ''
    fetchProfiles()
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

onMounted(fetchProfiles)
</script>

<template>
    <div class="body">
        <h1>Browse Potential Matches</h1>
        <div class="searchCard">
            <div class="specifications">
                <input v-model="location" placeholder="Filter by location...">
                <input type="number" v-model.number="minimum_age" placeholder="Minimum age...">
                <input type="number" v-model.number="maximum_age" placeholder="Maximum age...">
                <input v-model="interests" placeholder="Filter by interest...">
            </div>
            <button class="showResults" @click="searchProfiles">Search</button>
            <button class="reset" @click="resetFilters">Reset Filters</button>
        </div>

        <div class="matches">
            <p v-if="loading">Loading...</p>
            <p v-if="error">{{ error }}</p>
            <p v-if="!loading && profiles.length === 0">No profiles found!</p>
            <ul v-if="!loading && !error">
                <li v-for="profile in limitedProfiles" :key="profile.user_id">
                    <div class="profile">
                        <img :src="profile.profile_picture" :alt="profile.full_name" class="avatar">
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
        </div>
    </div>
</template>

<style lang="scss" scoped>
.body {
    padding: 30px;

    .searchCard, .profile {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        background: #fff;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    .specifications {
        display: flex;
        gap: 20px;

        input {
            padding: 8px 14px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-weight: 500;
            color: #333;
        }
    }

    button {
        padding: 8px 14px;
        border: none;
        border-radius: 6px;
        width: 50%;
        cursor: pointer;
        font-weight: 500;
        color: white;

        &.showResults { background-color: #9622e3; }
        &.reset { background-color: #393939; }
        &.likeBtn { background-color: #59D972; }
        &.dislikeBtn { background-color: #c93232; }
    }

    .avatar {
        width: 80px;
        height: 80px;
        border-radius: 10px;
        object-fit: cover;
    }

    ul { list-style: none; padding: 0; margin: 0; }

    .matches { display: flex; flex-direction: column; gap: 15px; }
    .info { flex: 1; display: flex; flex-direction: column; gap: 5px; }
    .actions { display: flex; gap: 10px; }
    .matchScore { color: #6c7ae0; font-weight: 500; }
}

//Tablet layout styling (600px - 1024px)
@media (max-width: 1024px) {

    .body { padding: 15px; }

    .searchCard, .profile {
        gap: 15px;
        padding: 12px;
    }

    .avatar {
        width: 70px;
        height: 70px;
    }

    button {
        padding: 8px 12px;
        font-size: 14px;
    }

    label { font-size: 1.6rem; }
}

//Phone layout styling (300px - 600px)
@media (max-width: 600px) {

    .body {padding: 10px; }

    .searchCard, .profile {
        flex-direction: column;
        align-items: flex-start;
        text-align: left;
        gap: 12px;
        padding: 12px;
    }

    .avatar {
        width: 100%;
        max-width: 250px;
        height: auto;
        align-self: center;
    }

    .info { width: 100%; }
    .actions {
        width: 100%;
        flex-direction: column;
    }

    button {
        width: 100%;
        padding: 10px;
        font-size: 15px;
    }

    h1, h2, h3, label { font-size: 1.2rem; }

    input {
      padding: 10px;
      font-size: 0.95rem;
    }

    p { font-size: 0.95rem; }
}
</style>