<script setup>
import { RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import { ref, provide, onMounted } from "vue";

const isAuthenticated = ref(false);
const user = ref(null);

provide("auth", {
  isAuthenticated, user,
  login: (userData) => {
    isAuthenticated.value = true;
    user.value = userData;
  },
  logout: () => {
    isAuthenticated.value = false;
    user.value = null;
  }
});

onMounted(async () => {
  try {
    const response = await fetch('/api/check-auth', { credentials: 'include' })
    const data = await response.json()
    if (data.authenticated) {
      isAuthenticated.value = true
      user.value = data.user
    }
  } catch (e) {
    console.error('Auth check failed', e)
  }
})
</script>

<template>
  <AppHeader />
  <main>
    <RouterView />
  </main>
  <AppFooter />
</template>

<style>
body {
  padding-top: 75px;
  background-color: #D8bFD8;
}
</style>