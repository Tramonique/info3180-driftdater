<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Drift Dater</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <!--Navigation Headers-->
            <li class="nav-item">
              <RouterLink to="/" class="nav-link" exact-active-class="active">Home</RouterLink>
            </li>

            <template v-if="auth.isAuthenticated">
              <li class="nav-item">
                <RouterLink to="/about" class="nav-link" exact-active-class="active">About</RouterLink>
              </li>
              <li class="nav-item"> <!--Log in navigation heading-->
                <RouterLink to="/login" class="nav-link" exact-active-class="active">Log In</RouterLink>
              </li>
            </template>

            <template v-else>
              <li class="nav-item"> <!--Dashboard navigation heading-->
                <RouterLink to="/dashboard" class="nav-link" exact-active-class="active">Dashboard</RouterLink>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { inject } from "vue";

const auth = inject("auth");
console.log("Auth State: ", auth)
</script>

<style>
.nav-link.router-link-active{
  color:aliceblue;
  background-color: #007bff;
}
</style>