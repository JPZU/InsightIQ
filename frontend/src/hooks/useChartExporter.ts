import { ref, type Ref } from 'vue'
import jsPDF from 'jspdf'

export function useChartExporter(chartTitle: string, chartCanvas: Ref<HTMLCanvasElement | null>) {
  const exportFormat = ref<'png' | 'jpg' | 'pdf'>('png')
  const message = ref('')

  const downloadChart = () => {
    if (!chartCanvas.value) {
      message.value = 'Chart is not ready yet.'
      return
    }

    try {
      const canvas = chartCanvas.value
      const dataUrl = canvas.toDataURL(`image/${exportFormat.value === 'jpg' ? 'jpeg' : 'png'}`)

      if (exportFormat.value === 'pdf') {
        const canvasWidth = canvas.width
        const canvasHeight = canvas.height
        const pxToMm = (px: number) => px * 0.264583
        const pdfWidth = pxToMm(canvasWidth)
        const pdfHeight = pxToMm(canvasHeight)

        const pdf = new jsPDF({
          orientation: pdfWidth > pdfHeight ? 'landscape' : 'portrait',
          unit: 'mm',
          format: [pdfWidth, pdfHeight],
        })

        pdf.addImage(dataUrl, 'PNG', 0, 0, pdfWidth, pdfHeight)
        pdf.save(`${chartTitle || 'chart'}.pdf`)
      } else {
        const link = document.createElement('a')
        link.download = `${chartTitle || 'chart'}.${exportFormat.value}`
        link.href = dataUrl
        link.click()
      }

      message.value = `Chart downloaded as ${exportFormat.value.toUpperCase()}.`
    } catch (err) {
      console.error(err)
      message.value = 'Failed to download chart. Please try again.'
    }
  }

  return { exportFormat, message, downloadChart }
}
