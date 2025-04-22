<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getNavbarConfig } from '@/utils/NavbarUtils'
import type { NavbarInterface } from '@/interfaces/NavbarInterface'
import AuthService from '@/services/AuthService'
import AlarmService from '@/services/AlarmService'

const route = useRoute()
const router = useRouter()
const navbarConfig = ref<NavbarInterface>({ primaryClass: '', tabs: [] })
const currentLanguage = ref('es')
const showLoginModal = ref(false)
const loginForm = ref({
  username: '',
  password: '',
  loading: false,
  error: ''
})

const isLoggedIn = computed(() => AuthService.isAuthenticated())

// 🔔 Estado para alarmas activadas
const triggeredAlarms = ref<any[]>([])

watch(route, (newRoute) => {
  const role = newRoute.path.startsWith('/admin') ? 'admin' : 'user'
  navbarConfig.value = getNavbarConfig(role)
})

const checkTriggeredAlarms = async () => {
  try {
    const response = await AlarmService.checkAlarms()
    triggeredAlarms.value = response.data?.triggered_alarms || []
  } catch (error) {
    console.error('Error checking alarms:', error)
  }
}

const closeModal = () => {
  triggeredAlarms.value = []
}

onMounted(() => {
  const role = route.path.startsWith('/admin') ? 'admin' : 'user'
  navbarConfig.value = getNavbarConfig(role)
})

const changeLanguage = () => {
  currentLanguage.value = currentLanguage.value === 'es' ? 'en' : 'es'
}

const handleLogin = async () => {
  loginForm.value.loading = true
  loginForm.value.error = ''
  
  try {
    const success = await AuthService.login(
      loginForm.value.username, 
      loginForm.value.password
    )
    
    if (success) {
      showLoginModal.value = false
      loginForm.value.username = ''
      loginForm.value.password = ''
      router.push({ name: 'home' })
    } else {
      loginForm.value.error = currentLanguage.value === 'es' 
        ? 'Credenciales incorrectas' 
        : 'Invalid credentials'
    }
  } catch (error) {
    loginForm.value.error = currentLanguage.value === 'es' 
      ? 'Error al iniciar sesión' 
      : 'Login error'
    console.error('Login error:', error)
  } finally {
    loginForm.value.loading = false
  }
}

const handleLogout = async () => {
  try {
    await AuthService.logout()
    router.push({ name: 'login' })
  } catch (error) {
    console.error('Logout error:', error)
  }
}

const goToProfile = () => {
  console.log('Ir al perfil del usuario')
}
</script>

<template>
  <nav class="navbar" style="height: 65px">
    <div class="container-fluid">
      <router-link class="navbar-brand ms-4 mb-0 h1" style="font-size: 1.5rem" :to="{ name: 'home' }">
        InsightIQ
      </router-link>

      <div class="d-flex align-items-center">
        <div class="dropdown me-3">
          <button
            class="btn btn-outline-secondary dropdown-toggle"
            type="button"
            id="languageDropdown"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            {{ currentLanguage === 'es' ? 'Español' : 'English' }}
          </button>
          <ul class="dropdown-menu" aria-labelledby="languageDropdown">
            <li>
              <a class="dropdown-item" href="#" @click.prevent="changeLanguage">
                {{ currentLanguage === 'es' ? 'English' : 'Español' }}
              </a>
            </li>
          </ul>
        </div>

        <div v-if="!isLoggedIn">
          <button
            type="button"
            class="btn btn-primary me-2"
            :class="navbarConfig.primaryClass"
            @click="router.push({ name: 'login' })"
          >
            {{ currentLanguage === 'es' ? 'Iniciar sesión' : 'Login' }}
          </button>
        </div>
        <div v-else class="dropdown">
          <button
            class="btn btn-outline-primary dropdown-toggle"
            :class="navbarConfig.primaryClass"
            type="button"
            id="userDropdown"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            {{ currentLanguage === 'es' ? 'Mi cuenta' : 'My account' }}
          </button>
          <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
            <li>
              <a class="dropdown-item" href="#" @click.prevent="goToProfile">
                {{ currentLanguage === 'es' ? 'Perfil' : 'Profile' }}
              </a>
            </li>
            <li>
              <a class="dropdown-item" href="#" @click.prevent="handleLogout">
                {{ currentLanguage === 'es' ? 'Cerrar sesión' : 'Logout' }}
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>

  <ul
    class="nav justify-content-center nav-underline d-flex align-items-center"
    :class="navbarConfig?.primaryClass"
    style="height: 65px"
    v-if="isLoggedIn"
  >
    <li v-for="tab in navbarConfig?.tabs" :key="tab.name" class="nav-item mx-5">
      <router-link
        class="nav-link text-white"
        :class="{ 'active fw-bold': route.name === tab?.routeName }"
        :to="{ name: tab?.routeName }"
      >
        {{ tab?.name }}
      </router-link>
    </li>
  </ul>

  <!-- Modal para alarmas activadas -->
  <div v-if="triggeredAlarms.length" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h3>Triggered Alarms</h3>
      <ul>
        <li v-for="(alarm, index) in triggeredAlarms" :key="index">
          <p><strong>The alarm with ID {{ alarm.alarm_id }} was triggered:</strong></p>
          <p><strong>Description:</strong> {{ alarm.description }}</p>
          <p><strong>Triggered Data:</strong></p>
          <ul>
            <li v-for="(value, key) in alarm.triggered_data" :key="key">
              <strong>{{ key.replace(/_/g, ' ') }}:</strong> {{ value || 'N/A' }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<style>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 500px;
  width: 90%;
  text-align: left;
  position: relative;
}

.close {
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 15px;
}
</style>
