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
    credentials: 'include',
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
            <input v-model="email" /> <br>
            <label>Password</label>
            <input type="password" v-model="Password" />
            <button class="login" @click="login">Log in</button>
            <p>Don't have an account?<router-link to="/register"> Sign up here</router-link></p>
        </div>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 30px;
    height: 100vh;
}
h1 { font-size: 4rem; }
.loginCard {
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
button {
    width: 40%;
    margin-top: 2%;
    background: linear-gradient(to right, #E3A3A3, #FFF1A8)
}
label { font-size: 2rem; }

/*Tablet layout*/
@media (max-width: 1024px) {
    h1 { font-size: 3rem; }

    .loginCard {
        width: 65%;
        min-width: unset;
        padding: 35px 25px;
    }

    label { font-size: 1.6rem; }

    button { width: 60%; }
}

/*Phone Layout */
@media (max-width: 600px) {
    .container {
      gap: 20px;
      padding: 15px;
    }

    h1 { font-size: 2.3rem; }

    .loginCard {
      width: 100%;
      padding: 25px 20px;
      border-radius: 8px;
    }

    label { font-size: 1.2rem; }

    input {
      padding: 10px;
      font-size: 0.95rem;
    }

    button {
      width: 100%;
      font-size: 1rem;
    }

    p { font-size: 0.9rem; }
}
</style>