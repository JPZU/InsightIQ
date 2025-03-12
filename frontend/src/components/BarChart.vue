<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  xAxis: {
    type: Array,
    required: true,
  },
  yAxis: {
    type: Array,
    required: true,
  },
  chartTitle: {
    type: String,
    default: 'Chart',
  },
})

const chartCanvas = ref(null)
let chartInstance = null

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy() // Destruir el gráfico anterior
  }

  const ctx = chartCanvas.value.getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: props.xAxis,
      datasets: [
        {
          label: props.chartTitle,
          data: props.yAxis,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  })
}

onMounted(renderChart)

watch(() => [props.xAxis, props.yAxis], renderChart)
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: auto;
}
</style>
