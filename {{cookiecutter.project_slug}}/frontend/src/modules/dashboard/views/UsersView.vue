<template>
  <div class="p-8 max-w-7xl mx-auto">
    <div class="page-header">
      <h1 class="page-title">Users</h1>
      <button @click="showAddUserModal = true" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        Add User
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-box">
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Search users..."
          class="search-input"
        >
      </div>
      
      <div class="filter-group">
        <select v-model="roleFilter" class="filter-select">
          <option value="">All Roles</option>
          <option value="admin">Admin</option>
          <option value="manager">Manager</option>
          <option value="user">User</option>
        </select>
        
        <select v-model="statusFilter" class="filter-select">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="pending">Pending</option>
        </select>
      </div>
    </div>

    <!-- Users Table -->
    <div class="table-card">
      <div class="table-wrapper">
        <table class="users-table">
          <thead>
            <tr>
              <th>
                <input type="checkbox" v-model="selectAll" @change="toggleSelectAll">
              </th>
              <th @click="sortBy('name')" class="sortable">
                Name
                <span class="sort-icon">{% raw %}{{ getSortIcon('name') }}{% endraw %}</span>
              </th>
              <th @click="sortBy('email')" class="sortable">
                Email
                <span class="sort-icon">{% raw %}{{ getSortIcon('email') }}{% endraw %}</span>
              </th>
              <th>Role</th>
              <th>Status</th>
              <th @click="sortBy('lastActive')" class="sortable">
                Last Active
                <span class="sort-icon">{% raw %}{{ getSortIcon('lastActive') }}{% endraw %}</span>
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td>
                <input type="checkbox" v-model="selectedUsers" :value="user.id">
              </td>
              <td>
                <div class="user-info">
                  <img v-if="user.avatar" :src="user.avatar" :alt="user.name" class="user-avatar">
                  <div v-else class="avatar-placeholder">
                    {% raw %}{{ getInitials(user.name) }}{% endraw %}
                  </div>
                  <div>
                    <div class="user-name">{% raw %}{{ user.name }}{% endraw %}</div>
                    <div class="user-subtitle">{% raw %}{{ user.department }}{% endraw %}</div>
                  </div>
                </div>
              </td>
              <td>{% raw %}{{ user.email }}{% endraw %}</td>
              <td>
                <span :class="['role-badge', `role-${user.role}`]">
                  {% raw %}{{ user.role }}{% endraw %}
                </span>
              </td>
              <td>
                <span :class="['status-badge', `status-${user.status}`]">
                  {% raw %}{{ user.status }}{% endraw %}
                </span>
              </td>
              <td>{% raw %}{{ formatDate(user.lastActive) }}{% endraw %}</td>
              <td>
                <div class="action-buttons">
                  <button @click="editUser(user)" class="btn-icon" title="Edit">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                  <button @click="deleteUser(user)" class="btn-icon danger" title="Delete">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination">
        <div class="pagination-info">
          Showing {% raw %}{{ startIndex + 1 }}{% endraw %} to {% raw %}{{ endIndex }}{% endraw %} of {% raw %}{{ filteredUsers.length }}{% endraw %} users
        </div>
        <div class="pagination-controls">
          <button 
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            Previous
          </button>
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="currentPage = page"
            :class="['pagination-btn', { active: currentPage === page }]"
          >
            {% raw %}{{ page }}{% endraw %}
          </button>
          <button 
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="pagination-btn"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit User Modal -->
    <div v-if="showAddUserModal || editingUser" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2 class="modal-title">{% raw %}{{ editingUser ? 'Edit User' : 'Add New User' }}{% endraw %}</h2>
          <button @click="closeModal" class="modal-close">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveUser" class="modal-body">
          <div class="form-grid">
            <div class="mb-6">
              <label for="userName">Name</label>
              <input 
                id="userName"
                v-model="userForm.name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
            </div>
            <div class="mb-6">
              <label for="userEmail">Email</label>
              <input 
                id="userEmail"
                v-model="userForm.email"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
            </div>
            <div class="mb-6">
              <label for="userDepartment">Department</label>
              <input 
                id="userDepartment"
                v-model="userForm.department"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
              >
            </div>
            <div class="mb-6">
              <label for="userRole">Role</label>
              <select 
                id="userRole"
                v-model="userForm.role"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
                <option value="user">User</option>
                <option value="manager">Manager</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div class="mb-6">
              <label for="userStatus">Status</label>
              <select 
                id="userStatus"
                v-model="userForm.status"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="pending">Pending</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:bg-gray-700 dark:text-gray-300">
              Cancel
            </button>
            <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors">
              {% raw %}{{ editingUser ? 'Update User' : 'Add User' }}{% endraw %}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
{% if cookiecutter.use_typescript == 'y' -%}
import { ref, computed, reactive } from 'vue'

interface User {
  id: string
  name: string
  email: string
  avatar?: string
  department: string
  role: 'admin' | 'manager' | 'user'
  status: 'active' | 'inactive' | 'pending'
  lastActive: Date
}

