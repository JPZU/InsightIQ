<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
    <div class="text-center">
      <select v-model="exportFormat" class="form-select mt-2">
        <option value="png">PNG</option>
        <option value="jpg">JPG</option>
        <option value="pdf">PDF</option>
      </select>
      <button @click="downloadChart" class="btn btn-primary mt-2">Download Chart</button>
      <p v-if="message" class="mt-2">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import { useChartExporter } from '@/hooks/useChartExporter'

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

const { exportFormat, message, downloadChart } = useChartExporter(props.chartTitle, chartCanvas)

onMounted(renderChart)
watch(() => [props.xAxis, props.yAxis], renderChart)
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: auto;
}
</style>
