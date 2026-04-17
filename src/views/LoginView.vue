<script setup>
import {ref} from 'vue'

/*const email = ref('')
const Password = ref('')
const register = ref('Sign up here')*/
</script>

<template>
    <div class="container">
        <h1>Log In</h1>
        <div class="loginCard">
            <label>Email</label> 
            <input v-model="email"/> <br>
            <label>Password</label> 
            <input type="password" v-model="Password"/>
            <button class="login">Log in</button>
            <!--Redirect to register page if user does not have an account-->
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