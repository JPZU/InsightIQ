<template>
  <div id="content-wrapper" class="d-flex flex-column vh-100">
    <div class="d-flex flex-grow-1">
      <!-- Sidebar -->
      <aside
        :class="['sidebar', { collapsed: isCollapsed }]"
        class="text-white p-3 d-flex flex-column"
      >
        <!-- Título de la aplicación -->
        <div class="text-center mb-4">
          <span v-if="!isCollapsed" class="fs-3 fw-bold">InsightIQ</span>
        </div>

        <!-- Menú de la sidebar -->
        <ul class="navbar-nav flex-column">
          <router-link to="/" @click="closeOffcanvas" class="nav-link mt-1" active-class="active">
            <i class="fas fa-fw fa-home"></i>
            <span v-if="!isCollapsed">Home</span>
          </router-link>
          <router-link
            to="/chat"
            @click="closeOffcanvas"
            class="nav-link mt-1"
            active-class="active"
          >
            <i class="fas fa-comments"></i>
            <span v-if="!isCollapsed">Chat</span>
          </router-link>
          <router-link
            to="/synthetic-data"
            @click="closeOffcanvas"
            class="nav-link mt-1"
            active-class="active"
          >
            <i class="fas fa-database"></i>
            <span v-if="!isCollapsed">Synthetic Data</span>
          </router-link>
          <router-link
            to="/dashboard"
            @click="closeOffcanvas"
            class="nav-link mt-1"
            active-class="active"
          >
            <i class="fa-solid fa-chart-line"></i>
            <span v-if="!isCollapsed">Dashboard</span>
          </router-link>
          <router-link
            to="/detail-report"
            @click="closeOffcanvas"
            class="nav-link mt-1"
            active-class="active"
          >
            <i class="fa-solid fa-file-pdf"></i>
            <span v-if="!isCollapsed">Detailed Report</span>
          </router-link>
          <router-link
            to="/file-manager"
            @click="closeOffcanvas"
            class="nav-link mt-1"
            active-class="active"
          >
            <i class="fa-solid fa-folder"></i>
            <span v-if="!isCollapsed">File Manager</span>
          </router-link>
        </ul>

        <!-- Botón de colapsar sidebar -->
        <div class="text-center mt-3">
          <button class="btn btn-dark" @click="toggleSidebar">
            <i :class="isCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
          </button>
        </div>
      </aside>

      <!-- Main Content -->
      <div id="content" class="flex-grow-1 p-4">
        <Navbar />
        <router-view :key="route.fullPath" />
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer text-center p-2">
      <small>&copy; {{ new Date().getFullYear() }} InsightIQ - All Rights Reserved</small>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import Navbar from './components/layouts/NavbarComponent.vue'

const route = useRoute()

// sidebar state
import { ref } from 'vue'
const isCollapsed = ref(false)
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}
const closeOffcanvas = () => {
  // placeholder if needed
}
</script>

<style scoped>
/* Sidebar */
.sidebar {
  width: 250px;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  background-color: #046e8f;
}

.sidebar.collapsed {
  width: 70px;
}

/* Links */
.sidebar .nav-link {
  color: white;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 5px;
  text-decoration: none;
}

.sidebar .nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.sidebar .nav-link.active {
  background-color: rgba(255, 255, 255, 0.3);
}

/* Botón de colapsar */
.sidebar .btn-dark {
  background-color: transparent;
  border: none;
}

/* Ajustar el contenido principal */
#content {
  transition: margin-left 0.3s ease;
  padding-bottom: 50px;
  margin-left: 250px;
}

.sidebar.collapsed + #content {
  margin-left: 70px;
}

/* Footer */
.footer {
  width: 100%;
  background-color: #046e8f;
  color: white;
  text-align: center;
}
</style>
