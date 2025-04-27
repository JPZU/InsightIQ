<script setup lang="ts">
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Navbar from './components/layouts/NavbarComponent.vue'

const route = useRoute()

const { locale } = useI18n()

const savedLang = localStorage.getItem('userLang') || 'en'
locale.value = savedLang

watch(locale, (newLang) => {
  localStorage.setItem('userLang', newLang)
})
</script>

<template>
  <Navbar />
  <router-view :key="route.fullPath" />
</template>
