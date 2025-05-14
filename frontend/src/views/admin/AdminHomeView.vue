<script setup lang="ts"></script>

<template>
  <div class="admin-dashboard min-vh-100 bg-light">
    <!-- Main Cards -->
    <main class="container py-5">
      <div class="row g-4 justify-content-center">
        <!-- Files Card -->
        <div class="col-md-6 col-lg-4" @click="$router.push('/admin/file-manager')">
          <div class="card shadow-sm h-100 feature-card">
            <div class="card-body text-center p-4">
              <img
                src="/file-manager.png"
                alt="Files"
                class="img-fluid mb-3"
                style="max-height: 120px"
              />
              <h4 class="mb-3">Files</h4>
              <ul class="text-start ps-4">
                <li class="mb-2">Manage all system files and datasets</li>
                <li class="mb-2">Upload and organize data sources</li>
                <li class="mb-2">Generate synthetic test data</li>
                <li class="mb-2">Monitor data quality and integrity</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Alerts Card -->
        <div class="col-md-6 col-lg-4" @click="$router.push('/admin/alarm')">
          <div class="card shadow-sm h-100 feature-card">
            <div class="card-body text-center p-4">
              <img
                src="/alerts.jpg"
                alt="Alerts"
                class="img-fluid mb-3"
                style="max-height: 120px"
              />
              <h4 class="mb-3">Alarms</h4>
              <ul class="text-start ps-4">
                <li class="mb-2">Create alerts with natural language</li>
                <li class="mb-2">View and manage active alerts</li>
                <li class="mb-2">Review alert history and patterns</li>
                <li class="mb-2">Configure notification settings</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Users Card -->
        <div class="col-md-6 col-lg-4" @click="$router.push('/admin/user-manager')">
          <div class="card shadow-sm h-100 feature-card">
            <div class="card-body text-center p-4">
              <img src="/users.png" alt="Users" class="img-fluid mb-3" style="max-height: 120px" />
              <h4 class="mb-3">Users</h4>
              <ul class="text-start ps-4">
                <li class="mb-2">Manage user accounts and access</li>
                <li class="mb-2">Configure roles and permissions</li>
                <li class="mb-2">Monitor user activity and usage</li>
                <li class="mb-2">View audit logs and changes</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
}

.dashboard-header {
  border-bottom: 1px solid #e9ecef;
}

.feature-card {
  transition: all 0.2s ease;
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: rgba(24, 52, 70, 0.2);
}

.card-body ul {
  list-style-type: none;
  padding-left: 1rem;
}

.card-body li::before {
  content: '•';
  color: #0395ff;
  font-weight: bold;
  display: inline-block;
  width: 1em;
  margin-left: -1em;
}
</style>
