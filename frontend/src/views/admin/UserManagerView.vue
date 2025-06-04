<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import AdminUserService from '@/services/admin/AdminUserService'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const state = reactive({
  loading: true,
  error: null,
  users: [],
  metrics: {
    total_users: 0,
    total_admins: 0,
    total_questions_asked: 0,
  },
  searchQuery: '',
  sortBy: 'name',
  sortDirection: 'asc',
})

const fetchUserData = async () => {
  state.loading = true
  state.error = null

  try {
    const response = await AdminUserService.listAllUsers()
    if (response?.response) {
      state.users = Array.isArray(response.response.users_info) ? response.response.users_info : []
      state.metrics = {
        total_users: response.response.general_metrics?.total_users || 0,
        total_admins: response.response.general_metrics?.total_admins || 0,
        total_questions_asked: response.response.general_metrics?.total_questions_asked || 0,
      }
    } else {
      state.error = t('admin_user_manager.errors.load_failed')
    }
  } catch (error) {
    console.error('Error fetching user data:', error)
    state.error = t('admin_user_manager.errors.load_failed')
    state.users = []
    state.metrics = {
      total_users: 0,
      total_admins: 0,
      total_questions_asked: 0,
    }
  } finally {
    state.loading = false
  }
}

const deleteUser = async (userId) => {
  try {
    await AdminUserService.deleteUser(userId)
    await fetchUserData() // Refresh the user list
  } catch (error) {
    console.error('Error deleting user:', error)
    state.error = t('admin_user_manager.errors.delete_failed')
  }
}

const promoteToAdmin = async (userId) => {
  try {
    await AdminUserService.promoteToAdmin(userId)
    await fetchUserData() // Refresh the user list
  } catch (error) {
    console.error('Error promoting user:', error)
    state.error = t('admin_user_manager.errors.promote_failed')
  }
}

const sortUsers = (column) => {
  if (state.sortBy === column) {
    state.sortDirection = state.sortDirection === 'asc' ? 'desc' : 'asc'
  } else {
    state.sortBy = column
    state.sortDirection = 'asc'
  }
}

const filteredUsers = computed(() => {
  let users = [...state.users]

  if (state.searchQuery) {
    const query = state.searchQuery.toLowerCase()
    users = users.filter(
      (user) => user.name.toLowerCase().includes(query) || user.email.toLowerCase().includes(query),
    )
  }

  users.sort((a, b) => {
    let valA = a[state.sortBy]
    let valB = b[state.sortBy]

    if (typeof valA === 'string') {
      valA = valA.toLowerCase()
      valB = valB.toLowerCase()
    }

    if (valA < valB) return state.sortDirection === 'asc' ? -1 : 1
    if (valA > valB) return state.sortDirection === 'asc' ? 1 : -1
    return 0
  })

  return users
})

// Fetch data on component mount
onMounted(fetchUserData)
</script>

