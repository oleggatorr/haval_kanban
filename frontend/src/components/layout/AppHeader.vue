<!-- src/components/AppHeader.vue -->
<template>
  <header class="app-header">
    <div class="header-container">
      <!-- Левая часть: Логотип + Навигация -->
      <div class="header-left">
        <router-link to="/" class="logo-link" title="На главную">
          <img
            src="@/assets/images/logo_5.png"
            alt="Logo"
            class="logo"
            @error="$event.target.style.display = 'none'"
          />
          <span class="logo-text">Кабан🐗</span>
        </router-link>

        <!-- Десктопная навигация -->
        <nav v-if="authStore.isAuthenticated" class="desktop-nav">
          <router-link to="/projects" class="nav-link" active-class="active">
            📁 Проекты
          </router-link>
          <router-link to="/tasks" class="nav-link" active-class="active"> ✅ Задачи </router-link>
        </nav>
      </div>

      <!-- Правая часть: Уведомления + Язык + Профиль -->
      <div class="header-right">
        <!-- Кнопка уведомлений (пока заглушка) -->
        <ActionButton
          v-if="authStore.isAuthenticated"
          icon="🔔"
          :tooltip="`${unreadCount} непрочитанных`"
          class="notification-btn"
          @click="handleNotifications"
        >
          <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
        </ActionButton>

        <!-- Переключатель языка -->
        <div class="lang-switcher">
          <button
            :class="['lang-btn', { active: currentLang === 'ru' }]"
            @click="changeLang('ru')"
            title="Русский"
          >
            RU
          </button>
          <button
            :class="['lang-btn', { active: currentLang === 'en' }]"
            @click="changeLang('en')"
            title="English"
          >
            EN
          </button>
        </div>

        <!-- Разделитель -->
        <div v-if="authStore.isAuthenticated" class="divider"></div>

        <!-- Секция пользователя -->
        <div v-if="authStore.isAuthenticated" class="user-section">
          <!-- Кнопка профиля с BurgerMenu -->
          <BurgerMenu
            :items="userMenuItems"
            placement="bottom-end"
            :title="authStore.user?.login || 'Профиль'"
          >
            <template #default="{ toggle }">
              <button class="user-btn" @click="toggle">
                <div class="user-avatar">
                  {{ getUserInitials }}
                </div>
                <div class="user-info">
                  <span class="user-name">{{ authStore.user?.login }}</span>
                  <span class="user-role" :class="authStore.user?.role">
                    {{ getRoleLabel(authStore.user?.role) }}
                  </span>
                </div>
                <span class="dropdown-arrow">▼</span>
              </button>
            </template>
          </BurgerMenu>
        </div>

        <!-- Кнопка входа для неавторизованных -->
        <router-link v-else to="/login" class="btn-login"> 🔑 Войти </router-link>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ActionButton from '@/components/ui/ActionButton.vue'
import BurgerMenu from '@/components/ui/BurgerMenu.vue'
import type { MenuItem } from '@/components/ui/BurgerMenu.vue'

const router = useRouter()
const authStore = useAuthStore()

// Состояния
const currentLang = ref('ru')
const unreadCount = ref(0)

// Вычисляемые свойства
const getUserInitials = computed(() => {
  const login = authStore.user?.login || ''
  return login.substring(0, 2).toUpperCase()
})

// Элементы меню пользователя
const userMenuItems = computed<MenuItem[]>(() => [
  {
    id: 'profile',
    label: '👤 Профиль',
    action: () => router.push('/profile'),
  },
  {
    id: 'settings',
    label: '⚙️ Настройки',
    action: () => router.push('/settings'),
  },
  {
    id: 'divider',
    label: '---',
    disabled: true,
  },
  {
    id: 'logout',
    label: '🚪 Выйти',
    action: handleLogout,
    danger: true,
  },
])

// Функции
const changeLang = (lang: string) => {
  currentLang.value = lang
  console.log(`Язык изменен на: ${lang}`)
  // TODO: Интеграция с i18n
}

const handleNotifications = () => {
  console.log('Открыть уведомления')
  // TODO: Открыть панель уведомлений
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const getRoleLabel = (role?: string) => {
  if (!role) return 'Гость'
  const roles: Record<string, string> = {
    admin: 'Админ',
    operator: 'Оператор',
    manager: 'Менеджер',
    user: 'Пользователь',
  }
  return roles[role] || role
}

// Инициализация при монтировании
onMounted(() => {
  // Здесь можно загрузить количество непрочитанных уведомлений
  // unreadCount.value = await fetchUnreadCount()
})
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  backdrop-filter: blur(10px);
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0.75rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

/* Левая часть */
.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: white;
  transition: all 0.3s ease;
  padding: 0.5rem;
  border-radius: 12px;
}

.logo-link:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.logo {
  height: 45px;
  width: auto;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.logo-text {
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: 1px;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Десктопная навигация */
.desktop-nav {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  padding: 0.6rem 1.2rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-2px);
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 3px;
  background: white;
  border-radius: 2px;
}

/* Правая часть */
.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Кнопка уведомлений */
.notification-btn {
  position: relative;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.6rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.2rem;
}

.notification-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ff4757;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(255, 71, 87, 0.4);
}

/* Переключатель языка */
.lang-switcher {
  display: flex;
  gap: 0.25rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.25rem;
  border-radius: 8px;
}

.lang-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.8);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.lang-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.lang-btn.active {
  background: white;
  color: #667eea;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Разделитель */
.divider {
  width: 1px;
  height: 30px;
  background: rgba(255, 255, 255, 0.3);
}

/* Секция пользователя */
.user-section {
  position: relative;
}

.user-btn {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.user-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.user-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: white;
}

.user-role {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 8px;
  display: inline-block;
}

.user-role.admin {
  background: rgba(255, 71, 87, 0.3);
  color: #ffe0e0;
}

.user-role.operator {
  background: rgba(46, 213, 115, 0.3);
  color: #d4ffd4;
}

.user-role.manager {
  background: rgba(255, 165, 2, 0.3);
  color: #fff3d4;
}

.user-role.user {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.dropdown-arrow {
  font-size: 0.7rem;
  opacity: 0.7;
  transition: transform 0.3s ease;
}

.user-btn:hover .dropdown-arrow {
  transform: rotate(180deg);
}

/* Кнопка входа */
.btn-login {
  background: white;
  border: 2px solid rgba(255, 255, 255, 0.5);
  color: #667eea;
  padding: 0.6rem 1.5rem;
  border-radius: 10px;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 700;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-login:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

/* Адаптивность */
@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }

  .header-container {
    padding: 0.75rem 1rem;
  }

  .logo-text {
    display: none;
  }
}

@media (max-width: 768px) {
  .user-info {
    display: none;
  }

  .user-btn {
    padding: 0.5rem;
  }

  .lang-switcher {
    display: none;
  }
}
</style>
