<template>
  <div class="app">
    <!-- =========================================
       SIDEBAR
  ========================================== -->
    <aside class="sidebar">
      <div class="logo">
        <img width="100%" src="@/assets/images/logo.png" alt="Logo" />
      </div>

      <nav class="nav">
        <a
          v-for="item in navItems"
          :key="item.label"
          :class="['nav-link', { active: item.active }]"
          :href="item.href"
          @click.prevent
        >
          <iconify-icon class="icon" :icon="item.icon"></iconify-icon>
          <span>{{ item.label }}</span>
          <span v-if="item.counter" class="nav-counter">{{ item.counter }}</span>
        </a>
      </nav>

      <div class="sidebar-user">
        <div class="avatar">
          <img :src="currentUser.avatar" :alt="currentUser.name" />
        </div>
        <div class="user-meta">
          {{ currentUser.name }}
          <small>{{ currentUser.role }}</small>
        </div>
      </div>
    </aside>

    <!-- =========================================
       MAIN
  ========================================== -->
    <main class="main">
      <!-- TOPBAR -->
      <header class="topbar">
        <div class="search-wrap">
          <iconify-icon icon="solar:magnifer-outline"></iconify-icon>
          <input v-model="searchQuery" class="search" placeholder="Поиск задач, проектов..." />
        </div>
        <button class="icon-btn" aria-label="Уведомления">
          <iconify-icon icon="solar:bell-outline"></iconify-icon>
        </button>
        <button class="icon-btn" aria-label="Приложения">
          <iconify-icon icon="solar:widget-2-outline"></iconify-icon>
        </button>
        <div class="profile">
          <img :src="currentUser.avatar" :alt="currentUser.name" />
        </div>
      </header>

      <section class="content">
        <!-- PROJECT HEADER -->
        <div class="project-head">
          <div>
            <a href="#" class="crumb" @click.prevent>
              <iconify-icon icon="solar:arrow-left-outline"></iconify-icon>
              Назад к проектам
            </a>
            <h1>
              {{ project.title }}
              <span class="status-badge">{{ project.status }}</span>
            </h1>
            <div class="subtitle">{{ project.subtitle }}</div>
          </div>
          <div class="head-actions">
            <button class="btn" @click="$emit('edit')">
              <iconify-icon icon="solar:pen-outline"></iconify-icon>
              Редактировать
            </button>
            <button class="btn btn-more" aria-label="Дополнительно">
              <iconify-icon icon="solar:menu-dots-outline"></iconify-icon>
            </button>
            <button class="btn primary" @click="$emit('add-task')">
              <iconify-icon icon="solar:add-circle-outline"></iconify-icon>
              Добавить задачу
            </button>
          </div>
        </div>

        <!-- META -->
        <section class="project-meta">
          <div v-for="item in projectMeta" :key="item.label" class="meta-item">
            <iconify-icon class="meta-icon" :icon="item.icon"></iconify-icon>
            <div class="meta-content">
              <div class="meta-value">{{ item.value }}</div>
              <div class="meta-label">{{ item.label }}</div>
            </div>
          </div>
        </section>

        <!-- TABS -->
        <div class="tabs">
          <a
            v-for="tab in tabs"
            :key="tab.key"
            href="#"
            :class="['tab', { active: activeTab === tab.key }]"
            @click.prevent="activeTab = tab.key"
          >
            {{ tab.label }}
            <span v-if="tab.count" class="tab-count">{{ tab.count }}</span>
          </a>
        </div>

        <!-- CONTENT GRID -->
        <div class="content-grid">
          <!-- LEFT -->
          <div class="left-column">
            <!-- DESCRIPTION -->
            <section class="card">
              <div class="card-header">
                <div class="card-title">
                  <iconify-icon icon="solar:document-text-outline"></iconify-icon>
                  Описание проекта
                </div>
                <div class="card-edit" @click="$emit('edit-description')">
                  <iconify-icon icon="solar:pen-outline"></iconify-icon>
                  Редактировать
                </div>
              </div>
              <div class="description">
                <p>{{ project.description }}</p>
              </div>
            </section>

            <!-- DOCUMENTATION -->
            <section class="card">
              <div class="card-header docs-header">
                <div class="card-title">
                  <iconify-icon icon="solar:file-text-outline"></iconify-icon>
                  Документация
                </div>
                <button class="upload-btn" @click="$emit('upload')">
                  <iconify-icon icon="solar:upload-outline"></iconify-icon>
                  Загрузить файл
                </button>
              </div>
              <div class="documents">
                <div class="doc-row header">
                  <div>Название</div>
                  <div>Тип</div>
                  <div>Размер</div>
                  <div class="hide-mobile">Дата загрузки</div>
                  <div class="hide-mobile">Автор</div>
                  <div></div>
                </div>
                <div v-for="doc in documents" :key="doc.name" class="doc-row">
                  <div class="doc-name">
                    <div :class="['file-icon', `file-${doc.kind}`]">
                      <iconify-icon icon="solar:file-text-outline"></iconify-icon>
                    </div>
                    <span>{{ doc.name }}</span>
                  </div>
                  <div class="doc-cell">{{ doc.type }}</div>
                  <div class="doc-cell">{{ doc.size }}</div>
                  <div class="doc-cell hide-mobile">{{ doc.uploadedAt }}</div>
                  <div class="doc-cell hide-mobile">{{ doc.author }}</div>
                  <iconify-icon class="doc-more" icon="solar:menu-dots-outline"></iconify-icon>
                </div>
              </div>
            </section>

            <!-- COSTS -->
            <section class="card">
              <div class="card-header">
                <div class="card-title">
                  <iconify-icon icon="solar:wallet-money-outline"></iconify-icon>
                  Затраты
                </div>
                <div class="card-edit" @click="$emit('edit-costs')">
                  <iconify-icon icon="solar:pen-outline"></iconify-icon>
                  Редактировать
                </div>
              </div>
              <div class="costs-content">
                <div class="total-cost">
                  <div class="total-label">Общие затраты</div>
                  <div class="total-value">{{ formatMoney(totalCost) }}</div>
                </div>
                <div class="cost-chart">
                  <div class="bar">
                    <div
                      v-for="cost in costs"
                      :key="cost.name"
                      class="bar-part"
                      :class="cost.barClass"
                    ></div>
                  </div>
                  <div class="cost-list">
                    <div v-for="cost in costs" :key="cost.name" class="cost-row">
                      <div class="cost-name">
                        <span class="cost-dot" :class="cost.dotClass"></span>
                        {{ cost.name }}
                      </div>
                      <div class="cost-amount">{{ formatMoney(cost.amount) }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- RIGHT -->
          <aside class="right-column">
            <!-- TEAM -->
            <section class="card right-card">
              <div class="card-header">
                <div class="card-title">
                  <iconify-icon icon="solar:users-group-rounded-outline"></iconify-icon>
                  Участники проекта
                </div>
              </div>
              <div class="team-list">
                <div v-for="member in team" :key="member.name" class="team-member">
                  <div class="team-avatar">
                    <img :src="member.avatar" :alt="member.name" />
                  </div>
                  <div class="member-info">
                    <div class="member-name">{{ member.name }}</div>
                    <div class="member-role">{{ member.role }}</div>
                  </div>
                  <span class="member-badge" :class="member.badgeClass">
                    {{ member.badge }}
                  </span>
                  <iconify-icon class="member-more" icon="solar:menu-dots-outline"></iconify-icon>
                </div>
                <div class="add-member" @click="$emit('add-member')">
                  <iconify-icon icon="solar:add-circle-outline"></iconify-icon>
                  Добавить участника
                </div>
              </div>
            </section>

            <!-- DEADLINE -->
            <section class="card right-card">
              <div class="card-header">
                <div class="card-title">
                  <iconify-icon icon="solar:calendar-outline"></iconify-icon>
                  Сроки и статус
                </div>
              </div>
              <div class="deadline-content">
                <div class="progress-top">
                  <div class="progress" style="width: 100%">
                    <div class="progress-value" :style="{ width: project.progress + '%' }"></div>
                  </div>
                </div>
                <div class="progress-percent-wrap">
                  <span class="progress-percent">{{ project.progress }}%</span>
                </div>
                <div class="deadline-info">
                  <div class="deadline-item">
                    <div class="deadline-label">Начало</div>
                    <div class="deadline-value">{{ project.startDate }}</div>
                  </div>
                  <div class="deadline-item">
                    <div class="deadline-label">Окончание</div>
                    <div class="deadline-value">{{ project.endDate }}</div>
                  </div>
                  <div class="deadline-item">
                    <div class="deadline-label">Осталось</div>
                    <div class="deadline-value">{{ project.daysLeft }} дня</div>
                  </div>
                </div>
              </div>
            </section>

            <!-- QUICK ACTIONS -->
            <section class="card right-card">
              <div class="card-header">
                <div class="card-title">
                  <iconify-icon icon="solar:bolt-outline"></iconify-icon>
                  Быстрые действия
                </div>
              </div>
              <div class="quick-list">
                <div
                  v-for="action in quickActions"
                  :key="action.label"
                  class="quick-item"
                  @click="$emit(action.event)"
                >
                  <iconify-icon :icon="action.icon"></iconify-icon>
                  {{ action.label }}
                  <iconify-icon
                    class="quick-arrow"
                    icon="solar:alt-arrow-right-outline"
                  ></iconify-icon>
                </div>
              </div>
            </section>
          </aside>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import '@/assets/styles/ProgectInfoVue.css'

/* ---------- EMITS ---------- */
defineEmits([
  'edit',
  'edit-description',
  'edit-costs',
  'add-task',
  'add-member',
  'upload',
  'change-status',
  'upload-docs',
  'add-cost',
])

/* ---------- LOCAL STATE ---------- */
const searchQuery = ref('')
const activeTab = ref('overview')

/* ---------- CURRENT USER ---------- */
const currentUser = {
  name: 'Иван Петров',
  role: 'Frontend Developer',
  avatar: 'https://i.pravatar.cc/100?img=12',
}

/* ---------- NAV ---------- */
const navItems = [
  {
    label: 'Проекты',
    icon: 'solar:folder-with-files-outline',
    counter: 3,
    active: true,
    href: '#',
  },
  { label: 'Мои задачи', icon: 'solar:checklist-minimalistic-outline', counter: 15, href: '#' },
  { label: 'Канбан', icon: 'solar:kanban-board-outline', href: '#' },
  { label: 'Календарь', icon: 'solar:calendar-outline', href: '#' },
  { label: 'Отчёты', icon: 'solar:chart-2-outline', href: '#' },
  { label: 'Настройки', icon: 'solar:settings-outline', href: '#' },
]

/* ---------- PROJECT ---------- */
const project = ref({
  title: 'Проект №2-2394',
  status: 'В работе',
  subtitle: 'Разработка системы автоматизации производства',
  description:
    'Разработка системы автоматизации производства, которая позволит оптимизировать производственные процессы, сократить время на выполнение операций и повысить точность планирования. Система будет интегрирована с существующими модулями и предоставит удобный интерфейс для сотрудников цехов и менеджеров.',
  startDate: '10.01.2026',
  endDate: '25.10.2026',
  daysLeft: 84,
  progress: 58,
})

const projectMeta = [
  { icon: 'solar:calendar-outline', value: '10.01.2026 – 25.10.2026', label: 'Срок выполнения' },
  { icon: 'solar:database-outline', value: '2 652 000 ₽', label: 'Затраты на разработку' },
  { icon: 'solar:users-group-rounded-outline', value: '5', label: 'Исполнители' },
  { icon: 'solar:user-outline', value: 'Иванов А.С.', label: 'Инициатор' },
  { icon: 'solar:user-check-outline', value: 'Петров И.В.', label: 'Менеджер проекта' },
]

/* ---------- TABS ---------- */
const tabs = [
  { key: 'overview', label: 'Обзор' },
  { key: 'tasks', label: 'Задачи', count: 20 },
  { key: 'docs', label: 'Документация', count: 5 },
  { key: 'costs', label: 'Затраты' },
  { key: 'team', label: 'Команда' },
  { key: 'history', label: 'История' },
]

/* ---------- DOCUMENTS ---------- */
const documents = [
  {
    name: 'Техническое задание.pdf',
    kind: 'pdf',
    type: 'ТЗ',
    size: '2.4 МБ',
    uploadedAt: '10.01.2026 14:32',
    author: 'Иванов А.С.',
  },
  {
    name: 'Архитектура системы.docx',
    kind: 'word',
    type: 'Документация',
    size: '1.8 МБ',
    uploadedAt: '12.01.2026 09:15',
    author: 'Петров И.В.',
  },
  {
    name: 'План-график реализации.xlsx',
    kind: 'excel',
    type: 'План',
    size: '320 КБ',
    uploadedAt: '13.01.2026 16:24',
    author: 'Сидоров Д.В.',
  },
  {
    name: 'Договор №2-2394.pdf',
    kind: 'pdf',
    type: 'Договор',
    size: '1.1 МБ',
    uploadedAt: '15.01.2026 11:03',
    author: 'Иванов А.С.',
  },
  {
    name: 'Протокол совещания.docx',
    kind: 'word',
    type: 'Прочее',
    size: '856 КБ',
    uploadedAt: '18.01.2026 15:47',
    author: 'Петров И.В.',
  },
]

/* ---------- COSTS ---------- */
const costs = [
  { name: 'Разработка', amount: 1_850_000, barClass: 'bar-development', dotClass: 'dot-blue' },
  { name: 'Тестирование', amount: 450_000, barClass: 'bar-testing', dotClass: 'dot-green' },
  { name: 'Внедрение', amount: 250_000, barClass: 'bar-implementation', dotClass: 'dot-green2' },
  { name: 'Прочее', amount: 102_000, barClass: 'bar-other', dotClass: 'dot-purple' },
]

const totalCost = computed(() => costs.reduce((sum, c) => sum + c.amount, 0))

/* ---------- TEAM ---------- */
const team = [
  {
    name: 'Иванов Александр Сергеевич',
    role: 'Инициатор',
    badge: 'Инициатор',
    badgeClass: '',
    avatar: 'https://i.pravatar.cc/100?img=47',
  },
  {
    name: 'Петров Иван Владимирович',
    role: 'Менеджер проекта',
    badge: 'Менеджер',
    badgeClass: '',
    avatar: 'https://i.pravatar.cc/100?img=11',
  },
  {
    name: 'Смирнов Алексей Викторович',
    role: 'Разработчик',
    badge: 'Исполнитель',
    badgeClass: 'green',
    avatar: 'https://i.pravatar.cc/100?img=13',
  },
  {
    name: 'Кузнецова Мария Сергеевна',
    role: 'Тестировщик',
    badge: 'Исполнитель',
    badgeClass: 'green',
    avatar: 'https://i.pravatar.cc/100?img=32',
  },
  {
    name: 'Васильев Дмитрий Николаевич',
    role: 'Разработчик',
    badge: 'Исполнитель',
    badgeClass: 'green',
    avatar: 'https://i.pravatar.cc/100?img=68',
  },
]

/* ---------- QUICK ACTIONS ---------- */
const quickActions = [
  { icon: 'solar:refresh-outline', label: 'Изменить статус проекта', event: 'change-status' },
  { icon: 'solar:add-circle-outline', label: 'Добавить задачу', event: 'add-task' },
  { icon: 'solar:upload-outline', label: 'Загрузить документацию', event: 'upload-docs' },
  { icon: 'solar:wallet-money-outline', label: 'Добавить затраты', event: 'add-cost' },
]

/* ---------- HELPERS ---------- */
function formatMoney(value) {
  return new Intl.NumberFormat('ru-RU').format(value) + ' ₽'
}
</script>

<style scoped>
/* @import '@/assets/styles/ProgectInfoVue.css'; */

/* Inline-стиль для статуса проекта переносим сюда */
.status-badge {
  font-size: 11px;
  background: #e7f5ff;
  color: #168be5;
  padding: 5px 9px;
  border-radius: 20px;
  vertical-align: middle;
}

/* Inline-стиль для блока прогресса */
.progress-percent-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: -25px;
  margin-bottom: 10px;
}
</style>
