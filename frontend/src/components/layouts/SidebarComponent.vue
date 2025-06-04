<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true,
    default: () => []
  },
  selectedItemId: {
    type: [String, Number],
    default: null
  },
  searchQuery: {
    type: String,
    default: ''
  },
  searchPlaceholder: {
    type: String,
    default: 'Search...'
  },
  newItemButtonText: {
    type: String,
    default: 'New Item'
  },
  showNewItemButton: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits([
  'update:searchQuery',
  'itemSelected',
  'newItemClick'
])

const handleItemClick = (item) => {
  emit('itemSelected', item)
}

const handleSearchInput = (event) => {
  emit('update:searchQuery', event.target.value)
}

const handleNewItemClick = () => {
  emit('newItemClick')
}
</script>

<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <input
        :value="searchQuery"
        @input="handleSearchInput"
        :placeholder="searchPlaceholder"
        class="search-input"
      />
      <button 
        v-if="showNewItemButton"
        @click="handleNewItemClick" 
        class="new-item-btn"
      >
        {{ newItemButtonText }}
      </button>
    </div>

    <div class="item-list">
      <div
        v-for="item in items"
        :key="item.id"
        @click="handleItemClick(item)"
        :class="['item', { active: item.id === selectedItemId }]"
      >
        {{ item.name }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 280px;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.new-item-btn {
  width: 100%;
  padding: 0.5rem;
  background: #0395ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.item-list {
  flex: 1;
  overflow-y: auto;
}

.item {
  padding: 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.item:hover {
  background: #f5f5f5;
}

.item.active {
  background: #e3f2fd;
}
</style>
