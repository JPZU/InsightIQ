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
import enAdminHome from './en/admin_home.json'
import esAdminHome from './es/admin_home.json'
import enAdminFileManager from './en/admin_file_manager.json'
import esAdminFileManager from './es/admin_file_manager.json'
import enAdminUserManager from './en/admin_user_manager.json'
import esAdminUserManager from './es/admin_user_manager.json'
// Merge translations by language
const messages = {
  en: {
    app: enApp,
    dashboard: enDashboard,
    chat: enChat,
    file_manager: enFileManager,
    synthetic_data: enSyntheticData,
    plans: enPlans,
    admin_home: enAdminHome,
    admin_file_manager: enAdminFileManager,
    admin_user_manager: enAdminUserManager,
  },
  es: {
    app: esApp,
    dashboard: esDashboard,
    chat: esChat,
    file_manager: esFileManager,
    synthetic_data: esSyntheticData,
    plans: esPlans,
    admin_home: esAdminHome,
    admin_file_manager: esAdminFileManager,
    admin_user_manager: esAdminUserManager,
  },
}

const i18n = createI18n({
  locale: localStorage.getItem('userLang') || 'en',
  fallbackLocale: 'en',
  messages,
})

export default i18n
