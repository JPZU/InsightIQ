<template>
  <div class="dashboard">
    <h1 class="text-center">AI-Generated Report</h1>

    <section class="file-schema">
      <h2>Generated on: {{ formatDate(report.date) }}</h2>

      <button @click="downloadPDF" class="download-btn">Download Report as PDF</button>

      <div
        ref="reportRef"
        v-if="report.report_text"
        class="report-text"
        v-html="formattedText"
      ></div>
      <div v-else class="loading">Loading report...</div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { marked } from 'marked'
import html2pdf from 'html2pdf.js'
import DetailReportService from '../services/DetailReportService'

const report = ref<{ report_text: string; date: string }>({
  report_text: '',
  date: '',
})
const reportRef = ref<HTMLElement | null>(null)

const formattedText = computed(() =>
  report.value.report_text ? marked.parse(report.value.report_text) : '',
)

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US')
}

const downloadPDF = () => {
  if (!reportRef.value) return

  const opt = {
    margin: 0.5,
    filename: `inventory_report_${new Date().toISOString().slice(0, 10)}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
  }

  html2pdf().set(opt).from(reportRef.value).save()
}

onMounted(async () => {
  const res = await DetailReportService.get_detailed_report()
  report.value = res.data
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
  font-family: Arial, sans-serif;
  max-width: 900px;
  margin: 0 auto;
}

.text-center {
  text-align: center;
}

.file-schema {
  margin-bottom: 30px;
  background: #fdfdfd;
  padding: 25px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.file-schema h2 {
  font-size: 1.3rem;
  margin-bottom: 10px;
  color: #2c3e50;
}

.download-btn {
  margin: 10px 0 20px;
  padding: 10px 18px;
  background-color: #0395ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.download-btn:hover {
  background-color: #43a3e7;
}

.report-text {
  font-size: 1rem;
  color: #333;
  line-height: 1.6;
}

.report-text h2,
.report-text h3 {
  color: #0395ff;
  margin-top: 20px;
}

.report-text p {
  margin: 12px 0;
  line-height: 1.6;
}

.report-text ul,
.report-text ol {
  margin: 12px 0 12px 20px;
}

.report-text table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 0.95rem;
}

.report-text th,
.report-text td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.report-text thead {
  background-color: #f4f4f4;
  font-weight: bold;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
}
</style>
