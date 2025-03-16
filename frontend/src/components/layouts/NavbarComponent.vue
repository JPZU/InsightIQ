<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getNavbarConfig } from '@/utils/NavbarUtils';
import type { NavbarInterface } from '@/interfaces/NavbarInterface';

const route = useRoute();
const navbarConfig = ref<NavbarInterface>({ primaryClass: '', tabs: [] });

watch(route, (newRoute) => {
    const role = newRoute.path.startsWith('/admin') ? 'admin' : 'user';
    navbarConfig.value = getNavbarConfig(role);
});

onMounted(() => {
    const role = route.path.startsWith('/admin') ? 'admin' : 'user';
    navbarConfig.value = getNavbarConfig(role);
});
</script>

<template>
    <nav class="navbar" style="height: 65px;">
        <div class="container-fluid">
            <a class="navbar-brand ms-4 mb-0 h1" style="font-size: 1.5rem;" href="#">InsightIQ</a>

            <form class="d-flex align-items-center">
                <div class="me-2">
                    <input type="text" class="form-control" placeholder="Search">
                </div>
                <div>
                    <button type="submit" class="btn btn-outline-primary"
                        :class="navbarConfig.primaryClass">Search</button>
                </div>
            </form>
        </div>
    </nav>

    <ul class="nav justify-content-center nav-underline d-flex align-items-center" :class="navbarConfig?.primaryClass"
        style="height: 65px;">
        <li v-for="tab in navbarConfig?.tabs" :key="tab.name" class="nav-item mx-5">
            <router-link class="nav-link text-white" :class="{ 'active fw-bold': route.name === tab?.routeName }"
                :to="{ name: tab?.routeName }">
                {{ tab?.name }}
            </router-link>
        </li>
    </ul>
</template>