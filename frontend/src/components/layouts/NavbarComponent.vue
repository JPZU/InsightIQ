<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AuthService from '@/services/AuthService'
import AlarmService from '@/services/AlarmService'

const { locale, t } = useI18n()
const route = useRoute()
const router = useRouter()
const currentLanguage = computed(() => locale.value)

const showLoginModal = ref(false)
const loginForm = ref({
  username: '',
  password: '',
  loading: false,
  error: '',
})

const isLoggedIn = computed(() => AuthService.isAuthenticated())
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
const triggeredAlarms = ref<any[]>([])

// Configuración quemada de las tabs
const navbarTabs = computed(() => {
  if (isAdminRoute.value) {
    return [
      { name: 'Admin Home', name_es: 'Inicio Admin', routeName: 'admin-home' },
      { name: 'Synthetic Data', name_es: 'Datos Sintéticos', routeName: 'synthetic-data' },
      { name: 'File Manager', name_es: 'Gestor de Archivos', routeName: 'file-manager' },
      { name: 'Alarm Manager', name_es: 'Gestor de Alarmas', routeName: 'alarm' },
    ]
  } else {
    return [
      { name: 'Home', name_es: 'Inicio', routeName: 'home' },
      { name: 'Chat', name_es: 'Chat', routeName: 'chat' },
      { name: 'Dashboard', name_es: 'Panel', routeName: 'dashboard' },
      { name: 'Report', name_es: 'Reporte', routeName: 'report' },
    ]
  }
})

const navbarClass = computed(() => {
  return isAdminRoute.value ? 'bg-danger' : 'bg-primary'
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
  checkTriggeredAlarms()
})

const changeLanguage = (lang: string) => {
  locale.value = lang
}

const handleLogin = async () => {
  loginForm.value.loading = true
  loginForm.value.error = ''

  try {
    const success = await AuthService.login(loginForm.value.username, loginForm.value.password)

    if (success) {
      showLoginModal.value = false
      loginForm.value.username = ''
      loginForm.value.password = ''
      router.push({ name: 'home' })
    } else {
      loginForm.value.error = t('auth.invalid_credentials')
    }
  } catch (error) {
    loginForm.value.error = t('auth.login_error')
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
  router.push({ name: 'profile' })
}
</script>

<template>
  <nav class="navbar" style="height: 65px">
    <div class="container-fluid">
      <router-link
        class="navbar-brand ms-4 mb-0 h1"
        style="font-size: 1.5rem"
        :to="{ name: 'home' }"
      >
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
              <a
                class="dropdown-item"
                href="#"
                @click.prevent="changeLanguage(currentLanguage === 'es' ? 'en' : 'es')"
              >
                {{ currentLanguage === 'es' ? 'English' : 'Español' }}
              </a>
            </li>
          </ul>
        </div>

        <div v-if="!isLoggedIn">
          <button
            type="button"
            class="btn btn-primary me-2"
            :class="navbarClass"
            @click="router.push({ name: 'login' })"
          >
            {{ $t('app.login') }}
          </button>
        </div>

        <div v-else class="dropdown">
          <button
            class="btn btn-outline-primary dropdown-toggle"
            :class="navbarClass"
            type="button"
            id="userDropdown"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            {{ $t('app.my_account') }}
          </button>
          <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
            <li>
              <a class="dropdown-item" href="#" @click.prevent="goToProfile">
                {{ $t('app.profile') }}
              </a>
            </li>
            <li>
              <a class="dropdown-item" href="#" @click.prevent="handleLogout">
                {{ $t('app.logout') }}
              </a>
            </li>
            <li>
              <a class="dropdown-item" href="#" @click.prevent="router.push('/admin')">
                {{ $t('app.go_to_admin') }}
              </a>
            </li>
            <li>
              <a class="dropdown-item" href="#" @click.prevent="router.push('/')">
                {{ $t('app.go_to_home') }}
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>

  <ul
    class="nav justify-content-center nav-underline d-flex align-items-center"
    :class="navbarClass"
    style="height: 65px"
    v-if="isLoggedIn"
  >
    <li v-for="tab in navbarTabs" :key="tab.name" class="nav-item mx-5">
      <router-link
        class="nav-link text-white"
        :class="{ 'active fw-bold': route.name === tab.routeName }"
        :to="{ name: tab.routeName }"
      >
        {{ currentLanguage === 'es' ? tab.name_es : tab.name }}
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
          <p>
            <strong>The alarm with ID {{ alarm.alarm_id }} was triggered:</strong>
          </p>
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

/* Estilos para las tabs */
.nav-underline .nav-link {
  color: rgba(255, 255, 255, 0.75);
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.nav-underline .nav-link:hover {
  color: white;
  border-bottom-color: white;
}

.nav-underline .nav-link.active {
  color: white;
  border-bottom-color: white;
}

/* Colores para admin/user */
.bg-danger {
  background-color: #c73659 !important;
}

.bg-primary {
  background-color: #0395ff !important;
  color: white !important;
}

.btn-outline-primary.bg-danger {
  color: white;
  border-color: white;
}

.btn-outline-primary.bg-danger:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
