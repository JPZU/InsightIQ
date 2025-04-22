<script setup lang="ts">
import { useRoute } from 'vue-router'
import Navbar from './components/layouts/NavbarComponent.vue'

const route = useRoute()
</script>

<template>
  <div id="content" class="flex-grow-1">
    <Navbar />
    <router-view :key="route.fullPath" />
  </div>
</template>

<style scoped></style>
