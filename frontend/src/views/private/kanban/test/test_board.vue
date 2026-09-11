<template>
  <div class="kanban-page">
    <!-- Background -->
    <div class="background"></div>
    <div class="background-overlay"></div>

    <!-- App -->
    <div class="app-shell">
      <!-- Sidebar -->
      <aside class="sidebar glass">
        <div class="logo-icon">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>

        <div class="sidebar-menu">
          <button class="side-button active">
            <svg viewBox="0 0 24 24">
              <rect x="3" y="3" width="7" height="7" rx="1" />
              <rect x="14" y="3" width="7" height="7" rx="1" />
              <rect x="3" y="14" width="7" height="7" rx="1" />
              <rect x="14" y="14" width="7" height="7" rx="1" />
            </svg>
          </button>

          <button class="side-button">
            <svg viewBox="0 0 24 24">
              <path d="M4 5h16v14H4z" />
              <path d="M8 9h8M8 13h5" />
            </svg>
          </button>

          <button class="side-button">
            <svg viewBox="0 0 24 24">
              <path d="M4 5h16v14H4z" />
              <path d="M8 9h8M8 13h5" />
            </svg>
          </button>

          <button class="side-button">
            <svg viewBox="0 0 24 24">
              <path d="M4 19V5" />
              <path d="M4 19h16" />
              <path d="M7 15l4-4 3 2 5-6" />
            </svg>
          </button>

          <button class="side-button">
            <svg viewBox="0 0 24 24">
              <circle cx="9" cy="8" r="3" />
              <circle cx="17" cy="10" r="3" />
              <path d="M3 20c0-3 2.5-5 6-5s6 2 6 5" />
              <path d="M14 16c3 0 5 1.5 6 4" />
            </svg>
          </button>
        </div>

        <div class="sidebar-bottom">
          <button class="side-button">
            <span class="help">?</span>
          </button>

          <button class="side-button">
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="3" />
              <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
              <path d="M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1" />
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
          <nav class="tabs">
            <button class="tab active">
              <svg viewBox="0 0 24 24">
                <rect x="4" y="4" width="16" height="16" rx="2" />
                <path d="M9 8h6M9 12h6M9 16h3" />
              </svg>
              Доска
            </button>

            <button class="tab">
              <svg viewBox="0 0 24 24">
                <path d="M5 5h14v14H5z" />
                <path d="M8 9h8M8 13h8M8 17h5" />
              </svg>
              Список
            </button>

            <button class="tab">
              <svg viewBox="0 0 24 24">
                <rect x="4" y="5" width="16" height="15" rx="2" />
                <path d="M8 3v4M16 3v4M4 10h16" />
              </svg>
              Календарь
            </button>

            <button class="tab">
              <svg viewBox="0 0 24 24">
                <path d="M6 3h9l4 4v14H6z" />
                <path d="M14 3v5h5" />
              </svg>
              Файлы
            </button>

            <button class="tab">
              <svg viewBox="0 0 24 24">
                <path d="M4 19V5" />
                <path d="M4 19h16" />
                <path d="M7 15l4-4 3 2 5-6" />
              </svg>
              Отчёты
            </button>
          </nav>

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

          <button class="create-button">
            <span>＋</span>
            Создать задачу
          </button>

          <button class="glass toolbar-button">
            <span class="dots">•••</span>
          </button>
        </section>

        <!-- Board -->
        <section class="board">
          <!-- BACKLOG -->
          <div class="column glass">
            <div class="column-header">
              <div>
                <span class="column-title">Бэклог</span>
                <span class="count">4</span>
              </div>

              <button class="column-settings">•••</button>
            </div>

            <div class="cards">
              <TaskCard
                title="Редизайн главной страницы"
                tag="Дизайн"
                tag-class="purple"
                comments="3"
                subtasks="5"
              />

              <TaskCard
                title="Настроить уведомления"
                tag="Бэкенд"
                tag-class="pink"
                comments="2"
                subtasks="3"
              />

              <TaskCard
                title="Интеграция с API"
                tag="Бэкенд"
                tag-class="pink"
                comments="5"
                subtasks="8"
              />

              <TaskCard
                title="Подготовить презентацию"
                tag="Маркетинг"
                tag-class="green"
                comments="1"
                subtasks="2"
              />
            </div>

            <button class="add-task">＋ &nbsp; Добавить задачу</button>
          </div>

          <!-- IN PROGRESS -->
          <div class="column glass">
            <div class="column-header">
              <div>
                <span class="column-title">В работе</span>
                <span class="count">3</span>
              </div>

              <button class="column-settings">•••</button>
            </div>

            <div class="cards">
              <TaskCard
                title="Адаптивная вёрстка"
                tag="Дизайн"
                tag-class="purple"
                comments="2"
                subtasks="4"
              />

              <!-- Card with subtasks -->
              <article class="task-card featured">
                <div class="task-top">
                  <h3>Разработка канбан доски</h3>

                  <button class="card-button">
                    <svg viewBox="0 0 24 24">
                      <path d="M6 4h12v16H6z" />
                      <path d="M9 9h6M9 13h6" />
                    </svg>
                  </button>
                </div>

                <span class="tag blue">Фронтенд</span>

                <div class="subtasks">
                  <div class="subtask">
                    <span class="checkbox"></span>
                    <span>Вёрстка доски</span>
                  </div>

                  <div class="subtask">
                    <span class="checkbox"></span>
                    <span>Логика перетаскивания</span>
                  </div>

                  <div class="subtask">
                    <span class="checkbox"></span>
                    <span>Сохранение порядка</span>
                  </div>
                </div>

                <button class="add-subtask">＋ Добавить подзадачу</button>
              </article>

              <TaskCard
                title="Тестирование фильтров"
                tag="Тестирование"
                tag-class="orange"
                comments="2"
                subtasks="4"
              />
            </div>

            <button class="add-task">＋ &nbsp; Добавить задачу</button>
          </div>

          <!-- REVIEW -->
          <div class="column glass">
            <div class="column-header">
              <div>
                <span class="column-title">На проверке</span>
                <span class="count">2</span>
              </div>

              <button class="column-settings">•••</button>
            </div>

            <div class="cards">
              <TaskCard
                title="Личный кабинет пользователя"
                tag="Фронтенд"
                tag-class="blue"
                comments="3"
                subtasks="6"
              />

              <TaskCard
                title="Экспорт данных"
                tag="Бэкенд"
                tag-class="pink"
                comments="2"
                subtasks="3"
              />
            </div>

            <button class="add-task">＋ &nbsp; Добавить задачу</button>
          </div>

          <!-- DONE -->
          <div class="column glass">
            <div class="column-header">
              <div>
                <span class="column-title">Готово</span>
                <span class="count">3</span>
              </div>

              <button class="column-settings">•••</button>
            </div>

            <div class="cards">
              <TaskCard
                title="Авторизация и регистрация"
                tag="Бэкенд"
                tag-class="purple"
                comments="2"
                subtasks="5"
                done
              />

              <TaskCard
                title="UI Kit компонентов"
                tag="Дизайн"
                tag-class="purple"
                comments="3"
                subtasks="7"
                done
              />

              <TaskCard
                title="Настроить CI/CD"
                tag="DevOps"
                tag-class="blue"
                comments="2"
                subtasks="4"
                done
              />
            </div>

            <button class="add-task">＋ &nbsp; Добавить задачу</button>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup>