interface UserForm {
  name: string
  email: string
  department: string
  role: 'admin' | 'manager' | 'user'
  status: 'active' | 'inactive' | 'pending'
}
{% else -%}
import { ref, computed, reactive } from 'vue'
{%- endif %}

const searchQuery = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = 10
const selectAll = ref(false)
const selectedUsers = ref([])
const showAddUserModal = ref(false)
const editingUser = ref(null)
const sortColumn = ref('name')
const sortDirection = ref('asc')

const userForm = reactive({% if cookiecutter.use_typescript == 'y' %}<UserForm>{% endif %}{
  name: '',
  email: '',
  department: '',
  role: 'user',
  status: 'active'
})

const users = ref({% if cookiecutter.use_typescript == 'y' %}<User[]>{% endif %}[
  {
    id: '1',
    name: 'John Doe',
    email: 'john.doe@example.com',
    avatar: '',
    department: 'Engineering',
    role: 'admin',
    status: 'active',
    lastActive: new Date('2024-01-15T10:30:00')
  },
  {
    id: '2',
    name: 'Jane Smith',
    email: 'jane.smith@example.com',
    avatar: '',
    department: 'Marketing',
    role: 'manager',
    status: 'active',
    lastActive: new Date('2024-01-15T14:45:00')
  },
  {
    id: '3',
    name: 'Bob Johnson',
    email: 'bob.johnson@example.com',
    avatar: '',
    department: 'Sales',
    role: 'user',
    status: 'inactive',
    lastActive: new Date('2024-01-10T09:15:00')
  },
  {
    id: '4',
    name: 'Alice Williams',
    email: 'alice.williams@example.com',
    avatar: '',
    department: 'HR',
    role: 'manager',
    status: 'active',
    lastActive: new Date('2024-01-15T16:20:00')
  },
  {
    id: '5',
    name: 'Charlie Brown',
    email: 'charlie.brown@example.com',
    avatar: '',
    department: 'Engineering',
    role: 'user',
    status: 'pending',
    lastActive: new Date('2024-01-12T11:00:00')
  }
])

const filteredUsers = computed(() => {
  let result = [...users.value]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(user => 
      user.name.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query) ||
      user.department.toLowerCase().includes(query)
    )
  }
  
  // Apply role filter
  if (roleFilter.value) {
    result = result.filter(user => user.role === roleFilter.value)
  }
  
  // Apply status filter
  if (statusFilter.value) {
    result = result.filter(user => user.status === statusFilter.value)
  }
  
  // Apply sorting
  result.sort((a, b) => {
    let aVal = a[sortColumn.value]
    let bVal = b[sortColumn.value]
    
    if (sortColumn.value === 'lastActive') {
      aVal = aVal.getTime()
      bVal = bVal.getTime()
    } else if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase()
      bVal = bVal.toLowerCase()
    }
    
    if (sortDirection.value === 'asc') {
      return aVal > bVal ? 1 : -1
    } else {
      return aVal < bVal ? 1 : -1
    }
  })
  
  return result
})

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / itemsPerPage))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, filteredUsers.value.length))

const paginatedUsers = computed(() => {
  return filteredUsers.value.slice(startIndex.value, endIndex.value)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const getInitials = (name) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase()
}

const formatDate = (date) => {
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) {
    const hours = Math.floor(diff / (1000 * 60 * 60))
    if (hours === 0) {
      const minutes = Math.floor(diff / (1000 * 60))
      return `${minutes} minutes ago`
    }
    return `${hours} hours ago`
  } else if (days === 1) {
    return 'Yesterday'
  } else if (days < 7) {
    return `${days} days ago`
  } else {
    return date.toLocaleDateString()
  }
}

const sortBy = (column) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
}

const getSortIcon = (column) => {
  if (sortColumn.value !== column) return '↕'
  return sortDirection.value === 'asc' ? '↑' : '↓'
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedUsers.value = paginatedUsers.value.map(u => u.id)
  } else {
    selectedUsers.value = []
  }
}

const editUser = (user) => {
  editingUser.value = user
  userForm.name = user.name
  userForm.email = user.email
  userForm.department = user.department
  userForm.role = user.role
  userForm.status = user.status
}

const deleteUser = (user) => {
  if (confirm(`Are you sure you want to delete ${user.name}?`)) {
    const index = users.value.findIndex(u => u.id === user.id)
    if (index > -1) {
      users.value.splice(index, 1)
    }
  }
}

const saveUser = () => {
  if (editingUser.value) {
    // Update existing user
    const index = users.value.findIndex(u => u.id === editingUser.value.id)
    if (index > -1) {
      users.value[index] = {
        ...users.value[index],
        ...userForm
      }
    }
  } else {
    // Add new user
    users.value.push({
      id: Date.now().toString(),
      ...userForm,
      avatar: '',
      lastActive: new Date()
    })
  }
  closeModal()
}

const closeModal = () => {
  showAddUserModal.value = false
  editingUser.value = null
  userForm.name = ''
  userForm.email = ''
  userForm.department = ''
  userForm.role = 'user'
  userForm.status = 'active'
}
</script>

