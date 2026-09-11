<template>
  <div class="kanban-page">
    <!-- Background -->
    <div class="background"></div>
    <div class="background-overlay"></div>

    <!-- App -->
    <div class="app-shell">
      <!-- Sidebar -->
      <aside class="sidebar glass">
        <div class="logo-icon"><span></span><span></span><span></span><span></span></div>

        <div class="sidebar-menu">
          <button class="side-button active">
            <svg viewBox="0 0 24 24">
              <rect x="3" y="3" width="7" height="7" rx="1" />
              <rect x="14" y="3" width="7" height="7" rx="1" />
              <rect x="3" y="14" width="7" height="7" rx="1" />
              <rect x="14" y="14" width="7" height="7" rx="1" />
            </svg>
          </button>
          <!-- Остальные кнопки sidebar... -->
        </div>

        <div class="sidebar-bottom">
          <button class="side-button"><span class="help">?</span></button>
          <button class="side-button">
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="3" />
              <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
            </svg>
          </button>
        </div>
      </aside>

      <!-- Main -->
      <main class="main">
        <!-- Header -->
        <header class="header glass">
          <div class="brand">
            <div class="brand-title">Kanbando</div>
          </div>

          <!-- Tabs -->
          <TabNavigation :tabs="tabs" :active-tab="activeTab" @change-tab="activeTab = $event" />

          <!-- Header actions -->
          <div class="header-actions">
            <button class="icon-button">
              <svg viewBox="0 0 24 24">
                <circle cx="11" cy="11" r="7" />
                <path d="M20 20l-4-4" />
              </svg>
            </button>
            <button class="icon-button">
              <svg viewBox="0 0 24 24">
                <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
                <path d="M10 21h4" />
              </svg>
            </button>
            <button class="icon-button">
              <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="3" />
                <path
                  d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-1.8 1.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V20h-2.5v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1-1.8-1.8.1-.1A1.7 1.7 0 0 0 8 15a1.7 1.7 0 0 0-1.5-1H6v-2.5h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1L9 6.7l.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.5V5h2.5v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1 1.8 1.8-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1h.1V14h-.1a1.7 1.7 0 0 0-1.5 1z"
                />
              </svg>
            </button>
            <div class="avatar">A</div>
          </div>
        </header>

        <!-- Toolbar -->
        <section class="toolbar">
          <div class="project-selector glass">
            <span>Проекты</span>
            <svg viewBox="0 0 24 24">
              <path d="M6 9l6 6 6-6" />
            </svg>
          </div>

          <button class="glass toolbar-button">
            <svg viewBox="0 0 24 24">
              <path d="M4 6h16M7 12h10M10 18h4" />
              <circle cx="8" cy="6" r="1.5" />
              <circle cx="15" cy="12" r="1.5" />
              <circle cx="12" cy="18" r="1.5" />
            </svg>
          </button>

          <div class="toolbar-spacer"></div>

          <button class="glass toolbar-button">
            <svg viewBox="0 0 24 24">
              <path d="M4 6h16M7 12h10M10 18h4" />
              <circle cx="8" cy="6" r="1.5" />
              <circle cx="15" cy="12" r="1.5" />
              <circle cx="12" cy="18" r="1.5" />
            </svg>
          </button>

          <button class="glass toolbar-button">
            <svg viewBox="0 0 24 24">
              <rect x="4" y="4" width="6" height="6" rx="1" />
              <rect x="14" y="4" width="6" height="6" rx="1" />
              <rect x="4" y="14" width="6" height="6" rx="1" />
              <rect x="14" y="14" width="6" height="6" rx="1" />
            </svg>
          </button>

          <button class="create-button" @click="createTask">
            <span>＋</span>
            Создать задачу
          </button>

          <button class="glass toolbar-button">
            <span class="dots">•••</span>
          </button>
        </section>

        <!-- Board -->
        <KanbanBoard
          :columns="columns"
          @column-settings="handleColumnSettings"
          @add-task="handleAddTask"
          @open-task="handleOpenTask"
          @add-subtask="handleAddSubtask"
        />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TabNavigation from './components/TabNavigation.vue'
import KanbanBoard from './components/KanbanBoard.vue'

const activeTab = ref('board')

const tabs = [
  {
    name: 'board',
    label: 'Доска',
    icon: '<rect x="4" y="4" width="16" height="16" rx="2" /><path d="M9 8h6M9 12h6M9 16h3" />',
  },
  {
    name: 'list',
    label: 'Список',
    icon: '<path d="M5 5h14v14H5z" /><path d="M8 9h8M8 13h8M8 17h5" />',
  },
  {
    name: 'calendar',
    label: 'Календарь',
    icon: '<rect x="4" y="5" width="16" height="15" rx="2" /><path d="M8 3v4M16 3v4M4 10h16" />',
  },
  {
    name: 'files',
    label: 'Файлы',
    icon: '<path d="M6 3h9l4 4v14H6z" /><path d="M14 3v5h5" />',
  },
  {
    name: 'reports',
    label: 'Отчёты',
    icon: '<path d="M4 19V5" /><path d="M4 19h16" /><path d="M7 15l4-4 3 2 5-6" />',
  },
]

