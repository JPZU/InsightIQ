<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
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
const triggeredAlarms = ref<Record<string, any[]>>({})
const showAlarmsModal = ref(false)
const alarmCheckInterval = ref<number | null>(null)
const checkInterval = ref(30000) // 30 seconds by default

// Tab configuration
const navbarTabs = computed(() => {
  if (isAdminRoute.value) {
    return [
      { name: 'Admin Home', name_es: 'Inicio Admin', routeName: 'admin-home' },
      { name: 'File Manager', name_es: 'Gestor de Archivos', routeName: 'file-manager' },
      { name: 'Alarm Manager', name_es: 'Gestor de Alarmas', routeName: 'alarm' },
      { name: 'User Manager', name_es: 'Gestor de Usuarios', routeName: 'user-manager' },
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
    triggeredAlarms.value = response.data || {}
    
    if (Object.keys(triggeredAlarms.value).length > 0) {
      showAlarmsModal.value = true
      stopAlarmCheckInterval() // Stop checking when modal is shown
    }
  } catch (error) {
    console.error('Error checking alarms:', error)
  }
}

const startAlarmCheckInterval = () => {
  if (showAlarmsModal.value) return // Don't start if modal is open
  
  stopAlarmCheckInterval()
  checkTriggeredAlarms()
  alarmCheckInterval.value = window.setInterval(checkTriggeredAlarms, checkInterval.value)
}

const stopAlarmCheckInterval = () => {
  if (alarmCheckInterval.value !== null) {
    window.clearInterval(alarmCheckInterval.value)
    alarmCheckInterval.value = null
  }
}

const closeModal = () => {
  showAlarmsModal.value = false
  triggeredAlarms.value = {}
  startAlarmCheckInterval() // Restart checking when modal is closed
}

// Watch for modal state changes
watch(showAlarmsModal, (newVal) => {
  if (newVal) {
    stopAlarmCheckInterval()
  } else {
    startAlarmCheckInterval()
  }
})

onMounted(() => {
  startAlarmCheckInterval()
})

onUnmounted(() => {
  stopAlarmCheckInterval()
})

const updateCheckInterval = (newInterval: number) => {
  checkInterval.value = newInterval
  startAlarmCheckInterval()
}

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

const hasAlarms = computed(() => {
  return Object.keys(triggeredAlarms.value).length > 0
})

watch(isLoggedIn, (newVal) => {
  if (newVal) {
    startAlarmCheckInterval()
  } else {
    stopAlarmCheckInterval()
  }
}, { immediate: true })
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

  <!-- Alarm Notification Badge -->
  <div v-if="hasAlarms && !showAlarmsModal" class="alarm-notification" @click="showAlarmsModal = true">
    <span class="badge bg-danger">{{ Object.values(triggeredAlarms).flat().length }}</span>
    <span>{{ $t('app.new_alarms') }}</span>
  </div>

  <!-- Alarm Modal -->
  <div v-if="showAlarmsModal" class="modal" @click.self="closeModal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h3 class="modal-title">{{ $t('app.triggered_alarms') }}</h3>
      
      <div class="alarm-container">
        <div v-for="(alarms, tableName) in triggeredAlarms" :key="tableName" class="table-alarms">
          <h4 class="table-name">{{ tableName }}</h4>
          
          <div v-for="(alarm, index) in alarms" :key="index" class="alarm-card" :class="{'critical': alarm.severity === 'critical', 'warning': alarm.severity === 'warning'}">
            <div class="alarm-header">
              <h5>{{ alarm.description }}</h5>
              <span class="alarm-id">#{{ alarm.alarm_id }}</span>
            </div>
            
            <div class="alarm-details">
              <div class="detail-row">
                <span class="detail-label">{{ $t('app.condition') }}:</span>
                <span class="detail-value">{{ alarm.condition }} {{ alarm.threshold }}</span>
              </div>
              
              <div class="triggered-data">
                <h6>{{ $t('app.triggered_data') }}</h6>
                <div class="data-grid">
                  <div v-for="(value, key) in alarm.triggered_data" :key="key" class="data-item">
                    <span class="data-key">{{ String(key).replace(/_/g, ' ') }}:</span>
                    <span class="data-value">{{ value || 'N/A' }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="alarm-timestamp">
              {{ new Date(alarm.timestamp).toLocaleString() }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-actions">
        <button class="btn btn-primary" @click="closeModal">
          {{ $t('app.close') }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base modal styles */
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
  z-index: 1050;
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  position: relative;
}

.close {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 28px;
  font-weight: bold;
  color: #aaa;
  cursor: pointer;
  transition: color 0.2s;
}

.close:hover {
  color: #333;
}

.modal-title {
  margin-bottom: 20px;
  color: #333;
  font-weight: 600;
}

/* Alarm notification badge */
.alarm-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: white;
  padding: 10px 15px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  z-index: 100;
  transition: transform 0.2s;
}

.alarm-notification:hover {
  transform: translateY(-2px);
}

.alarm-notification .badge {
  font-size: 14px;
  padding: 5px 8px;
}

/* Alarm container styles */
.alarm-container {
  margin-top: 15px;
}

.table-alarms {
  margin-bottom: 25px;
}

.table-name {
  color: #444;
  margin-bottom: 15px;
  padding-bottom: 5px;
  border-bottom: 1px solid #eee;
}

.alarm-card {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  border-left: 4px solid #ddd;
}

.alarm-card.critical {
  border-left-color: #dc3545;
  background-color: #fff5f5;
}

.alarm-card.warning {
  border-left-color: #ffc107;
  background-color: #fffdf5;
}

.alarm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.alarm-header h5 {
  margin: 0;
  color: #333;
  font-weight: 600;
}

.alarm-id {
  background: #eee;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  color: #666;
}

.alarm-details {
  margin-bottom: 10px;
}

.detail-row {
  display: flex;
  margin-bottom: 5px;
}

.detail-label {
  font-weight: 500;
  margin-right: 5px;
  color: #555;
}

.detail-value {
  color: #333;
}

.triggered-data {
  margin-top: 10px;
}

.triggered-data h6 {
  margin: 10px 0 5px 0;
  color: #555;
  font-weight: 500;
}

.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
  margin-top: 8px;
}

.data-item {
  background: white;
  padding: 6px 10px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.data-key {
  font-weight: 500;
  color: #555;
  margin-right: 5px;
}

.data-value {
  color: #333;
}

.alarm-timestamp {
  font-size: 0.8em;
  color: #777;
  text-align: right;
}

.modal-actions {
  margin-top: 20px;
  text-align: right;
}

/* Navbar styles (existing) */
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