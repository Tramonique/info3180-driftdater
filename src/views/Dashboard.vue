<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const current_User = ref(null) //Holds the current users profile information
const profiles = ref([]) //Holds all the potential matching profiles
const loading = ref(false)
const error = ref(null)
const router = useRouter()

/*Getting and handling current user profile*/ 
const currentProfile = async() => {
    loading.value = true
    error.value = null
    try{
        const response = await fetch('/api/profiles/<int:user_id>')
        if (!response.ok){
            throw new Error('Failed to fetch current user profile')
        }
        
        const data = await response.json()
        current_User.value = data
    } catch (err){
        error.value = err.message
    } finally {
        loading.value = false
    }
}

/*Getting and handling of potential profiles that best match with current user. Data is fetched from views.py discover route*/ 
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

//Edit Profile


onMounted(() => {
    currentProfile()
    fetchProfiles()
})
</script>

<template>
    <div class="body">
        <p v-if="loading">Loading...</p>
        <p v-if="error">{{ error }}</p>

        <!--Current User Display Section-->
        <div class="userProfile" v-if="!loading && !error">
            <img :src="current_User.profile_picture" :alt="current_User.full_name">
            <div class="info">
                <h2 class="userTitle">Welcome, {{current_User.full_name}}!</h2>
                <p class="Labels"><strong>Age: </strong> {{ current_User.age }}</p> 
                <p class="Labels"><strong>Location: </strong> {{ current_User.location }}</p>
                <p class="Labels"><strong>Bio: </strong> {{ current_User.bio }}</p>
                <button class="editBtn" @click="editProfile"> Edit Profile</button>
            </div>
        </div>
        
        <!--Possible Matching Profiles Section-->
        <h1> Browse Potential Matches</h1>
        <div class="matches">
            <ul v-if="!loading && !error"> 
                <li v-for="(profile, index) in profiles" v-if="index < 10" :key="profile.user_id">
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

<style scoped lang="scss">
$primary: #6c7ae0;
$like: #59D972;
$dislike: #c93232;

.body {
  padding: 20px;
}

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

.avatar {
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

  &.editBtn {
    background-color: $primary;
    margin-top: 10px;
    width: fit-content;
  }

  &.likeBtn {
    background-color: $like;
  }

  &.dislikeBtn {
    background-color: $dislike;
  }
}

.actions {
  display: flex;
  gap: 10px;
}

.matches {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.userTitle {
  margin: 10px 0;
}

.matchScore {
  color: $primary;
  font-weight: 500;
}
</style>