<template>
  <div class="bar-chart">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script lang="ts" setup>
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

// Registramos los componentes de Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

interface Props {
  columnName: string
  stats: Record<string, number>
}

const props = defineProps<Props>()

// Orden específico de métricas que queremos
const orderedMetrics = ['min', '25%', '50%', '75%', 'max', 'mean']

// Filtrar y ordenar solo las métricas que queremos mostrar en el orden correcto
const filteredStats = computed(() => {
  const { count, std, ...rest } = props.stats // Excluimos count y std
  const orderedStats: Record<string, number> = {}

  orderedMetrics.forEach((metric) => {
    if (rest[metric] !== undefined) {
      orderedStats[metric] = rest[metric]
    }
  })

  return orderedStats
})

const chartData = computed(() => ({
  labels: Object.keys(filteredStats.value),
  datasets: [
    {
      label: `Statistics for ${props.columnName}`,
      data: Object.values(filteredStats.value),
      backgroundColor: ['#3498db', '#1abc9c', '#f39c12', '#e74c3c', '#9b59b6', '#2ecc71'],
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // Control libre de tamaño
  plugins: {
    legend: {
      display: false,
    },
    title: {
      display: true,
      text: `Statistics for ${props.columnName}`,
    },
  },
}
</script>

<style scoped>
.bar-chart {
  width: 100%;
  height: 300px; /* Puedes ajustar según necesites */
}
</style>
