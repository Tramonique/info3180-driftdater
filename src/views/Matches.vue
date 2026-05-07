<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

const matches = ref([])
const loading = ref(false)
const error = ref(null)
const router = useRouter()

const fetchMatches = async () => {
    loading.value = true
    error.value = null
    try {
        const response = await fetch('/api/matches', {
            credentials: 'include'
        })
        if (!response.ok) {
            throw new Error('Failed to fetch matched profiles')
        }
        const data = await response.json()
        matches.value = data.matches
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

const goToMessages = (match) => {
    router.push({
        name: 'message',
        params: {
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
        <p v-if="!loading && matches.length === 0">No matches yet!</p>
        <ul>
            <li v-for="match in matches" :key="match.match_id">
                <div class="matchedProfile">
                    <img :src="match.profile_picture" :alt="match.full_name" class="avatar">
                    <div class="info">
                        <h3>{{ match.full_name }}, {{ match.age }}</h3>
                        <p>{{ match.bio }}</p>
                        <button @click="goToMessages(match)">Message</button>
                    </div>
                </div>
            </li>
        </ul>
    </div>
</template>

<style lang="scss" scoped>
.body {
    padding: 20px;

    ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .matchedProfile {
        display: flex;
        align-items: center;
        gap: 20px;
        background: #fff;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);

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
            button {
                padding: 8px 14px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 500;
                color: white;
                background-color: #60BF00;
                width: fit-content;
            }
        }
    }
}

//Tablet layout styling (600px - 1024px)
@media (max-width: 1024px) {

  .body { padding: 15px; }

  .matchedProfile{
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
}

//Phone layout styling (300px - 600px)
@media (max-width: 600px) {

  .body {padding: 10px; }

  .matchedProfile {
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

  button {
    width: 100%;
    padding: 10px;
    font-size: 15px;
  }

  h1, h2, h3 { font-size: 1.2rem; }

  p { font-size: 0.95rem; }
}
</style>