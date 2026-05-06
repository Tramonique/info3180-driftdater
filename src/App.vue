<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import {ref, provide} from "vue";

const isAuthenticated = ref(false);
const user = ref(null);

//To know what header titles to display based on if the user is logged in or not
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