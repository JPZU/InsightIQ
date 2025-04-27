<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">Registered Alarms</h2>

    <div v-if="alarms.length === 0" class="text-gray-600">No alarms registered.</div>

    <div v-else class="space-y-4">
      <div
        v-for="alarm in alarms"
        :key="alarm.id"
        class="border border-gray-300 p-4 rounded shadow-sm flex justify-between items-start"
      >
        <div>
          <p><strong>Table:</strong> {{ alarm.table_name }}</p>
          <p><strong>Field:</strong> {{ alarm.field }}</p>
          <p><strong>Condition:</strong> {{ alarm.condition }} {{ alarm.threshold }}</p>
          <p><strong>Description:</strong> {{ alarm.description }}</p>
        </div>
        <button @click="goToEditAlarm(alarm.id)" class="btn-edit">Edit</button>
        <button @click="deleteAlarm(alarm.id)" class="btn-delete">Delete</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import AlarmService from '@/services/AlarmService'

const router = useRouter()

const goToEditAlarm = (id: number) => {
  router.push({ name: 'alarm-edit', params: { id } })
}

interface Alarm {
  id: number
  table_name: string
  field: string
  condition: string
  threshold: string | number
  description: string
}

const alarms = ref<Alarm[]>([])

const fetchAlarms = async () => {
  try {
    alarms.value = await AlarmService.listAlarms()
  } catch (error) {
    console.error('Error fetching alarms:', error)
  }
}

const deleteAlarm = async (id: number) => {
  try {
    await AlarmService.deleteAlarm(id)
    alarms.value = alarms.value.filter((alarm) => alarm.id !== id)
  } catch (error) {
    console.error('Error deleting alarm:', error)
  }
}

onMounted(fetchAlarms)
</script>

<style scoped>
.btn-edit {
  background-color: #3b82f6; /* Azul */
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  border: none;
  font-size: 14px;
  cursor: pointer;
}

.btn-edit:hover {
  background-color: #2563eb;
}

.btn-delete {
  background-color: #ef4444;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  border: none;
  font-size: 14px;
  cursor: pointer;
}

.btn-delete:hover {
  background-color: #dc2626;
}
</style>
