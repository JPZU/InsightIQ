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
  <div id="content-wrapper" class="d-flex flex-column vh-100">
    <div class="d-flex flex-grow-1">
      <!-- Main Content -->
      <div id="content" class="flex-grow-1 p-4">
        <select
          v-model="locale"
          class="px-4 py-2 border rounded-lg bg-white dark:bg-gray-800 text-gray-700 dark:text-white focus:ring focus:ring-blue-300 shadow-md transition"
        >
          <option value="en">English (US)</option>
          <option value="es">Español (CO)</option>
        </select>

        <Navbar />
        <router-view :key="route.fullPath" />
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer text-center p-2">
      <small>&copy; {{ new Date().getFullYear() }}{{ $t('app.rights') }}</small>
    </footer>
  </div>
</template>

<style scoped>
.footer {
  width: 100%;
  background-color: #046e8f;
  color: white;
  text-align: center;
}
</style>
