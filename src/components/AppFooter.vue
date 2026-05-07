<template>
      <footer class="mt-5">
          <div class="container">
              <p>Copyright &copy {{ year }} Flask Inc.</p>
              <p>This website is for academic demonstration purposes only. 
                All images are the property of their respective owners and are used for illustration purposes only.</p>
          </div>
      </footer>
</template>

<script setup>
import { ref } from "vue";

const year = (new Date).getFullYear();
</script>

<style>
/* Add any component specific styles here */
</style>