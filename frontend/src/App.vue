<script setup lang="ts">
import { useRoute } from 'vue-router';
import Navbar from './components/layouts/NavbarComponent.vue';

const route = useRoute();
</script>

<template>
  <Navbar />
  <router-view :key="route.fullPath" />
</template>
