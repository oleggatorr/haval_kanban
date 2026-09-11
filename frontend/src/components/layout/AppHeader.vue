<!-- src/components/layout/AppHeader.vue -->
<template>
  <header class="app-header">
    <div class="header-container">
      <!-- Левая часть: Лого + Навигация -->
      <div class="header-left">
        <router-link to="/" class="logo-link" title="На главную">
          <div class="logo-wrapper">
            <img
              src="@/assets/images/logo_5.png"
              alt="Logo"
              class="logo-img"
              @error="$event.target.style.display = 'none'"
            />
          </div>
          <span class="logo-text">Кабан<span class="logo-accent">🐗</span></span>
        </router-link>

        <nav v-if="authStore.isAuthenticated" class="main-nav">
          <router-link
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="nav-item"
            active-class="active"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-label">{{ item.label }}</span>
          </router-link>
        </nav>
      </div>

      <!-- Правая часть: Действия + Профиль -->
      <div class="header-right">
        <!-- Поиск (заглушка) -->
        <button class="icon-btn" title="Поиск">
          <svg
            viewBox="0 0 24 24"
            width="18"
            height="18"
            stroke="currentColor"
            stroke-width="2"
            fill="none"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>

        <!-- Уведомления -->
        <button
          v-if="authStore.isAuthenticated"
          class="icon-btn notification-btn"
          title="Уведомления"
          @click="handleNotifications"
        >
          <svg
            viewBox="0 0 24 24"
            width="18"
            height="18"
            stroke="currentColor"
            stroke-width="2"
            fill="none"
          >
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <transition name="pop">
            <span v-if="unreadCount > 0" class="badge">{{
              unreadCount > 9 ? '9+' : unreadCount
            }}</span>
          </transition>
        </button>

        <!-- Язык -->
        <div class="lang-switcher">
          <button :class="['lang-btn', { active: currentLang === 'ru' }]" @click="changeLang('ru')">
            RU
          </button>
          <button :class="['lang-btn', { active: currentLang === 'en' }]" @click="changeLang('en')">
            EN
          </button>
        </div>

        <div v-if="authStore.isAuthenticated" class="divider"></div>

        <!-- Профиль -->
        <div v-if="authStore.isAuthenticated" class="user-section">
          <BurgerMenu :items="userMenuItems" placement="bottom-end" :offset="8">
            <template #default="{ toggle }">
              <button class="user-trigger" @click="toggle">
                <div class="avatar">
                  {{ getUserInitials }}
                </div>
                <div class="user-meta">
                  <span class="username">{{ authStore.user?.login }}</span>
                  <span class="role-tag" :class="authStore.user?.role">
                    {{ getRoleLabel(authStore.user?.role) }}
                  </span>
                </div>
                <svg
                  class="chevron"
                  viewBox="0 0 24 24"
                  width="14"
                  height="14"
                  stroke="currentColor"
                  stroke-width="2"
                  fill="none"
                >
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>
            </template>
          </BurgerMenu>
        </div>

        <!-- Вход -->
        <router-link v-else to="/login" class="login-btn"> Войти </router-link>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BurgerMenu from '@/components/ui/BurgerMenu.vue'
import type { MenuItem } from '@/components/ui/BurgerMenu.vue'

const router = useRouter()
const authStore = useAuthStore()

const currentLang = ref('ru')
const unreadCount = ref(0)

// Конфигурация навигации для удобства поддержки
const navItems = [
  { to: '/projects', label: 'Проекты', icon: '▦' },
  { to: '/tasks', label: 'Задачи', icon: '✓' },
]

const getUserInitials = computed(() => {
  const login = authStore.user?.login || ''
  return login.substring(0, 2).toUpperCase()
})

const userMenuItems = computed<MenuItem[]>(() => [
  { id: 'profile', label: '👤 Профиль', action: () => router.push('/profile') },
  { id: 'settings', label: '⚙️ Настройки', action: () => router.push('/settings') },
  { id: 'divider', label: '---', disabled: true },
  { id: 'logout', label: '🚪 Выйти', action: handleLogout, danger: true },
])

const changeLang = (lang: string) => {
  currentLang.value = lang
  // TODO: Интеграция i18n
}

const handleNotifications = () => {
  console.log('Open notifications panel')
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const getRoleLabel = (role?: string) => {
  const map: Record<string, string> = {
    admin: 'Админ',
    operator: 'Оператор',
    manager: 'Менеджер',
    user: 'Пользователь',
  }
  return role ? map[role] || role : 'Гость'
}

onMounted(async () => {
  // TODO: Загрузка счетчика уведомлений
})
</script>

<style scoped>
/* =========================================
   BASE & VARIABLES
========================================= */
.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: 12px 24px;
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    sans-serif;

  /* Glassmorphism Background */
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.header-container {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

/* =========================================
   LEFT: LOGO & NAV
========================================= */
.header-left {
  display: flex;
  align-items: center;
  gap: 32px;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: white;
  transition: opacity 0.2s ease;
}

.logo-link:hover {
  opacity: 0.9;
}

.logo-wrapper {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.15);
  overflow: hidden;
}

.logo-img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.logo-accent {
  margin-left: 2px;
  font-size: 16px;
}

.main-nav {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  color: white;
  background: rgba(255, 255, 255, 0.08);
}

.nav-item.active {
  color: white;
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-icon {
  font-size: 14px;
  opacity: 0.9;
}

/* =========================================
   RIGHT: ACTIONS & USER
========================================= */
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-btn {
  position: relative;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  border: 1px solid transparent;
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  border-color: rgba(255, 255, 255, 0.1);
}

.badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 8px;
  background: #ff4757;
  color: white;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(15, 23, 42, 0.8); /* Match header bg roughly */
}

/* Language Switcher */
.lang-switcher {
  display: flex;
  align-items: center;
  padding: 3px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.lang-btn {
  padding: 4px 8px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.5);
  font-size: 11px;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.lang-btn.active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.12);
  margin: 0 4px;
}

/* User Trigger */
.user-trigger {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 8px 4px 4px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.04);
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-trigger:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.user-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1px;
}

.username {
  font-size: 12px;
  font-weight: 600;
  line-height: 1.2;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.role-tag {
  font-size: 10px;
  font-weight: 500;
  line-height: 1.2;
  opacity: 0.6;
}

.chevron {
  opacity: 0.5;
  margin-left: 2px;
  transition: transform 0.2s ease;
}

.user-trigger:hover .chevron {
  opacity: 0.8;
}

/* Login Button */
.login-btn {
  padding: 8px 16px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.9);
  color: #1e293b;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.login-btn:hover {
  background: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
}

/* =========================================
   ANIMATIONS
========================================= */
.pop-enter-active,
.pop-leave-active {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.pop-enter-from,
.pop-leave-to {
  opacity: 0;
  transform: scale(0.5);
}

/* =========================================
   RESPONSIVE
========================================= */
@media (max-width: 1024px) {
  .main-nav {
    display: none; /* На планшетах скрываем меню, можно добавить бургер */
  }

  .user-meta {
    display: none;
  }

  .chevron {
    display: none;
  }

  .user-trigger {
    padding: 4px;
    border: none;
    background: transparent;
  }
}

@media (max-width: 768px) {
  .app-header {
    padding: 12px 16px;
  }

  .logo-text {
    display: none;
  }

  .lang-switcher {
    display: none;
  }

  .divider {
    display: none;
  }
}
</style>
