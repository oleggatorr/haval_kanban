// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { setupAuthGuards } from './guards'

// Определение маршрутов
const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/public/LoginVue.vue'),
    meta: {
      requiresAuth: false,
      title: 'Вход',
    },
  },
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/private/HomeView.vue'),
    meta: {
      requiresAuth: true,
      title: 'Главная',
    },
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('@/views/private/kanban/projects/ListProgectsVue.vue'),
    meta: {
      requiresAuth: true,
      title: 'Проекты',
    },
  },
  {
    path: '/project/:id',
    name: 'project',
    component: () => import('@/views/private/kanban/projects/ProgectVue.vue'),
    meta: {
      requiresAuth: true,
      title: 'Проект',
    },
  },
  {
    path: '/project/:project_id/board',
    name: 'project-board',
    component: () => import('@/views/private/kanban/boards/KanbanBoard.vue'),
    meta: {
      requiresAuth: true,
      title: 'Доска проекта',
    },
  },
  {
    path: '/board/:project_id',
    name: 'board',
    component: () => import('@/components/layout/KanbanBoard.vue'),
    meta: {
      requiresAuth: true,
      title: 'Канбан-доска',
    },
  },

  {
    path: '/profille',
    name: 'user',
    component: () => import('@/views/private/users/ProfileView.vue'),
    meta: {
      requiresAuth: true,
      title: 'Канбан-user',
    },
  },

  {
    path: '/test',
    name: 'user',
    component: () => import('@/views/private/kanban/test/test_board.vue'),
    meta: {
      requiresAuth: false,
      title: 'Канбан-user',
    },
  },

  {
    path: '/test2',
    name: 'user',
    component: () => import('@/views/private/kanban/test/KanbanPage.vue'),
    meta: {
      requiresAuth: false,
      title: 'Канбан-user',
    },
  },

  {
    path: '/test3/:id',
    name: 'test3',
    component: () => import('@/views/test1/ProgectInfoVue.vue'),
    props: true,
    meta: {
      requiresAuth: false,
      title: 'Проект',
    },
  },
  {
    path: '/test4/:id',
    name: 'test4',
    component: () => import('@/views/test2/TaskBoardView.vue'),
    props: true,
    meta: {
      requiresAuth: false,
      title: 'Канбан проекта',
    },
  },
  {
    path: '/test5/:id',
    name: 'test5',
    component: () => import('@/views/test2/ProjectInfoView.vue'),
    props: true,
    meta: {
      requiresAuth: false,
      title: 'Канбан проекта',
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue'),
    meta: {
      requiresAuth: false, // 404 не требует авторизации
      title: 'Страница не найдена',
    },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// ✅ Устанавливаем guards
setupAuthGuards(router)

export default router
