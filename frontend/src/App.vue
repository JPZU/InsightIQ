<script setup lang="ts">
import { ref } from 'vue'
import Navbar from './components/layouts/NavbarComponent.vue'

const userRole = ref('user')

const navbarConfig = ref({
    role: userRole.value,
    tabs: [
        { name: 'Inicio', routeName: 'home' },
        { name: 'Chat', routeName: 'chat' },
        { name: 'Dashboard', routeName: 'dashboard' },
        { name: 'Synthetic Data', routeName: 'synthetic-data' },
        { name: 'File Manager', routeName: 'file-manager' },
    ]
})
</script>

<template>
    <Navbar :navbar-config="navbarConfig" />
    <router-view />
</template>
