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

    <div class="text-center my-3">
      <select v-model="exportFormat" class="form-select me-2">
        <option value="csv">CSV</option>
        <option value="xlsx">XLSX</option>
      </select>
      <button @click="downloadTable" class="btn btn-primary mt-2">Download Table</button>
      <p v-if="message" class="mt-2">{{ message }}</p>
    </div>

    <!-- Paginación -->
    <div class="pagination-container">
      <button class="btn btn-outline-primary" :disabled="currentPage === 1" @click="currentPage--">
        {{ $t('dashboard.previous') }}
      </button>

      <span class="page-indicator">
        {{ $t('dashboard.page') }} {{ currentPage }} {{ $t('dashboard.of') }} {{ totalPages }}
      </span>

      <button
        class="btn btn-outline-primary"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        {{ $t('dashboard.next') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import * as XLSX from 'xlsx'

const props = defineProps({
  queryOutput: {
    type: Array,
    required: true,
  },
})

const currentPage = ref(1)
const rowsPerPage = 5
const exportFormat = ref('csv')
const message = ref('')

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

const downloadTable = () => {
  if (!props.queryOutput.length) {
    message.value = 'No data available for export.'
    return
  }

  const format = exportFormat.value

  if (format === 'csv') {
    try {
      let csvContent = 'data:text/csv;charset=utf-8,'

      if (headers.value.length) {
        csvContent += headers.value.join(',') + '\r\n'
      }

      props.queryOutput.forEach((row) => {
        csvContent +=
          row
            .map((cell) =>
              typeof cell === 'string' && (cell.includes(',') || cell.includes('"'))
                ? `"${cell.replace(/"/g, '""')}"`
                : cell,
            )
            .join(',') + '\r\n'
      })

      const encodedUri = encodeURI(csvContent)
      const link = document.createElement('a')
      link.setAttribute('href', encodedUri)
      link.setAttribute('download', 'table_export.csv')
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      message.value = 'CSV file downloaded successfully!'
    } catch (error) {
      console.error(error)
      message.value = 'Error exporting CSV file.'
    }
  }

  if (format === 'xlsx') {
    try {
      const data = props.queryOutput.map((row) => {
        const obj = {}
        row.forEach((cell, i) => {
          obj[headers.value[i] || `Column ${i + 1}`] = cell
        })
        return obj
      })

      const worksheet = XLSX.utils.json_to_sheet(data)
      const workbook = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Table')
      XLSX.writeFile(workbook, 'table_export.xlsx')

      message.value = 'XLSX file downloaded successfully!'
    } catch (error) {
      console.error(error)
      message.value = 'Error exporting XLSX file.'
    }
  }
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
