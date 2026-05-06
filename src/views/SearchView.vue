<script>
import { ref, onMounted, computed } from 'vue'

const location = ref('')
const minimum_age = ref('')
const maximum_age = ref('')
const interests = ref('')

const profiles = ref([]) //Holds all the potential matching profiles
const loading = ref(false)
const error = ref(null)

const limitedProfiles = computed(() => {
    return profiles.value.slice(0,10)
})

/*Getting all profiles. Data is fetched from views.py discover route*/ 
const fetchProfiles = async() => {
    loading.value = true
    error.value = null
    try{
        const response = await fetch('/api/discover/')
        if (!response.ok){
            throw new Error('Failed to fetch profiles')
        }
        
        const data = await response.json()
        profiles.value = data
    } catch (err){
        error.value - err.message
    } finally {
        loading.value = false
    }
}

//Search Filter
const searchProfiles = async() => {
    loading.value = true
    error.value = null
    try{
        const params = new URLSearchParams()
        if (location.value){
            params.append('location', location.value)
        }
        if (minimum_age.value){
            params.append('age_min', minimum_age.value)
        }
        if (maximum_age.value){
            params.append('age_max', maximum_age.value)
        }
        if (interests.value){
            params.append('interests', interests.value)
        }

        const response = await fetch('/api/search?{params.toString()}', {
            credentials: 'include' //suggested by AI
        })

        if (!response.ok){
            throw new Error('Failed to send profiles')
        }

        const data = await response.json()
        profiles.value = data.profiles
    } catch (err){
        error.value = err.message
    } finally {
        loading.value = false
    }
}

//Reset Filters
const resetFilters = () =>{
    location.value = ''
    minimum_age.value = null
    maximum_age.vale = null
    interests.value = ''

    fetchProfiles()
}


//Handling user like button
const likeUser = async(userID) => {
    try{
        const response = await fetch('/api/profiles/${userID}/like', {
            method: 'POST'
        })
        const data = await response.json()

        if (!response.ok){
            alert(data.message)
            return
        }
        if (data.matched){
            alert("It's a match")
        }

        profiles.value = profiles.value.filter(p => p.user_id !== userID)
    } catch (err){
        console.error(err)
    }
}

//Handling user pass button
const passUser = async(userID) => {
    try{
        const response = await fetch('/api/profiles/${userID}/pass', {
            method: 'POST'
        })
        const data = await response.json()

        if (!response.ok){
            alert(data.message)
            return
        }

        profiles.value = profiles.value.filter(p => p.user_id !== userID)
    } catch (err){
        console.error(err)
    }
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
            <button class="showResults" @click="searchProfiles"> Search </button>
            <button class="reset" @click="resetFilters"> Reset Filters </button>
        </div>

        <div class="matches">
            <p v-if="loading">Loading...</p>
            <p v-if="error">{{ error }}</p>

            <ul v-if="!loading && !error"> 
                <li v-for="profile in limitedProfiles" :key="profile.user_id">
                    <div class="profile">
                        <img :src="profile.profile_picture" :alt="profile.full_name">
                        <div class="info">
                            <h3>{{ profile.full_name }}, {{ profile.age }}</h3>
                            <p> {{ profile.interests }} </p>
                            <p class="matchScore">Match Score: {{ profile.match_score }}</p>
                        </div>
                        <div class="actions">
                            <button class="likeBtn" @click="likeUser(profile.user_id)">Like</button> <button class="dislikeBtn" @click="passUser(profile.user_id)">Pass</button>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.body{
    padding: 30px;

    .searchCard, .profile{
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

    .specifications{
        display: flex;
        gap: 20px;

        input{
            padding: 8px 14px;
            border: groove;
            border-radius: 6px;
            width: 50%;
            font-weight: 500;
            color: white;
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

        &.showResults{
            background-color: #9622e3;
        }

        &.reset{
            background-color: #393939;
        }

        &.likeBtn {
            background-color: #59D972;
        }

        &.dislikeBtn {
            background-color: #c93232;
        }
    }

    .matches {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .info {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .actions {
        display: flex;
        gap: 10px;
    }

    .matchScore {
        color: #6c7ae0;
        font-weight: 500;
    }
}
</style>