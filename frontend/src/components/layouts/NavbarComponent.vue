<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const props = defineProps<{ navbarConfig: { role: string, tabs: { name: string, routeName: string }[] } }>()

const primaryClass = props.navbarConfig.role === 'admin' ? 'primary-admin' : 'primary-user'
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
                    <button type="submit" class="btn btn-outline-primary" :class="primaryClass">
                        Search
                    </button>
                </div>
            </form>
        </div>
    </nav>

    <ul class="nav justify-content-center nav-underline d-flex align-items-center"
        :class="primaryClass" style="height: 65px;">
        <li v-for="tab in props.navbarConfig.tabs" :key="tab.name" class="nav-item mx-4">
            <router-link class="nav-link text-white" 
                :class="{ 'active fw-bold': route.name === tab.routeName }"
                :to="{ name: tab.routeName }">
                {{ tab.name }}
            </router-link>
        </li>
    </ul>
</template>