import TaskCard from './TaskCard.vue'
</script>

<style scoped>
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

/* =========================================
   BACKGROUND
========================================= */

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

/* =========================================
   GLASS
========================================= */

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

/* =========================================
   APP
========================================= */

.app-shell {
  display: flex;
  min-height: 100vh;
  /* padding: 22px 20px; */
  gap: 16px;
}

.main {
  flex: 1;
  min-width: 0;
}

/* =========================================
   SIDEBAR
========================================= */

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

/* =========================================
   HEADER
========================================= */

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

.tabs {
  height: 100%;

  display: flex;
  align-items: center;

  gap: 4px;

  padding: 8px;

  border-radius: 18px;

  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tab {
  height: 48px;

  border: 0;
  border-radius: 13px;

  padding: 0 19px;

  display: flex;
  align-items: center;
  gap: 9px;

  color: rgba(255, 255, 255, 0.78);
  background: transparent;

  font-size: 15px;

  cursor: pointer;
  transition: all 0.2s ease;
}

.tab:hover:not(.active) {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.95);
}

.tab svg {
  width: 18px;
  height: 18px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;

  transition: transform 0.2s ease;
}

.tab:hover svg {
  transform: scale(1.1);
}

.tab.active {
  background: rgba(255, 255, 255, 0.14);
  color: #fff;

  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.17);
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

/* =========================================
   TOOLBAR
========================================= */

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

/* =========================================
   BOARD
========================================= */

.board {
  display: grid;

  grid-template-columns: repeat(4, minmax(240px, 1fr));

  gap: 14px;

  min-height: calc(100vh - 178px);
}

.column {
  border-radius: 20px;

  padding: 14px;

  display: flex;
  flex-direction: column;

  min-width: 0;

  transition: all 0.3s ease;
}

.column:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.08));
  border-color: rgba(255, 255, 255, 0.25);
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  height: 44px;

  padding: 0 5px 8px;
}

.column-header > div {
  display: flex;
  align-items: center;
  gap: 8px;
}

.column-title {
  font-size: 16px;
  font-weight: 500;
}

.count {
  min-width: 25px;
  height: 25px;

  padding: 0 7px;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  border-radius: 8px;

  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.1);

  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);

  transition: all 0.2s ease;
}

