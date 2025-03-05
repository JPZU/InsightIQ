<template>
  <div id="content-wrapper" class="d-flex flex-column vh-100">
    <div class="d-flex flex-grow-1">
      <!-- Sidebar -->
      <aside
        :class="['sidebar', { collapsed: isCollapsed }]"
        class="bg-dark text-white p-3 d-flex flex-column"
      >
        <!-- Título de la aplicación -->
        <div class="text-center mb-4">
          <span v-if="!isCollapsed" class="fs-3 fw-bold">InsighIQ</span>
        </div>

        <!-- Menú de la sidebar -->
        <ul class="navbar-nav flex-column">
          <router-link to="/" @click="closeOffcanvas" class="nav-link mt-1" active-class="active">
            <i class="fas fa-fw fa-home"></i>
            <span>Home</span>
          </router-link>
          <router-link
            to="/chat"
            @click="closeOffcanvas"
            class="nav-link mt-1"
            active-class="active"
          >
            <i class="fas fa-comments"></i>
            <span>Chat</span>
          </router-link>
          <router-link
            to="/synthetic-data"
            @click="closeOffcanvas"
            class="nav-link mt-1"
            active-class="active"
          >
            <i class="fas fa-database"></i>
            <span>Synthetic Data</span>
          </router-link>
          <router-link
            to="/dashboard"
            @click="closeOffcanvas"
            class="nav-link mt-1"
            active-class="active"
          >
            <i class="fa-solid fa-chart-line"></i>
            <span>Dashboard</span>
          </router-link>
        </ul>

        <!-- Botón de colapsar sidebar (justo debajo del menú) -->
        <div class="text-center mt-3">
          <button class="btn btn-dark" @click="toggleSidebar">
            <i :class="isCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
          </button>
        </div>
      </aside>

      <!-- Main Content -->
      <div
        id="content"
        class="flex-grow-1 p-4"
        :style="{ marginLeft: isCollapsed ? '70px' : '250px' }"
      >
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

// Estado para controlar si la sidebar está colapsada
const isCollapsed = ref(false)

// Función para alternar el estado de colapso
function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

// Función para cerrar el offcanvas (si es necesario)
function closeOffcanvas() {
  const offcanvasToggler = document.getElementById('offcanvasToggler')
  if (offcanvasToggler) {
    offcanvasToggler.click()
  }
}
</script>

<style scoped>
/* Ajuste de sidebar */
.sidebar {
  width: 250px;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
  position: fixed; /* Fijar la sidebar */
  height: 100vh; /* Altura completa */
}

.sidebar.collapsed {
  width: 70px;
}

/* Ocultar texto cuando está colapsado */
.sidebar .nav-link span {
  display: inline;
  transition: opacity 0.3s ease;
  white-space: nowrap; /* Evitar que el texto ocupe más de una línea */
}

.sidebar.collapsed .nav-link span {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

/* Iconos bien alineados */
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

.sidebar .nav-link i {
  width: 20px;
  text-align: center;
}

/* Estilo para el enlace activo */
.sidebar .nav-link.active {
  background-color: rgba(255, 255, 255, 0.3);
}

/* Estilo para el botón de colapsar */
.sidebar .btn-dark {
  background-color: transparent;
  border: none;
  white-space: nowrap; /* Evitar que el texto ocupe más de una línea */
}

.sidebar .btn-dark:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Estilo para el título de la aplicación */
.sidebar .fs-3 {
  color: white;
  font-size: 1.75rem; /* Tamaño más grande */
}

/* Espacio entre el menú y el botón */
.sidebar .text-center.mt-3 {
  margin-top: 1rem; /* Espacio de 1rem (16px) */
}

/* Ajustar el contenido principal */
#content {
  transition: margin-left 0.3s ease; /* Transición suave */
}
</style>
