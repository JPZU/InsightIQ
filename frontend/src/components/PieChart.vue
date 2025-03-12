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
    default: 'Pie Chart',
  },
})

const chartCanvas = ref(null)
let chartInstance = null

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: props.xAxis,
      datasets: [
        {
          label: props.chartTitle,
          data: props.yAxis,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: props.chartTitle,
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
