<script setup>
import { ref, onMounted} from "vue"

const matches = ref([])
const loading = ref(false)
const erros = ref(null)

const fetchMatches = async() => {
    loading.value = true
    error.value = null
    try{
        const response = await fetch('http://localhost:8000/api/matches/')
        if (!response.ok){
            throw new Error('Failed to fetch matched profiles')
        }
        
        const data = await response.json()
        matches.value = data
    } catch (err){
        error.value - err.message
    } finally {
        loading.value = false
    }
}
onMounted(fetchMatches)


</script>

<template>
    <div class="body">
        <h1>Your Matches</h1>
        <ul v-for="match in matches" :key="match_id">
            <div class="matchedProfile">
                <img :src="match.profile_picture" :alt="match.full_name" class="avatar">
                <div class="info">
                    <h3>{{ match.full_name }}, {{ match.age }}</h3>
                    <p>{{ matches.bio }}</p>
                    <button> Message </button>
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