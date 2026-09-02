<template>
  <div class="py-4">
    <!-- Приветствие -->
    <div class="text-center mb-5">
      <h1 class="h3 mb-2" style="color: #1e293b; font-weight: 600">
        👋 С возвращением,
        <!-- {{ agent.full_name }}! -->
      </h1>
    </div>

    <!-- Быстрые действия -->
    <div class="row g-4 justify-content-center mb-5">
      <div class="col-md-4">
        <router-link to="/login" class="text-decoration-none">
          <div class="card h-100 card-border-primary">
            <div class="card-body text-center p-4">
              <!-- <div class="mb-3" style="font-size: 2.5rem">📋</div> -->
              <h3 class="h6 mb-2">Авторизация</h3>
              <p class="text-muted mb-3 small">/login</p>
            </div>
          </div>
        </router-link>

        <router-link to="/projects" class="text-decoration-none">
          <div class="card h-100 card-border-primary">
            <div class="card-body text-center p-4">
              <!-- <div class="mb-3" style="font-size: 2.5rem">📋</div> -->
              <h3 class="h6 mb-2">Проекты</h3>
              <p class="text-muted mb-3 small">/projects</p>
            </div>
          </div>
        </router-link>

        <router-link to="/tabs" class="text-decoration-none">
          <div class="card h-100 card-border-primary">
            <div class="card-body text-center p-4">
              <!-- <div class="mb-3" style="font-size: 2.5rem">📋</div> -->
              <h3 class="h6 mb-2">Вкладки</h3>
              <p class="text-muted mb-3 small">/tabs</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Типы данных
interface Agent {
  full_name: string
  role?: string
  department?: {
    name: string
  } | null
}

interface Stats {
  total_my_tickets: number
  in_progress: number
  awaiting_response: number
  solved_today: number
}

// Props
const props = defineProps<{
  agent: Agent
  stats: Stats
}>()

// Можно добавить вычисляемые свойства при необходимости
// const userRole = computed(() => props.agent.role || 'operator')
// const departmentName = computed(() => props.agent.department?.name || '—')
</script>

<style scoped>
.card-border-primary {
  border-left: 3px solid #2563eb !important;
}

.text-decoration-none:hover {
  opacity: 0.9;
  transition: opacity 0.2s ease;
}
</style>
