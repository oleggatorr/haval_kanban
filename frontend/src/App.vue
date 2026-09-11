<!-- src/App.vue -->
<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'

// Импорт глобальных стилей
import '@/assets/styles/main.css'
</script>

<template>
  <!-- <div id="app-container"> -->
  <!-- Шапка -->
  <!-- <AppHeader /> -->

  <!-- Основной контент -->
  <!-- <main class="content-wrapper"> -->
  <RouterView v-slot="{ Component }">
    <component :is="Component" :key="$route.fullPath" />
  </RouterView>
  <!-- </main> -->
  <!-- </div> -->
</template>

<style>
/* Ваши стили остаются без изменений */
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

#app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-image: url('@/assets/images/3xNT8aTLIlNOtrcptECM8tefiw.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-color: #f5f7fa;
}

.content-wrapper {
  flex: 1;
  padding: 2rem;
  position: relative;
  z-index: 1;
  /* margin-left: 70px;
  margin-right: 70px; */
  margin-top: 10px;
  transition: margin-left 0.3s ease;
}
</style>
