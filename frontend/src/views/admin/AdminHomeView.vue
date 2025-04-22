<script setup lang="ts"></script>

<template>
  <div class="d-flex flex-column min-vh-100">
    <section
      class="text-center pb-1 bg-light d-flex flex-column align-items-center justify-content-center"
    >
      <h1 class="display-6 fw-bold mt-3 mb-3" style="color: #183446">Admin Dashboard</h1>
      <p class="text-muted mt-2 mb-4">Manage system configurations and datasets.</p>
      <div class="row g-3">
        <div class="col-md-4" @click="$router.push('/admin/synthetic-data')">
          <div class="card shadow-sm p-3 card-hover h-100 text-center">
            <i class="bi bi-database h2" style="color: #183446"></i>
            <h5>Generate Synthetic Data</h5>
            <p class="text-muted">Create custom synthetic datasets tailored to your needs.</p>
            <img
              src="/synthetic-data.png"
              alt="Synthetic Data Icon"
              class="img-fluid"
              style="max-height: 220px"
            />
          </div>
        </div>
        <div class="col-md-4" @click="$router.push('/admin/file-manager')">
          <div class="card shadow-sm p-3 card-hover h-100 text-center">
            <i class="bi bi-folder h2" style="color: #183446"></i>
            <h5>File Manager</h5>
            <p class="text-muted">Manage and organize your project files.</p>
            <img
              src="/file-manager.png"
              alt="File Manager Icon"
              class="img-fluid"
              style="max-height: 220px"
            />
          </div>
        </div>
        <div class="col-md-4" @click="$router.push('/admin/alarm-create')">
          <div class="card shadow-sm p-3 card-hover h-100 text-center">
            <i class="bi bi-bell-plus h2" style="color: #183446"></i>
            <h5>Create Alarm</h5>
            <p class="text-muted">
              Describe in natural language the condition for generating an alarm..
            </p>
          </div>
        </div>
        <div class="col-md-4" @click="$router.push('/admin/alarm-list')">
          <div class="card shadow-sm p-3 card-hover h-100 text-center">
            <i class="bi bi-list-check h2" style="color: #183446"></i>
            <h5>Alarms List</h5>
            <p class="text-muted">Review and delete existing alarms configured in the system.</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.card-hover {
  transition:
    transform 0.3s ease-in-out,
    box-shadow 0.3s ease-in-out;
  cursor: pointer;
}
.card-hover:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}
</style>
