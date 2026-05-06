<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const Password = ref('')
const router = useRouter()

async function register() {
  const response = await fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email.value, password: Password.value })
  })
  const data = await response.json()
  if (response.ok) {
    router.push('/createprofile')
  } else {
    alert(data.message)
  }
}
</script>

<template>
    <div class="container">
        <h1>Sign up</h1>
        <div class="signupCard">
            <label>Email</label> 
            <input v-model="email"/> <br>
            <label>Password</label> 
            <input type="password" v-model="Password"/>
            <button class="login" @click="register">Sign up</button>
        </div>
    </div>
</template>

<style scoped>
.container{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 30px;
    height: 100vh;
}
h1{
    font-size: 4rem;
}
.signupCard{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    background-color: #ffffff;
    border: 1px groove #000000;
    border-radius: 5px;
    width: 40%;
    height: 50%;
    padding: 20px;
}
button{
    width: 40%;
    margin-top: 2%;
    background: linear-gradient(to right, #E3A3A3, #FFF1A8)
}
label{
    font-size: 2rem;
}
</style>