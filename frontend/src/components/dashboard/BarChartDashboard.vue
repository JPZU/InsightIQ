<template>
  <div class="bar-chart">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import type { I18n } from 'vue-i18n'
import { useI18n } from 'vue-i18n'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $t: (key: string, ...args: unknown[]) => string
  }
}

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

interface Props {
  columnName: string
  stats: Record<string, number>
}
const props = defineProps<Props>()

const orderedMetrics = ['min', '25%', '50%', '75%', 'max', 'mean']

const filteredStats = computed(() => {
  const { count, std, ...rest } = props.stats
  const orderedStats: Record<string, number> = {}

  orderedMetrics.forEach((metric) => {
    if (rest[metric] !== undefined) {
      orderedStats[metric] = rest[metric]
    }
  })

  return orderedStats
})

const { t } = useI18n()

const chartData = computed(() => ({
  labels: Object.keys(filteredStats.value),
  datasets: [
    {
      label: `${t('dashboard.statistics_for')} ${props.columnName}`,
      data: Object.values(filteredStats.value),
      backgroundColor: ['#3498db', '#1abc9c', '#f39c12', '#e74c3c', '#9b59b6', '#2ecc71'],
    },
  ],
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    title: { display: true, text: `${t('dashboard.statistics_for')} ${props.columnName}` },
  },
}))
</script>

<style scoped>
.bar-chart {
  width: 100%;
  height: 300px;
}
</style>