.count:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.column-settings {
  border: 0;
  background: transparent;

  color: rgba(255, 255, 255, 0.75);

  font-size: 17px;
  letter-spacing: 2px;

  cursor: pointer;
  transition: all 0.2s ease;
}

.column-settings:hover {
  color: rgba(255, 255, 255, 1);
  transform: scale(1.2);
}

.cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* =========================================
   TASK CARD
========================================= */

.task-card {
  border-radius: 15px;

  padding: 16px;

  background: linear-gradient(135deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.07));

  border: 1px solid rgba(255, 255, 255, 0.22);

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    0 8px 25px rgba(20, 25, 60, 0.08);

  min-height: 137px;

  cursor: pointer;
  transition: all 0.2s ease;
}

.task-card:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0.12));
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-3px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 12px 32px rgba(20, 25, 60, 0.15);
}

.task-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.task-card h3 {
  margin: 0 0 14px;

  font-size: 14px;
  line-height: 1.35;

  font-weight: 500;
}

.card-button {
  width: 24px;
  height: 24px;

  padding: 0;

  border: 0;
  background: transparent;

  color: rgba(255, 255, 255, 0.72);

  flex-shrink: 0;

  cursor: pointer;
  transition: all 0.2s ease;
}

.card-button:hover {
  color: rgba(255, 255, 255, 1);
  transform: scale(1.15);
}

.card-button svg {
  width: 18px;
  height: 18px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
}

.tag {
  display: inline-flex;
  align-items: center;

  height: 24px;

  padding: 0 9px;

  border-radius: 7px;

  font-size: 11px;
  font-weight: 500;

  background: rgba(255, 255, 255, 0.18);

  transition: all 0.2s ease;
}

.tag:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.tag.purple {
  background: rgba(139, 119, 255, 0.65);
}

.tag.pink {
  background: rgba(184, 102, 221, 0.65);
}

.tag.blue {
  background: rgba(76, 178, 224, 0.65);
}

.tag.green {
  background: rgba(85, 175, 119, 0.65);
}

.tag.orange {
  background: rgba(194, 139, 85, 0.7);
}

.task-meta {
  display: flex;
  align-items: center;

  gap: 15px;

  margin-top: 17px;

  color: rgba(255, 255, 255, 0.72);

  font-size: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.meta-icon {
  width: 15px;
  height: 15px;

  border: 1.4px solid currentColor;

  display: inline-block;
}

.meta-icon.comment {
  border-radius: 50%;
  position: relative;
}

.meta-icon.comment::after {
  content: '';

  position: absolute;
  right: -2px;
  bottom: -2px;

  width: 4px;
  height: 4px;

  border-left: 1px solid currentColor;
  transform: rotate(-20deg);
}

.meta-icon.subtask {
  border-radius: 4px;
}

/* =========================================
   SUBTASKS
========================================= */

.featured {
  min-height: 250px;
}

.subtasks {
  margin-top: 14px;

  border: 1px solid rgba(255, 255, 255, 0.13);
  border-radius: 10px;

  overflow: hidden;

  background: rgba(255, 255, 255, 0.04);
}

.subtask {
  height: 39px;

  padding: 0 11px;

  display: flex;
  align-items: center;
  gap: 9px;

  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  color: rgba(255, 255, 255, 0.74);

  font-size: 12px;

  cursor: pointer;
  transition: all 0.2s ease;
}

.subtask:hover {
  background: rgba(255, 255, 255, 0.08);
  padding-left: 14px;
}

.subtask:last-child {
  border-bottom: 0;
}

.checkbox {
  width: 18px;
  height: 18px;

  border: 1px solid rgba(255, 255, 255, 0.65);

  border-radius: 50%;

  transition: all 0.2s ease;
}

.checkbox:hover {
  border-color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.1);
}

.add-subtask {
  margin-top: 10px;

  border: 0;
  background: transparent;

  color: rgba(255, 255, 255, 0.75);

  font-size: 12px;

  cursor: pointer;
  transition: all 0.2s ease;
}

.add-subtask:hover {
  color: rgba(255, 255, 255, 1);
  transform: translateX(4px);
}

/* =========================================
   ADD TASK
========================================= */

.add-task {
  width: 100%;

  margin-top: auto;
  padding-top: 17px;

  border: 0;
  background: transparent;

  color: rgba(255, 255, 255, 0.75);

  font-size: 13px;

  text-align: center;

  cursor: pointer;
  transition: all 0.2s ease;
}

.add-task:hover {
  color: rgba(255, 255, 255, 1);
  transform: scale(1.02);
}

/* =========================================
   RESPONSIVE
========================================= */

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
  .board {
    grid-template-columns: repeat(2, minmax(260px, 1fr));

    overflow-y: auto;
  }

  .kanban-page {
    overflow: auto;
  }

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

  .board {
    grid-template-columns: 1fr;
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
}
</style>