const columns = ref([
  {
    id: 'backlog',
    title: 'Бэклог',
    tasks: [
      {
        id: 1,
        title: 'Редизайн главной страницы',
        tag: 'Дизайн',
        tagClass: 'purple',
        comments: 3,
        subtasks: 5,
        done: false,
      },
      {
        id: 2,
        title: 'Настроить уведомления',
        tag: 'Бэкенд',
        tagClass: 'pink',
        comments: 2,
        subtasks: 3,
        done: false,
      },
    ],
  },
  {
    id: 'in-progress',
    title: 'В работе',
    tasks: [
      {
        id: 3,
        title: 'Разработка канбан доски',
        tag: 'Фронтенд',
        tagClass: 'blue',
        comments: 2,
        subtasks: [
          { title: 'Вёрстка доски', completed: false },
          { title: 'Логика перетаскивания', completed: false },
          { title: 'Сохранение порядка', completed: false },
        ],
        done: false,
      },
    ],
  },
  {
    id: 'review',
    title: 'На проверке',
    tasks: [
      {
        id: 4,
        title: 'Личный кабинет пользователя',
        tag: 'Фронтенд',
        tagClass: 'blue',
        comments: 3,
        subtasks: 6,
        done: false,
      },
    ],
  },
  {
    id: 'done',
    title: 'Готово',
    tasks: [
      {
        id: 5,
        title: 'Авторизация и регистрация',
        tag: 'Бэкенд',
        tagClass: 'purple',
        comments: 2,
        subtasks: 5,
        done: true,
      },
    ],
  },
])

// Event handlers
const handleColumnSettings = (column) => {
  console.log('Settings for column:', column)
}

const handleAddTask = (columnId) => {
  console.log('Add task to column:', columnId)
}

const handleOpenTask = (task) => {
  console.log('Open task:', task)
}

const handleAddSubtask = (task) => {
  console.log('Add subtask to task:', task)
}

const createTask = () => {
  console.log('Create new task')
}
</script>

<style scoped>
/* Все стили из оригинального файла остаются здесь */
* {
  box-sizing: border-box;
}

.kanban-page {
  min-height: 100vh;
  color: #fff;
  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;
  overflow: hidden;
  position: relative;
}

.background {
  position: fixed;
  inset: 0;
  background-image: url('/kanban-bg.jpg');
  background-size: cover;
  background-position: center;
  transform: scale(1.03);
  z-index: -3;
}

.background-overlay {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(circle at 20% 25%, rgba(255, 184, 202, 0.24), transparent 30%),
    radial-gradient(circle at 75% 20%, rgba(128, 174, 255, 0.25), transparent 32%),
    linear-gradient(135deg, rgba(29, 35, 70, 0.38), rgba(71, 63, 104, 0.25));
  backdrop-filter: blur(2px);
  z-index: -2;
}

.glass {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.06));
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.18),
    0 12px 40px rgba(13, 19, 45, 0.12);
  backdrop-filter: blur(24px) saturate(130%);
  -webkit-backdrop-filter: blur(24px) saturate(130%);
  transition: all 0.3s ease;
}

.glass:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
  border-color: rgba(255, 255, 255, 0.25);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.25),
    0 16px 48px rgba(13, 19, 45, 0.18);
}

.app-shell {
  display: flex;
  min-height: 100vh;
  gap: 16px;
}

.main {
  flex: 1;
  min-width: 0;
}

/* Sidebar styles */
.sidebar {
  width: 76px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 14px 10px;
}

.logo-icon {
  width: 38px;
  height: 38px;
  display: grid;
  grid-template-columns: repeat(2, 9px);
  grid-template-rows: repeat(2, 9px);
  gap: 5px;
  align-content: center;
  justify-content: center;
  margin-bottom: 38px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo-icon:hover {
  transform: scale(1.1);
}

.logo-icon span {
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 3px;
  transition: border-color 0.3s ease;
}

.logo-icon:hover span {
  border-color: rgba(255, 255, 255, 1);
}

.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.sidebar-bottom {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.side-button {
  width: 48px;
  height: 48px;
  border: 1px solid transparent;
  background: transparent;
  border-radius: 15px;
  color: rgba(255, 255, 255, 0.78);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.side-button:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(20, 30, 70, 0.15);
}

.side-button svg {
  width: 21px;
  height: 21px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.6;
  transition: transform 0.2s ease;
}

.side-button:hover svg {
  transform: scale(1.1);
}

.side-button.active {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 8px 20px rgba(20, 30, 70, 0.12);
}

.help {
  width: 21px;
  height: 21px;
  border: 1.5px solid currentColor;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

/* Header styles */
.header {
  height: 84px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  padding: 0 18px 0 26px;
}

.brand {
  width: 220px;
}

.brand-title {
  font-size: 24px;
  font-weight: 500;
  letter-spacing: -0.5px;
  cursor: default;
  transition: opacity 0.2s ease;
}

.brand-title:hover {
  opacity: 0.8;
}

.header-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon-button {
  width: 48px;
  height: 48px;
  border: 1px solid rgba(255, 255, 255, 0.13);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.07);
  color: rgba(255, 255, 255, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.icon-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition:
    width 0.4s,
    height 0.4s;
  pointer-events: none;
}

.icon-button:active::before {
  width: 100px;
  height: 100px;
}

.icon-button:active {
  transform: scale(0.9) translateY(0);
  background: rgba(255, 255, 255, 0.2);
}

.icon-button:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(20, 30, 70, 0.2);
}

.icon-button svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.6;
  transition: transform 0.2s ease;
}

.icon-button:hover svg {
  transform: scale(1.15);
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.25));
  color: rgba(40, 50, 80, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.avatar:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
}
.avatar:active {
  transform: scale(0.9);
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.2);
}

