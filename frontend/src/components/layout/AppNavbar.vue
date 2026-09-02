<!-- src/components/AppNavbar.vue -->
<template>
  <aside class="sidebar-container">
    <nav class="sidebar">
      <ul class="nav-list">
        <!-- Список тикетов -->
        <li class="nav-item">
          <router-link to="/tickets" class="nav-link" active-class="active">
            <span class="icon">📂</span>
            <span class="text">Список заявок</span>
          </router-link>
        </li>

        <!-- Агенты (только для админа) -->
        <li v-if="isAdmin" class="nav-item">
          <router-link to="/agents" class="nav-link" active-class="active">
            <span class="icon">👥</span>
            <span class="text">Операторы</span>
          </router-link>
        </li>

        <!-- Департаменты -->
        <li class="nav-item">
          <router-link to="/departments" class="nav-link" active-class="active">
            <span class="icon">🏢</span>
            <span class="text">Департаменты</span>
          </router-link>
        </li>

        <!-- Категории -->
        <li class="nav-item">
          <router-link to="/question-category-list" class="nav-link" active-class="active">
            <span class="icon">📁</span>
            <span class="text">Категории</span>
          </router-link>
        </li>

        <!-- Баны -->
        <li class="nav-item">
          <router-link to="/bans" class="nav-link" active-class="active">
            <span class="icon">🚫</span>
            <span class="text">Блокировки</span>
          </router-link>
        </li>

        <!-- Настройки - прилеплена к низу -->
        <li class="nav-item nav-item-bottom">
          <router-link to="/settings" class="nav-link" active-class="active">
            <span class="icon">⚙️</span>
            <span class="text">Настройки</span>
          </router-link>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script setup lang="ts">
interface Props {
  isAdmin: boolean
  unreadCount?: number
}

withDefaults(defineProps<Props>(), {
  unreadCount: 0,
})
</script>

<style scoped>
.sidebar-container {
  position: fixed;
  left: 0;
  top: 77px; /* Отступ сверху под хедер */
  bottom: 0;
  width: 60px; /* Ширина свернутого состояния */
  z-index: 999;
  background-color: #f8f9fa;
  border-right: 1px solid #dee2e6;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);

  /* Ключевая часть: переход для ширины */
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden; /* Скрываем контент, выходящий за границы */
}

/* При наведении на контейнер расширяем его */
.sidebar-container:hover {
  width: 260px; /* Ширина развернутого состояния */
}

.sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 260px; /* Фиксируем ширину списка, чтобы текст не прыгал */
  height: 100%;
}

.nav-item {
  width: 100%;
}

/* Кнопка "Настройки" прилеплена к низу */
.nav-item-bottom {
  margin-top: auto;
}

.nav-link {
  display: flex;
  align-items: center;
  height: 48px; /* Фиксированная высота для красоты */
  padding: 0 1.2rem;
  color: #495057;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  white-space: nowrap; /* Запрещаем перенос текста */
  transition: background-color 0.2s;
  position: relative;
}

.nav-link .icon {
  font-size: 1.4rem;
  min-width: 30px;
  text-align: center;
  margin-right: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.nav-link .text {
  opacity: 0; /* Скрыт по умолчанию */
  transform: translateX(-10px); /* Небольшой сдвиг для анимации появления */
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
  flex-grow: 1;
}

/* Показываем текст при наведении на родительский контейнер */
.sidebar-container:hover .nav-link .text {
  opacity: 1;
  transform: translateX(0);
}

.nav-link:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: #2d3748;
}

.nav-link.active {
  color: #0ea5e9;
  background-color: rgba(14, 165, 233, 0.1);
  font-weight: 600;
}

/* Индикатор активного пункта слева */
.nav-link.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: #0ea5e9;
}

.badge-danger {
  background-color: #dc3545;
  color: white;
  font-size: 0.75rem;
  padding: 0.2em 0.6em;
  border-radius: 10px;
  font-weight: 700;
  opacity: 0;
  transition: opacity 0.2s ease;
  margin-left: auto;
}

/* Показываем бейдж при наведении */
.sidebar-container:hover .badge-danger {
  opacity: 1;
}

/* Адаптивность */
@media (max-width: 768px) {
  .sidebar-container {
    top: 70px;
    width: 50px;
  }

  .sidebar-container:hover {
    width: 220px;
  }

  .nav-list {
    width: 220px;
  }
}
</style>
