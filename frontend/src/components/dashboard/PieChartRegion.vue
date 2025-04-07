<template>
  <div style="width: 400px; margin: 0 auto; padding: 10px 0">
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { computed } from 'vue'

// 📦 Registramos los componentes necesarios de Chart.js
ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale)

// 🧾 Props que recibe el componente
const props = defineProps<{
  region: string
  data: Array<{ name: string; value: number }>
}>()

// 🧠 Datos que va a mostrar el gráfico
const chartData = computed(() => ({
  labels: props.data.map((item) => item.name),
  datasets: [
    {
      label: 'Unidades vendidas',
      data: props.data.map((item) => item.value),
      backgroundColor: [
        '#3498db',
        '#2ecc71',
        '#e74c3c',
        '#f1c40f',
        '#9b59b6',
        '#1abc9c',
        '#e67e22',
        '#34495e',
        '#7f8c8d',
        '#ff6384',
      ],
    },
  ],
}))

// 🎛️ Opciones del gráfico
const chartOptions = computed(() => ({
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom',
    },
    title: {
      display: true,
      text: `Distribución de ventas - Región ${props.region}`,
    },
  },
}))
</script>