/* Toolbar styles */
.toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 22px 6px 18px;
}

.project-selector {
  height: 50px;
  min-width: 140px;
  border-radius: 14px;
  padding: 0 17px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.project-selector:active {
  transform: scale(0.98);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.15));
}

.project-selector:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
  border-color: rgba(255, 255, 255, 0.25);
}

.project-selector svg {
  width: 17px;
  height: 17px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.7;
  transition: transform 0.2s ease;
}

.project-selector:hover svg {
  transform: rotate(180deg);
}

.toolbar-spacer {
  flex: 1;
}

.toolbar-button {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  color: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.toolbar-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition:
    width 0.4s,
    height 0.4s;
  pointer-events: none;
}

.toolbar-button:active::before {
  width: 100px;
  height: 100px;
}

.toolbar-button:active {
  transform: scale(0.9) translateY(0);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.15));
}

.toolbar-button:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
  border-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(20, 30, 70, 0.15);
}

.toolbar-button svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  transition: transform 0.2s ease;
}

.toolbar-button:hover svg {
  transform: scale(1.1);
}

.dots {
  font-size: 18px;
  letter-spacing: 2px;
}

.create-button {
  height: 50px;
  padding: 0 22px;
  border: 1px solid rgba(255, 255, 255, 0.45);
  border-radius: 14px;
  background: rgba(240, 246, 255, 0.78);
  color: #34405e;
  font-size: 14px;
  font-weight: 600;
  box-shadow:
    0 8px 25px rgba(24, 34, 70, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  gap: 7px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.create-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(52, 64, 94, 0.2);
  transform: translate(-50%, -50%);
  transition:
    width 0.5s,
    height 0.5s;
  pointer-events: none;
}

.create-button:active::before {
  width: 300px;
  height: 300px;
}

.create-button:active {
  transform: scale(0.95) translateY(0);
  background: rgba(240, 246, 255, 0.9);
}

.create-button:active span {
  transform: rotate(0deg) scale(0.9);
}

.create-button:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-2px);
  box-shadow:
    0 12px 32px rgba(24, 34, 70, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.create-button span {
  font-size: 22px;
  font-weight: 300;
  transition: transform 0.2s ease;
}

.create-button:hover span {
  transform: rotate(90deg);
}

/* Responsive */
@media (max-width: 1250px) {
  .brand {
    width: 150px;
  }
  .tab {
    padding: 0 12px;
  }
  .tab:not(.active) {
    font-size: 0;
  }
  .tab:not(.active) svg {
    margin: 0;
  }
}

@media (max-width: 1000px) {
  .header {
    flex-wrap: wrap;
    height: auto;
    min-height: 84px;
    padding: 15px;
    gap: 10px;
  }
  .brand {
    width: auto;
  }
  .tabs {
    order: 3;
    width: 100%;
    justify-content: center;
  }
  .header-actions {
    margin-left: auto;
  }
}

@media (max-width: 700px) {
  .app-shell {
    padding: 10px;
  }
  .sidebar {
    display: none;
  }
  .toolbar {
    flex-wrap: wrap;
  }
  .toolbar-spacer {
    display: none;
  }
  .project-selector {
    flex: 1;
  }
  .tabs {
    overflow-x: auto;
    justify-content: flex-start;
  }
  .tab {
    flex-shrink: 0;
  }
  .header-actions .icon-button:nth-child(-n + 2) {
    display: none;
  }

  .side-button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition:
      width 0.4s,
      height 0.4s;
    pointer-events: none;
  }

  .side-button:active::before {
    width: 100px;
    height: 100px;
  }

  .side-button:active {
    transform: scale(0.9) translateY(0);
    background: rgba(255, 255, 255, 0.15);
  }
}
.logo-icon:active {
  transform: scale(0.95);
}

.logo-icon:active span {
  border-color: rgba(255, 255, 255, 1);
  animation: logoPulse 0.3s ease;
}

@keyframes logoPulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}
</style>
