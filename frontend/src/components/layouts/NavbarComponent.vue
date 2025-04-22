<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getNavbarConfig } from '@/utils/NavbarUtils'
import type { NavbarInterface } from '@/interfaces/NavbarInterface'
import AlarmService from '@/services/AlarmService'

const route = useRoute()
const navbarConfig = ref<NavbarInterface>({ primaryClass: '', tabs: [] })

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

  // Evaluar alarmas al montar la navbar
  checkTriggeredAlarms()
})
</script>

<template>
  <nav class="navbar" style="height: 65px">
    <div class="container-fluid">
      <a class="navbar-brand ms-4 mb-0 h1" style="font-size: 1.5rem" href="#">InsightIQ</a>

      <form class="d-flex align-items-center">
        <div class="me-2">
          <input type="text" class="form-control" placeholder="Search" />
        </div>
        <div>
          <button type="submit" class="btn btn-outline-primary" :class="navbarConfig.primaryClass">
            Search
          </button>
        </div>
      </form>
    </div>
  </nav>

  <ul
    class="nav justify-content-center nav-underline d-flex align-items-center"
    :class="navbarConfig?.primaryClass"
    style="height: 65px"
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
</style>
