<template>
  <div class="table-responsive">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in paginatedRows" :key="rowIndex">
          <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
        </tr>
      </tbody>
    </table>

    <div class="text-center mb-3">
      <button @click="exportToCSV" class="btn btn-primary">Export to CSV</button>
    </div>

    <!-- Paginación -->
    <div class="pagination-container">
      <button class="btn btn-outline-primary" :disabled="currentPage === 1" @click="currentPage--">
        Previous
      </button>

      <span class="page-indicator"> Page {{ currentPage }} of {{ totalPages }} </span>

      <button
        class="btn btn-outline-primary"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  queryOutput: {
    type: Array,
    required: true,
  },
})

const currentPage = ref(1)
const rowsPerPage = 5 // Máximo de registros por página

// Extraer encabezados de la primera fila si existen
const headers = computed(() => {
  if (props.queryOutput.length > 0 && Array.isArray(props.queryOutput[0])) {
    return props.queryOutput[0].map((_, index) => `Column ${index + 1}`)
  }
  return []
})

// Cálculo de paginación
const totalPages = computed(() => Math.ceil(props.queryOutput.length / rowsPerPage))

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage
  return props.queryOutput.slice(start, start + rowsPerPage)
})

const exportToCSV = () => {
  if (!props.queryOutput.length) return

  // Prepare CSV content
  let csvContent = 'data:text/csv;charset=utf-8,'

  // Add headers if they exist
  if (headers.value.length) {
    csvContent += headers.value.join(',') + '\r\n'
  }

  // Add all rows (not just paginated ones)
  props.queryOutput.forEach((row) => {
    csvContent +=
      row
        .map((cell) => {
          // Escape cells that contain commas or quotes
          if (typeof cell === 'string' && (cell.includes(',') || cell.includes('"'))) {
            return `"${cell.replace(/"/g, '""')}"`
          }
          return cell
        })
        .join(',') + '\r\n'
  })

  // Create download link
  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', 'table_export.csv')
  document.body.appendChild(link)

  // Trigger download
  link.click()
  document.body.removeChild(link)
}
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}

.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}

.page-indicator {
  margin: 0 15px;
  font-weight: bold;
}
</style>
