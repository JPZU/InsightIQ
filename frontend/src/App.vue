<template>
  <div id="content-wrapper" class="d-flex flex-column vh-100">
    <!-- Main Content -->
    <div class="flex-grow-1 p-4">
      <Navbar />
      <router-view :key="route.fullPath" />
    </div>

    <!-- Footer -->
    <footer class="footer text-center p-2">
      <small>&copy; {{ new Date().getFullYear() }} InsightIQ - All Rights Reserved</small>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import Navbar from './components/layouts/NavbarComponent.vue'

const route = useRoute()
</script>

<style scoped>
/* Ajustar el contenido principal */
#content-wrapper {
  width: 100%;
}

/* Footer */
.footer {
  width: 100%;
  background-color: #046e8f;
  color: white;
  text-align: center;
}
</style>
