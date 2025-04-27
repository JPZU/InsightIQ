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
    default: 'Bar Chart',
  },
})

const chartCanvas = ref(null)
let chartInstance = null

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }

  if (!props.xAxis.length || !props.yAxis.length) return

  const ctx = chartCanvas.value.getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: props.xAxis,
      datasets: [
        {
          label: props.chartTitle,
          data: props.yAxis,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              return `${context.dataset.label}: ${context.parsed.y}`;
            }
          }
        }
      }
    },
  })
}

const { exportFormat, message, downloadChart } = useChartExporter(props.chartTitle, chartCanvas)

onMounted(renderChart)
watch(() => [props.xAxis, props.yAxis], renderChart)
</script>

<template>
  <div>
    <div style="position: relative; height: 400px;">
      <canvas ref="chartCanvas"></canvas>
    </div>
    <div class="text-center mt-2">
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

<style scoped>
canvas {
  max-width: 100%;
  height: auto;
}
</style>
