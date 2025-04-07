<template>
  <div class="dashboard">
    <h1 class="text-center">📊 Detailed Sales Report</h1>

    <section class="file-schema">
      <h2>📦 Inventory Summary</h2>
      <ul>
        <li><strong>Total unique products:</strong> {{ summary.total_products }}</li>
        <li><strong>Total inventory:</strong> {{ summary.total_inventory }}</li>
        <li>
          <strong>Average inventory per product:</strong>
          {{ summary.average_for_product_inventory }}
        </li>
      </ul>
    </section>

    <section class="file-schema">
      <h2>🚨 Restock Recommendations</h2>
      <ul>
        <li v-for="item in restock" :key="item['Product ID']">
          {{ item['Product ID'] }} — Inventory: {{ item['Inventory Level'] }}, Forecast:
          {{ item['Demand Forecast'] }}
        </li>
      </ul>
    </section>

    <section class="file-schema">
      <h2>🌍 Sales by Region</h2>
      <div class="region-buttons">
        <button
          v-for="region in Object.keys(report)"
          :key="region"
          @click="selectedRegion = region"
          :class="{ active: selectedRegion === region }"
        >
          {{ region }}
        </button>
      </div>
    </section>

    <section
      v-for="(stores, region) in report"
      :key="region"
      v-show="selectedRegion === region"
      class="file-schema"
      :id="`region-${region}`"
    >
      <h3>📍 Region: {{ region }}</h3>

      <button @click="downloadRegionReport(region)" class="download-btn">
        📥 Download Report as PDF
      </button>

      <PieChartRegion :region="region" :data="getStoreSalesData(stores)" />

      <div v-for="(info, storeId) in stores" :key="storeId" class="store-block">
        <h4>🏪 Store ID: {{ storeId }}</h4>

        <div class="product-columns">
          <div class="column-block">
            <h5>🔼 Top 5 Best-Selling Products</h5>
            <ul>
              <li v-for="p in info.top_5_products" :key="p['Product ID']">
                {{ p['Product ID'] }} — {{ p['Units Sold'] }} units sold
              </li>
            </ul>
          </div>

          <div class="column-block">
            <h5>🔽 Bottom 5 Worst-Selling Products</h5>
            <ul>
              <li v-for="p in info.bottom_5_products" :key="p['Product ID']">
                {{ p['Product ID'] }} — {{ p['Units Sold'] }} units sold
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import DetailReportService from '../services/DetailReportService'
import PieChartRegion from '../components/dashboard/PieChartRegion.vue'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

const summary = ref({
  total_products: 0,
  total_inventory: 0,
  average_inventory: 0,
})
const restock = ref([])
const report = ref({})
const selectedRegion = ref('')

const getStoreSalesData = (stores: any) =>
  Object.entries(stores).map(([storeId, info]: any) => ({
    name: storeId,
    value: info.top_5_products.reduce((sum: number, p: any) => sum + p['Units Sold'], 0),
  }))

const downloadRegionReport = async (region: string) => {
  const section = document.getElementById(`region-${region}`)
  if (!section) return

  const canvas = await html2canvas(section, { scale: 2 })
  const imgData = canvas.toDataURL('image/png')
  const pdf = new jsPDF('p', 'mm', 'a4')
  const pdfWidth = pdf.internal.pageSize.getWidth()
  const pdfHeight = (canvas.height * pdfWidth) / canvas.width

  pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight)
  pdf.save(`region_${region}_report.pdf`)
}

onMounted(async () => {
  const [inv, turn, reco] = await Promise.all([
    DetailReportService.getInventorySummary(),
    DetailReportService.getTurnoverAnalysisByRegion(),
    DetailReportService.getRestockRecommendations(),
  ])
  summary.value = inv.data
  report.value = turn.data
  restock.value = reco.data
  selectedRegion.value = Object.keys(turn.data)[0]
})
</script>

<style scoped>
.product-columns {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
  justify-content: space-between;
}

.column-block {
  flex: 1;
  min-width: 280px;
}

.download-btn {
  margin: 10px 0 20px;
  padding: 10px 18px;
  background-color: #046e8f;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.download-btn:hover {
  background-color: #035471;
}

.dashboard {
  padding: 20px;
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}

.region-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 15px;
}

.region-buttons button {
  background-color: #f4f4f4;
  border: 1px solid #ccc;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.region-buttons button.active,
.region-buttons button:hover {
  background-color: #046e8f;
  color: white;
}

.store-block {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px 20px;
  margin-bottom: 20px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.05);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-wrapper {
  background: #f9f9f9;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  margin-bottom: 20px;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f4f4f4;
}

.file-schema {
  margin-bottom: 30px;
  background: #fdfdfd;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.file-schema h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
  background: white;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  background-color: white;
  border: 1px solid #ddd;
}

.styled-table thead {
  background-color: #f4f4f4;
}

.styled-table th {
  padding: 12px;
  text-align: left;
  font-weight: bold;
  color: #2c3e50;
  border-bottom: 2px solid #ddd;
}

.styled-table td {
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
  color: #555;
}

.styled-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.styled-table tr:hover {
  background-color: #f1f1f1;
  transition: background-color 0.3s ease;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
