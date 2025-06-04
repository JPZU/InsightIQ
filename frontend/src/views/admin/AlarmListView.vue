<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">{{ $t('admin_alarms.list.title') }}</h2>

    <div v-if="alarms.length === 0" class="text-gray-600">{{ $t('admin_alarms.list.empty') }}</div>

    <div v-else class="space-y-4">
      <div
        v-for="alarm in alarms"
        :key="alarm.id"
        class="border border-gray-300 p-4 rounded shadow-sm flex justify-between items-start"
      >
        <div>
          <p><strong>{{ $t('admin_alarms.list.alarm.table') }}:</strong> {{ alarm.table_name }}</p>
          <p><strong>{{ $t('admin_alarms.list.alarm.field') }}:</strong> {{ alarm.field }}</p>
          <p><strong>{{ $t('admin_alarms.list.alarm.condition') }}:</strong> {{ alarm.condition }} {{ alarm.threshold }}</p>
          <p><strong>{{ $t('admin_alarms.list.alarm.description') }}:</strong> {{ alarm.description }}</p>
        </div>
        <button @click="goToEditAlarm(alarm.id)" class="btn-edit">{{ $t('admin_alarms.list.actions.edit') }}</button>
        <button @click="deleteAlarm(alarm.id)" class="btn-delete">{{ $t('admin_alarms.list.actions.delete') }}</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import AlarmService from '@/services/AlarmService'

const router = useRouter()
const { t } = useI18n()

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
    console.error(t('admin_alarms.list.errors.fetch_failed'), error)
  }
}

const deleteAlarm = async (id: number) => {
  try {
    await AlarmService.deleteAlarm(id)
    alarms.value = alarms.value.filter((alarm) => alarm.id !== id)
  } catch (error) {
    console.error(t('admin_alarms.list.errors.delete_failed'), error)
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
