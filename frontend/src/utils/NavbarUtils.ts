import type { NavbarConfigInterface } from '@/interfaces/NavbarInterface'

export const getNavbarConfig = (role: string): NavbarConfigInterface => {
  if (role === 'admin') {
    return {
      tabs: [
        { name: 'Admin Home', routeName: 'admin-home' },
        { name: 'Synthetic Data', routeName: 'synthetic-data' },
        { name: 'File Manager', routeName: 'file-manager' },
        { name: 'Create Alarm', routeName: 'alarm-create' },
        { name: 'Alarm List', routeName: 'alarm-list' },
        
      ],
      primaryClass: 'primary-admin',
    }
  } else if (role === 'user') {
    return {
      tabs: [
        { name: 'Home', routeName: 'home' },
        { name: 'Chat', routeName: 'chat' },
        { name: 'Dashboard', routeName: 'dashboard' },
        { name: 'Report', routeName: 'report' },
      ],
      primaryClass: 'primary-user',
    }
  } else {
    return {
      tabs: [],
      primaryClass: '',
    }
  }
}
