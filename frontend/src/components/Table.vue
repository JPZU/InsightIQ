<template>
  <div class="table-responsive">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
          <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  queryOutput: {
    type: Array,
    required: true,
  },
})

// Extraer encabezados y filas de queryOutput
const headers = computed(() => {
  if (props.queryOutput.length > 0 && Array.isArray(props.queryOutput[0])) {
    return props.queryOutput[0].map((_, index) => `Column ${index + 1}`)
  }
  return []
})

const rows = computed(() => {
  return props.queryOutput.slice(0, 5) // Mostrar máximo 5 filas
})
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}
</style>