<template>
  <div class="app-container">
    <div class="main-area">
      <div v-if="state.loading" class="loading-spinner">
        <div class="spinner"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="state.error" class="error-message">
        {{ state.error }}
      </div>

      <!-- User data display -->
      <div v-else class="user-data-container">
        <!-- Metrics Cards -->
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-value">{{ $t('admin_user_manager.metrics.users_limit', { count: state.metrics.total_users }) }}</div>
            <div class="metric-label">{{ $t('admin_user_manager.metrics.total_users') }}</div>
          </div>

          <div class="metric-card">
            <div class="metric-value">{{ state.metrics.total_admins }}</div>
            <div class="metric-label">{{ $t('admin_user_manager.metrics.total_admins') }}</div>
          </div>

          <div class="metric-card">
            <div class="metric-value">{{ $t('admin_user_manager.metrics.questions_limit', { count: state.metrics.total_questions_asked }) }}</div>
            <div class="metric-label">{{ $t('admin_user_manager.metrics.total_questions') }}</div>
          </div>
        </div>

        <!-- Users Table -->
        <div class="table-section">
          <div class="table-header">
            <h2>{{ $t('admin_user_manager.user_list') }}</h2>
            <div class="table-actions">
              <input
                v-model="state.searchQuery"
                :placeholder="$t('admin_user_manager.search_users')"
                class="search-input"
              />
            </div>
          </div>

          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th @click="sortUsers('name')">
                    {{ $t('admin_user_manager.table.name') }}
                    <i
                      class="sort-icon"
                      :class="{
                        active: state.sortBy === 'name',
                        asc: state.sortBy === 'name' && state.sortDirection === 'asc',
                        desc: state.sortBy === 'name' && state.sortDirection === 'desc',
                      }"
                    ></i>
                  </th>
                  <th @click="sortUsers('email')">
                    {{ $t('admin_user_manager.table.email') }}
                    <i
                      class="sort-icon"
                      :class="{
                        active: state.sortBy === 'email',
                        asc: state.sortBy === 'email' && state.sortDirection === 'asc',
                        desc: state.sortBy === 'email' && state.sortDirection === 'desc',
                      }"
                    ></i>
                  </th>
                  <th @click="sortUsers('role')">
                    {{ $t('admin_user_manager.table.role') }}
                    <i
                      class="sort-icon"
                      :class="{
                        active: state.sortBy === 'role',
                        asc: state.sortBy === 'role' && state.sortDirection === 'asc',
                        desc: state.sortBy === 'role' && state.sortDirection === 'desc',
                      }"
                    ></i>
                  </th>
                  <th @click="sortUsers('questions_asked')">
                    {{ $t('admin_user_manager.table.questions') }}
                    <i
                      class="sort-icon"
                      :class="{
                        active: state.sortBy === 'questions_asked',
                        asc: state.sortBy === 'questions_asked' && state.sortDirection === 'asc',
                        desc: state.sortBy === 'questions_asked' && state.sortDirection === 'desc',
                      }"
                    ></i>
                  </th>
                  <th>{{ $t('admin_user_manager.table.actions') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.email">
                  <td>{{ user.name }}</td>
                  <td>{{ user.email }}</td>
                  <td>
                    <span class="role-badge" :class="user.role">
                      {{ user.role === 'ADMIN' ? $t('admin_user_manager.roles.admin') : $t('admin_user_manager.roles.user') }}
                    </span>
                  </td>
                  <td>{{ user.questions_asked }}</td>
                  <td class="actions-cell">
                    <button
                      v-if="user.role !== 'admin'"
                      class="action-btn promote-btn"
                      :title="$t('admin_user_manager.actions.promote_to_admin')"
                      @click="promoteToAdmin(user.id)"
                    >
                      <i class="fa-solid fa-user-shield"></i>
                    </button>
                    <button
                      class="action-btn delete-btn"
                      :title="$t('admin_user_manager.actions.delete_user')"
                      @click="deleteUser(user.id)"
                    >
                      <i class="fa-solid fa-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 84vh;
}

.main-area {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background-color: #fff;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 1.75rem;
  font-weight: bold;
  color: #333;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.promote-btn {
  color: #28a745;
  margin-right: 5px;
}

.promote-btn:hover {
  color: #218838;
}

.delete-btn:hover {
  color: #c82333;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-message {
  color: #dc3545;
  text-align: center;
  padding: 2rem;
  font-weight: bold;
}

.user-data-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Metrics styling */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.metric-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  text-align: center;
  border-top: 4px solid #c73659;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.metric-label {
  color: #666;
  font-size: 1rem;
}

/* Table section styling */
.table-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.table-header {
  padding: 1.25rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-header h2 {
  font-size: 1.25rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.table-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.btn-create {
  padding: 0.5rem 1rem;
  background: #c73659;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: #f8f9fa;
  text-align: left;
  padding: 0.75rem 1.25rem;
  font-weight: 600;
  color: #495057;
  border-bottom: 2px solid #e0e0e0;
  position: relative;
  cursor: pointer;
}

td {
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid #e0e0e0;
  color: #333;
}

tbody tr:hover {
  background-color: #f8f9fa;
}

/* Role badge styling */
.role-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.role-badge.user {
  background-color: #e3f2fd;
  color: #0069c0;
}

.role-badge.admin {
  background-color: #ffefc1;
  color: #b86e00;
}

/* Action buttons */
.actions-cell {
  white-space: nowrap;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.edit-btn {
  color: #007bff;
}

.delete-btn {
  color: #dc3545;
}

.action-btn:hover {
  transform: scale(1.1);
}

/* Sorting icons */
th {
  position: relative;
}

.sort-icon {
  display: inline-block;
  position: relative;
  width: 10px;
  height: 15px;
  margin-left: 5px;
  vertical-align: middle;
}

.sort-icon::before,
.sort-icon::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  opacity: 0.3;
}

.sort-icon::before {
  border-bottom: 5px solid #333;
  top: 0;
}

.sort-icon::after {
  border-top: 5px solid #333;
  bottom: 0;
}

.sort-icon.active::before {
  opacity: 0.3;
}

.sort-icon.active::after {
  opacity: 0.3;
}

.sort-icon.active.asc::before {
  opacity: 1;
}

.sort-icon.active.desc::after {
  opacity: 1;
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .table-actions {
    width: 100%;
    flex-direction: column;
  }

  .search-input {
    width: 100%;
  }

  .btn-create {
    width: 100%;
  }
}
</style>
