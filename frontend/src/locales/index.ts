import { createI18n } from 'vue-i18n'

// Import JSON files
import enApp from './en/app.json'
import enDashboard from './en/dashboard.json'
import enChat from './en/chat.json'
import enFileManager from './en/file_manager.json'
import enSyntheticData from './en/synthetic_data.json'

import esApp from './es/app.json'
import esDashboard from './es/dashboard.json'
import esChat from './es/chat.json'
import esFileManager from './es/file_manager.json'
import esSyntheticData from './es/synthetic_data.json'
import esPlans from './es/plans.json'
import enPlans from './en/plans.json'
// Merge translations by language
const messages = {
  en: {
    app: enApp,
    dashboard: enDashboard,
    chat: enChat,
    file_manager: enFileManager,
    synthetic_data: enSyntheticData,
    plans: enPlans,
  },
  es: {
    app: esApp,
    dashboard: esDashboard,
    chat: esChat,
    file_manager: esFileManager,
    synthetic_data: esSyntheticData,
    plans: esPlans,
  },
}

const i18n = createI18n({
  locale: localStorage.getItem('userLang') || 'en',
  fallbackLocale: 'en',
  messages,
})

export default i18n
