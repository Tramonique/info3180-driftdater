<script setup>
import { ref, onMounted} from "vue"
import { useRouter } from "vue-router"

const matches = ref([])
const loading = ref(false)
const error = ref(null)
const router = useRouter()

//Loading of all matched profiles
const fetchMatches = async() => {
    loading.value = true
    error.value = null
    try{
        const response = await fetch('/api/matches/')
        if (!response.ok){
            throw new Error('Failed to fetch matched profiles')
        }
        
        const data = await response.json()
        matches.value = data.matches
    } catch (err){
        error.value - err.message
    } finally {
        loading.value = false
    }
}

//Message navigation
const goToMessages = (match) => {
    router.push({
        name: 'message',
        params:{
            matchID: match.match_id,
            receiverID: match.user_id
        }
    })
}
onMounted(fetchMatches)


</script>

<template>
    <div class="body">
        <h1>Your Matches</h1>
        <p v-if="loading">Loading...</p>
        <p v-if="error">{{ error }}</p>
        <ul v-for="match in matches" :key="match_id">
            <div class="matchedProfile">
                <img :src="match.profile_picture" :alt="match.full_name" class="avatar"> <!--if src doesnt load do "/uploads/${match.profile_picture}"-->
                <div class="info">
                    <h3>{{ match.full_name }}, {{ match.age }}</h3>
                    <p>{{ matches.bio }}</p>
                    <button @click="goToMessages"> Message </button>
                </div>

            </div>
        </ul>
    </div>
</template>

<style lang="scss" scoped>
.body{
    padding: 20px
}

.matchedProfile{
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
  background-color: #60BF00;
}
</style>