<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const Password = ref('')
const router = useRouter()
const auth = inject("auth");

async function login() {
  const response = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email.value, password: Password.value })
  })
  const data = await response.json()
  if (response.ok) {
    auth.login(data.user)
    router.push('/dashboard')
  } else {
    alert(data.message)
  }
}
</script>

<template>
    <div class="container">
        <h1>Log In</h1>
        <div class="loginCard">
            <label>Email</label> 
            <input v-model="email"/> <br>
            <label>Password</label> 
            <input type="password" v-model="Password"/>
            <button class="login" @click="login">Log in</button>
            <p> Don't have an account?<router-link to="/register"> Sign up here</router-link></p>
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
.loginCard{
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